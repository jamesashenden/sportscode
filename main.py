import sys
from functools import partial
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QMenuBar, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog

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
        self.versionLabel = QLabel("Version: ")
        self.generalLayout.addWidget(self.versionLabel)
        
        self.setButton = QPushButton("Change")
        self.setButton.clicked.connect(partial(self.setVersionText, "HELLO"))
        self.generalLayout.addWidget(self.setButton)
        
        self.uploadButton = QPushButton("Upload Video")
        self.uploadButton.clicked.connect(self.uploadVideo)
        self.generalLayout.addWidget(self.uploadButton)

    def setVersionText(self, text):
        self.versionLabel.setText(text)
        
    def uploadVideo(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select the video to upload.")
        if file_path:
            self.setVersionText(file_path)
            run_analysis(video_path=file_path)
        else:
            self.setVersionText("No file.")
        

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