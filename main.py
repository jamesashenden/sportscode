import sys, requests, zipfile, os, urllib.request, shutil, subprocess, time
from functools import partial
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QMenuBar, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QLineEdit, QHBoxLayout, QGridLayout, QDialog, QMessageBox, QProgressBar

from timeline import *
from scvideo import *
from analysis import run_analysis

VERSION = "0.0.3"      

class Window(QMainWindow):
    """
    Main application window / GUI.
    """
    
    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("Sportscode")
        self.setGeometry(0, 0, 500, 200)
        self.generalLayout = QVBoxLayout()
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(centralWidget)
        
        self.init_menubar()
        self.init_view()
        
        # Place in center of screen.
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        window_geometry = self.frameGeometry()
        center_point = screen_geometry.center()
        window_geometry.moveCenter(center_point)
        self.move(window_geometry.topLeft())
    
    def init_menubar(self):
        menubar = self.menuBar()
        
        file_menu = menubar.addMenu("File")
        
        updates_action = QAction("Check for Updates", self)
        file_menu.addAction(updates_action)
        updates_action.triggered.connect(self.checkForUpdates)
    
    def init_view(self):
        
        ####
        # VERSION LABEL
        self.versionLabel = QLabel("Version: " + VERSION)
        self.versionLabel.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.generalLayout.addWidget(self.versionLabel)
        ####
        
        ####
        # PROGRESS BAR
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(30, 40, 400, 25)
        self.progress_bar.setMaximum(100)
        self.generalLayout.addWidget(self.progress_bar)
        self.progress_bar.hide()
        ####
        
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
        # CHECK FOR UPDATES BUTTON
        # self.updatesButton = QPushButton("Check for Updates")
        # self.updatesButton.clicked.connect(self.checkForUpdates)
        # self.generalLayout.addWidget(self.updatesButton)
        ####
        
        #self.setButton = QPushButton("Change")
        #self.setButton.clicked.connect(partial(self.setVersionText, "HELLO"))
        #self.generalLayout.addWidget(self.setButton)
    

    def setVersionText(self, text):
        self.versionLabel.setText(text)
        QApplication.processEvents()
        
    def uploadVideo(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select the video to upload.")
        if file_path:
            self.videoFileText.setText(file_path)
        
    def setSaveLocation(self):
        folder_path  = QFileDialog.getExistingDirectory(self, "Select a save location.")
        if folder_path:
            self.saveFileText.setText(folder_path)
            
    def updateProgressBar(self, value):
        self.progress_bar.setValue(value)
        QApplication.processEvents()
        self.progress_bar.setValue(value)
        QApplication.processEvents()
            
    def processVideo(self):
        self.progress_bar.show()
        self.progress_bar.setValue(0)
        QApplication.processEvents()
        self.progress_bar.setValue(1)
        QApplication.processEvents()
        
        run_analysis(video_path=self.videoFileText.text(), save_path=self.saveFileText.text(), window=self)
        self.updateProgressBar(100)
        
    def checkForUpdates(self):
        # Get current version.
        current_version = VERSION
        
        # Get latest version.
        response = requests.get("https://jamesashenden.github.io/sportscode/updates.json")
        if response.status_code != 200:
            return
        latest = response.json()['latest']
        latest_version = latest['version']
        latest_url = latest['url']
                
        # Compare latest version to current version.
        if not latest_version:
            return
        if current_version == latest_version:
            # Show popup confirmation and break.
            popup = QMessageBox()
            popup.setWindowTitle("Check for Updates")
            popup.setText("Latest version v" + latest_version + " already installed.")
            popup.setIcon(QMessageBox.Icon.Information)
            popup.setStandardButtons(QMessageBox.StandardButton.Ok)
            popup.exec()            
            return
        
        # Show update bar.
        self.update_bar = QProgressBar(self)
        self.update_bar.setGeometry(30, 40, 400, 25)
        self.update_bar.setMaximum(100)
        self.generalLayout.addWidget(self.update_bar)
        # Show label.
        self.updating_label = QLabel("Downloading update...")
        self.generalLayout.addWidget(self.updating_label)
        self.update_bar.setValue(25)
        QApplication.processEvents()
        
        # Download latest version.
        save_path = os.path.join(os.getcwd(), 'latest.zip')
        r = requests.get(latest_url, stream=True)
        with open(save_path, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=1024):
                fd.write(chunk)
        
        self.update_bar.setValue(65)
        self.updating_label = QLabel("Installing...")
        QApplication.processEvents()
        
        # Apply latest version.
        app_path = os.path.join(os.getcwd(), "../../..")
        self.setVersionText("Applying update...")
        subprocess.run(['unzip', '-o', save_path, '-d', app_path], check=True)
        
        self.update_bar.setValue(85)
        self.updating_label = QLabel("Removing update file...")
        QApplication.processEvents()
    
        # Delete zip file.
        os.remove(save_path)
        
        self.update_bar.setValue(75)
        self.updating_label = QLabel("Restarting...")
        QApplication.processEvents()
        
        # Restart app.
        QApplication.quit()
        python = sys.executable
        os.execl(python, python, *sys.argv)
        

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