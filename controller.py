from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import QApplication

import sys, os

class Controller:
    """
    CONTROLLER component of MVC.
    """
    def __init__(self, model, view):
        self.model = model
        self.view = view
        
        """
        Menubar Connections
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
        self.updatesWorker.s_completedUpdate.connect(self.restart)
    
    
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
    s_completedUpdate = pyqtSignal()
    
    def __init__(self, model):
        super().__init__()
        self.model = model
        
    def run(self):
        self.model.checkForUpdates()
        self.s_completedUpdate.emit()