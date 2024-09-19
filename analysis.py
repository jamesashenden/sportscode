from faster_whisper import WhisperModel
from pyannote.audio import Pipeline
from moviepy.editor import VideoFileClip
import torch

from timeline import *
from scvideo import *

# TRANSCRIPTION SETUP 
model_size = "distil-large-v3"
model = WhisperModel(model_size, device="cpu", compute_type="int8")

# DIARIZATION SETUP
mps_device = torch.device("mps")
pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization", use_auth_token="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")
pipeline.to(mps_device)

# CONSTANTS
match_margin = 0.2

# Function to convert MP4 to WAV
def mp4_to_wav(mp4_path):
    wav_path = "temp.wav"
    video = VideoFileClip(mp4_path)
    audio = video.audio
    audio.write_audiofile(wav_path, codec='pcm_s16le')
    video.close()
    return wav_path

def run_analysis(video_path, save_path, window_model):
    
    # Initialise timeline.
    timeline = Timeline()
    
    # Add Coach's voice row.
    row = Row()
    row.name = "SPEAKER_00"
    row.colour = "#535353"
    timeline.addRow(row)
    # Add Player's voice row.
    row = Row()
    row.name = "SPEAKER_01"
    row.colour = "#535353"
    timeline.addRow(row)
    # Add Silence row.
    row = Row()
    row.name = "Silence"
    row.colour = "#535353"
    timeline.addRow(row)
    
    # Add Silence row.
    row = Row()
    row.name = "No Speaker"
    row.colour = "#535353"
    timeline.addRow(row)
    
    # Transcribe video.
    segments, info = model.transcribe(video_path, beam_size=1, language="en")
    
    # Create audio file of video.
    window_model.s_setProcessText.emit("Extracting audio...")
    audio = mp4_to_wav(video_path)
    
    # Run diarization.
    window_model.s_setProcessText.emit("Analysing number of voices...")
    diarization = pipeline(audio, min_speakers=1, max_speakers=2)
    
    
    last_segment_end = 0
    count = 0
    uncoded = []
    # Iterate through each segment in the transcription.
    for segment in segments:
         # Show transcribed text.
        window_model.s_setProcessText.emit(segment.text)
        print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
        
        
        # Code silence if gap from start of this to end of last.
        if last_segment_end and last_segment_end < segment.start:

            # Check silence is long enough.
            if (segment.start - last_segment_end) > 0.5:
                        
                silence = Code()
                silence.startTime = last_segment_end
                silence.endTime = segment.start
                timeline.rows["Silence"].addInstance(silence)
            
        last_segment_end = segment.end
        
        # Create Code for current segment.
        code = Code()
        code.startTime = segment.start
        code.endTime = segment.end
        # code.labels.append(Labels.labels["POSITIVE"])
        
        coded = False
        # Calculate determined speaker for segment.
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            
            # Skip if already coded.
            if coded:
                continue
            
            # If time intervals overlap.
            if not (segment.end < turn.start - match_margin or segment.start > turn.end + match_margin):
                
                timeline.rows[speaker].addInstance(code)
                coded = True
        
        # If not coded, add to list to add later.
        if not coded:
            uncoded.append(code)
            
        # Update progress bar.
        if count < 90:
            count+=5
            window_model.s_updateProgressBar.emit(count)

    if timeline.rows['SPEAKER_00'].instanceCount > timeline.rows['SPEAKER_01'].instanceCount:
        timeline.rows['SPEAKER_00'].name = "Coach's Voice"
        timeline.rows['SPEAKER_01'].name = "Player's Voice"
    else:
        timeline.rows['SPEAKER_01'].name = "Coach's Voice"
        timeline.rows['SPEAKER_00'].name = "Player's Voice"
            
    for code in uncoded:
        timeline.rows["Coach's Voice"].addInstance(code)
    
    # Output diarization results.
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        print(f"Speaker {speaker} speaks from {turn.start:.1f}s to {turn.end:.1f}s")

    # Remove old audio file.
    os.remove(audio)

    # Compile SCVideo file.
    scvideo = SCVideo(timeline=timeline, video_path=video_path, save_path=save_path)
    scvideo.createFile()