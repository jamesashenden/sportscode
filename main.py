import sys, requests
from functools import partial
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QMenuBar, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QLineEdit, QHBoxLayout, QGridLayout

from timeline import *
from scvideo import *
from analysis import run_analysis

class Window(QMainWindow):
    """
    Main application window / GUI.
    """
    
    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("Sportscode")
        self.setBaseSize(100, 100)
        self.generalLayout = QVBoxLayout()
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(centralWidget)
        
        self.init_view()
    
    def init_view(self):
        
        ####
        # FILES LAYOUT
        ####
        # VIDEO FILE 
        self.filesLayout = QGridLayout()
        
        self.videoFileText = QLineEdit()
        self.filesLayout.addWidget(self.videoFileText, 0, 0)
        
        self.videoFileUpload = QPushButton("Upload Video")
        self.videoFileUpload.clicked.connect(self.uploadVideo)
        self.filesLayout.addWidget(self.videoFileUpload, 0, 1)
        
        ####
        # SAVE LOCATION       
        self.saveFileText = QLineEdit()
        self.filesLayout.addWidget(self.saveFileText, 1, 0)
        
        self.saveFileUpload = QPushButton("Choose Save Location")
        self.saveFileUpload.clicked.connect(self.setSaveLocation)
        self.filesLayout.addWidget(self.saveFileUpload, 1, 1)
        
        self.generalLayout.addLayout(self.filesLayout)
        ####
        
        ####
        # PROCESS VIDEO BUTTON
        self.processButton = QPushButton("Process Video")
        self.processButton.clicked.connect(self.processVideo)
        self.generalLayout.addWidget(self.processButton)
        ####
        
        ####
        # VERSION LABEL
        self.versionLabel = QLabel("Version: 1.0")
        self.versionLabel.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.generalLayout.addWidget(self.versionLabel)
        ####
        
        ####
        # CHECK FOR UPDATES BUTTON
        self.updatesButton = QPushButton("Check for Updates")
        self.updatesButton.clicked.connect(self.checkForUpdates)
        self.generalLayout.addWidget(self.updatesButton)
        ####
        
        #self.setButton = QPushButton("Change")
        #self.setButton.clicked.connect(partial(self.setVersionText, "HELLO"))
        #self.generalLayout.addWidget(self.setButton)
    

    def setVersionText(self, text):
        self.versionLabel.setText(text)
        
    def uploadVideo(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select the video to upload.")
        print(file_path)
        if file_path:
            self.videoFileText.setText(file_path)
        else:
            self.setVersionText("No file.")
        
    def setSaveLocation(self):
        folder_path  = QFileDialog.getExistingDirectory(self, "Select a save location.")
        if folder_path:
            self.saveFileText.setText(folder_path)
        else:
            self.setVersionText("No file.")
            
    def processVideo(self):
        run_analysis(video_path=self.videoFileText.text(), save_path=self.saveFileText.text())
        
    def checkForUpdates(self):
        # Get current version.
        from setup import OPTIONS
        current_version = OPTIONS['plist']['CFBundleShortVersionString']
        
        # Get latest version.
        response = requests.get("https://jamesashenden.github.io/sportscode/updates.txt")
        if response.status_code != 200:
            pass
        latest_version = response.text.strip()
        
        # Compare latest version to current version.
        if not latest_version:
            pass
        if current_version == latest_version:
            pass
        
        # Download latest version.
        save_path = os.getcwd()
        response = requests.get("https://jamesashenden.github.io/sportscode/latest.zip", stream=True)
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        
    

def main():
    """
    Application root main method.
    """
    app = QApplication([])
    window = Window()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()