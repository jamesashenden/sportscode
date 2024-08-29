from faster_whisper import WhisperModel
from transformers import pipeline

from timeline import *
from scvideo import *

# TRANSCRIPTION SETUP
model_size = "large-v3"
# run on CPU with INT8
model = WhisperModel(model_size, device="cpu", compute_type="int8")

# NLP SETUP
classifier = pipeline('sentiment-analysis')

def run_analysis(video_path):
    # Call to transcribe video.
    segments, info = model.transcribe(video_path, beam_size=5)

    print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

    timeline = Timeline()

    # Iterate through each segment in the transcription.
    for segment in segments:
        print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
        
        # Run NLP on transcribed text.
        result = classifier(segment.text)[0]
        print("%s %.2f" % (result['label'], result['score']))
        
        code = Code()
        code.startTime = segment.start
        code.endTime = segment.end
        
        try:
            timeline.rows[result['label']].addInstance(code)
        except:
            row = Row()
            row.name = result['label']
            timeline.addRow(row)
            timeline.rows[result['label']].addInstance(code)

        

    # row = Row()
    # row.name = "Positive"
    # timeline.addRow(row)

    # row = Row()
    # row.name = "Negative"
    # timeline.addRow(row)

    # code = Code()
    # timeline.rows['Positive'].addInstance(code)
    # timeline.rows['Negative'].addInstance(code)

    scvideo = SCVideo(filename='fulltest', timeline=timeline, video_path=video_path)
    scvideo.createFile()