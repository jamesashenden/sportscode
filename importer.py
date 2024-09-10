import os, json
from moviepy.video.io.VideoFileClip import VideoFileClip
from faster_whisper import WhisperModel

modelData = {
    'text': [],
    'label': []
}

def process_video(path):
    filename = os.path.splitext(os.path.basename(path))[0]
    timeline_path = os.path.join(path, filename + ".SCTimeline")
    video_path = os.path.join(path, "Video/Stream0000/Segment_00000.mov")

    video = VideoFileClip(video_path)

    model_size = "large-v3"
    model = WhisperModel(model_size, device="cpu", compute_type="int8")

    with open(timeline_path, "r") as file:
        data = json.load(file)

    all_rows = data['timeline']['rows']

    target_row = None
    for row in all_rows:
        if row['name'] == "Coach's Voice":
            target_row = row

    # PER CODE
    for instance in target_row['instances']:
        print(instance['startTime'])
        print(instance['endTime'])
        
        if instance['endTime'] > video.duration:
            instance['endTime'] = video.duration
        
        clip = video.subclip(instance['startTime'], instance['endTime']) 
        audio = clip.audio
        audio.write_audiofile('clip.wav')
        
        segments, info = model.transcribe('clip.mp3', beam_size=5)
        for segment in segments:
            print(segment.text)
            for label in instance['labels']:
                print(label['name'])
                modelData['text'].append(segment.text)
                modelData['label'].append(label['name'])
                
        os.remove('clip.wav')
    
        
            
        print("+++++")
        
folder = "/Users/jamesashenden/Desktop/SportscodeTrain/"
with os.scandir(folder) as files:
    for file in files:
        if os.path.splitext(os.path.basename(file.path))[1] == ".SCVideo":
            print(file.path)
            process_video(file.path)
            
with open('data.json', 'w') as file:
    file.write(json.dumps(modelData))