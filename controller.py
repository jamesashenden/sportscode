from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import QApplication, QFileDialog

import sys, os

class Controller:
    """
    CONTROLLER component of MVC.
    """
    def __init__(self, model, view):
        self.model = model
        self.view = view
        
        """
        View Initialisation
        """
        self.view.versionLabel.setText("Version: " + self.model.version)
        
        """
        Updates Connections
        """
        self.updatesWorker = UpdatesWorker(self.model)
        
        # Check for Updates button triggered.
        self.view.checkUpdatesAction.triggered.connect(self.updatesWorker.start)
        # Show latest version message.
        self.model.s_checkUpdatesOnLatestVersion.connect(self.view.showLatestVersion)
        
        # Show downloading update.
        self.model.s_downloadingUpdate.connect(self.view.showDownloadingUpdate)
        # Show installing update.
        self.model.s_installingUpdate.connect(self.view.showInstallingUpdate)
        # Once update complete, restart app.
        self.model.s_completedUpdate.connect(self.restart)
        
        """
        Paths Connections
        """
        # Show file selector dialog for video path upload.
        self.view.videoFileUpload.clicked.connect(self.chooseVideoPath)
        # Show chosen video in path.
        self.model.s_setVideoPath.connect(self.view.setVideoPath)
        
        # Show file selector dialog for save path upload.
        self.view.saveFileUpload.clicked.connect(self.chooseSavePath)
        # Show chosen save location in path.
        self.model.s_setSavePath.connect(self.view.setSavePath)
    
    
    def chooseVideoPath(self):
        """
        Method to get selected video path and set.
        """
        file_path, _ = QFileDialog.getOpenFileName(self.view, "Select the video to upload.")
        if file_path:
            self.model.setVideoPath(file_path)
            
    def chooseSavePath(self):
        """
        Method to get selected save path and set.
        """
        folder_path = QFileDialog.getExistingDirectory(self.view, "Select a save location.")
        if folder_path:
            self.model.setSavePath(folder_path)
    
    
    def restart(self):
        """
        Method to restart the app.
        """
        QApplication.quit()
        python = sys.executable
        os.execl(python, python, *sys.argv)
        
        
class UpdatesWorker(QThread):
    """
    Worker to handle downloading and installing updates in the background.
    """
    
    def __init__(self, model):
        super().__init__()
        self.model = model
        
    def run(self):
        self.model.checkForUpdates()