import os, json, shutil

from timeline import gen_unique_id

class SCVideo:
    def __init__(self, filename, timeline, video_path) -> None:
        self.filename = filename
        self.timeline = timeline
        self.video_path = video_path
        
        self.rootPath = os.getcwd()
        self.filePath = os.path.join(self.rootPath, self.filename+".SCVideo")
        
    def generatePackageMetaText(self) -> str:
        text = {
                "source" : "import",
                "createdWithBuild" : "55790.d54139e",
                "architecture" : "x86_64,arm64",
                "createdDate" : "2024-08-06T20:42:18.545Z",
                "version" : "1.0.0",
                "type" : "standalone",
                "createdWithVersion" : "12.39.0",
                "hideGameTimeRows" : False
            }
        
        return text
    
    def generateVideoText(self) -> str:
        text = {
            "id": gen_unique_id()
        }
        
        return text
    
    def generateStreamText(self) -> str:
        text = {
                    "id" : gen_unique_id(),
                    "name" : "Angle 1",
                    "isAudioMuted" : False,
                    "source" : "unknown",
                    "segments" : []
                }
        
        return text
        
    def createFile(self) -> None:
        os.mkdir(self.filePath) #Make .SCVideo folder.
        video_path = os.path.join(self.filePath, "Video")
        os.mkdir(video_path) #Make Video folder.
        
        # Create package.meta file.
        with open( os.path.join(self.filePath, "package.meta"), 'w') as file:
            file.write( json.dumps(self.generatePackageMetaText()) )
        
        # Create video.json file.
        with open( os.path.join(video_path, "video.json"), 'w' ) as file:
            file.write( json.dumps(self.generateVideoText()) )
        
        # Create timeline file.
        self.timeline.createFile( self.filePath, self.filename )
        
        # Create Stream folder.
        stream_path = os.path.join(video_path, "Stream0000")
        os.mkdir(stream_path)
        
        # Create stream.json file.
        with open( os.path.join(stream_path, "stream.json"), 'w' ) as file:
            file.write( json.dumps(self.generateStreamText()) )
    
        # Copy video to Stream folder.
        new_video_path = os.path.join(stream_path, "Segment_00000."+self.video_path[-3:])
        print(new_video_path)
        shutil.copy(self.video_path, new_video_path)