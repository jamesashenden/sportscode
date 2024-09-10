from faster_whisper import WhisperModel

from timeline import *
from scvideo import *

# TRANSCRIPTION SETUP
model_size = "distil-large-v3"
# run on CPU with INT8
model = WhisperModel(model_size, device="cpu", compute_type="int8")


def run_analysis(video_path, save_path, window_model):
    # Call to transcribe video.
    segments, info = model.transcribe(video_path, beam_size=5, language="en")

    print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

    timeline = Timeline()

    last_segment_end = 0

    count = 0
    # Iterate through each segment in the transcription.
    for segment in segments:
        print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
        
        # Code silence if gap from start of this to end of last.
        if last_segment_end and last_segment_end < segment.start:

            # Check silence is long enough.
            if (segment.start - last_segment_end) > 0.5:
                        
                silence = Code()
                silence.startTime = last_segment_end
                silence.endTime = segment.start
                try:
                    timeline.rows["Silence"].addInstance(silence)
                except:
                    row = Row()
                    row.name = "Silence"
                    row.colour = "#535353"
                    timeline.addRow(row)
                    timeline.rows["Silence"].addInstance(silence)
            
        last_segment_end = segment.end
        
        code = Code()
        code.startTime = segment.start
        code.endTime = segment.end
        # code.labels.append(Labels.labels["POSITIVE"])
        
        try:
            timeline.rows["Coach's Voice"].addInstance(code)
        except:
            row = Row()
            row.name = "Coach's Voice"
            row.colour = "#535353"
            timeline.addRow(row)
            timeline.rows["Coach's Voice"].addInstance(code)
            
        # Show transcribed text.
        window_model.s_setProcessText.emit(segment.text)
            
        # Update progress bar.
        if count < 90:
            count+=5
            window_model.s_updateProgressBar.emit(count)

    scvideo = SCVideo(timeline=timeline, video_path=video_path, save_path=save_path)
    scvideo.createFile()