from PyQt6.QtCore import QObject, pyqtSignal, QThread

import requests, time, os, subprocess

from main import VERSION

class Model(QObject):
    """
    MODEL component of MVC.
    """
    s_checkUpdatesOnLatestVersion = pyqtSignal(str)
    s_downloadingUpdate = pyqtSignal()
    s_installingUpdate = pyqtSignal()
    
    def __init__(self):
        super().__init__()
    
    def checkForUpdates(self):
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