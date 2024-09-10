from PyQt6.QtCore import QObject, pyqtSignal, QThread

import requests, time, os, subprocess

from main import VERSION
from analysis import run_analysis

class Model(QObject):
    """
    MODEL component of MVC.
    """
    s_checkUpdatesOnLatestVersion = pyqtSignal(str)
    s_downloadingUpdate = pyqtSignal()
    s_installingUpdate = pyqtSignal()
    s_completedUpdate = pyqtSignal()
    
    s_setVideoPath = pyqtSignal(str)
    s_setSavePath = pyqtSignal(str)
    s_showPathsError = pyqtSignal(str)
    
    s_toggleInputLock = pyqtSignal(int)
    s_updateProgressBar = pyqtSignal(int)
    s_setProcessText = pyqtSignal(str)
    s_hideProcessText = pyqtSignal()
    
    version = VERSION
    
    videoPath = ""
    savePath = ""
    valid_extensions = [".MP4", ".mp4", ".mov", ".MOV"]
    
    def __init__(self):
        super().__init__()
        
    
    def checkForUpdates(self):
        """
        Updates method.
        """
        
        # Get current version.
        current_version = VERSION
        
        # Get latest version.
        response = requests.get("https://jamesashenden.github.io/sportscode/updates.json")
        if response.status_code != 200: # If invalid or error response, break.
            self.s_checkUpdatesOnLatestVersion.emit("")
            return
        latest = response.json()['latest']
        if not latest:
            self.s_checkUpdatesOnLatestVersion.emit("")
            return
        latest_version = latest['version']
        latest_url = latest['url']
        
        # Compare latest version to current version.
        if not latest_version:
            return
        if current_version == latest_version: # If already on the latest version, break.
            self.s_checkUpdatesOnLatestVersion.emit(current_version) # Show popup message.
            return
        
        # Set view to downloading update.
        self.s_downloadingUpdate.emit()
        
        # Download latest version.
        save_path = os.path.join(os.getcwd(), 'latest.zip')
        r = requests.get(latest_url, stream=True)
        with open(save_path, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=1024):
                fd.write(chunk)
        
        # Set view to installing update.
        self.s_installingUpdate.emit()
        
        # Apply latest version.
        app_path = os.path.join(os.getcwd(), "../../..")
        self.setVersionText("Applying update...")
        subprocess.run(['unzip', '-o', save_path, '-d', app_path], check=True)
        
        # Delete zip file.
        os.remove(save_path)
        
        # Emit restart signal.
        self.s_completedUpdate.emit()
        
    def processVideo(self):
        """
        Process video method.
        """
        
        # Show error if no paths are selected.
        if self.videoPath == "":
            self.s_showPathsError.emit("Please select a video file to process.")
            return
        if self.savePath == "":
            self.s_showPathsError.emit("Please select a location to save the processed video.")
            return
        
        # Lock inputs.
        self.s_toggleInputLock.emit(1)
        self.s_hideProcessText.emit()
        
        # Show initial progress bar.
        self.s_updateProgressBar.emit(0)
        
        # Start analysis.
        run_analysis(video_path=self.videoPath, save_path=self.savePath, window_model=self)
        
        # Show complete.
        self.s_updateProgressBar.emit(100)
        self.s_setProcessText.emit("Complete!")
        
        # Unlock inputs.
        self.s_toggleInputLock.emit(0)
        
    def setVideoPath(self, path):
        """
        videoPath setter.
        """
        extension = os.path.splitext(os.path.basename(path))[1]
        if extension not in self.valid_extensions: # If invalid extensions show error.
            self.s_showPathsError.emit("Invalid file type - please select a video file.")
            return
        
        self.videoPath = path    
        self.s_setVideoPath.emit(path)
        
    def setSavePath(self, path):
        """
        savePath setter.
        """
        self.savePath = path
        self.s_setSavePath.emit(path)