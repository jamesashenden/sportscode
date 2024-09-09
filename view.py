from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QMenuBar, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QLineEdit, QHBoxLayout, QGridLayout, QDialog, QMessageBox, QProgressBar

class View(QMainWindow):
    """
    VIEW component of MVC.
    
    View class to handle PyQT6 views for main app.
    """
    def __init__(self):
        super().__init__(parent=None)
        
        # Initialise window attributes.
        self.setWindowTitle("Sportscode")
        self.setGeometry(0, 0, 500, 200)
        
        # Setup base window layout.
        self.generalLayout = QVBoxLayout()
        
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(centralWidget)
        
        # Place in center of screen.
        screenGeometry = QApplication.primaryScreen().availableGeometry()
        windowGeometry = self.frameGeometry()
        centerPoint = screenGeometry.center()
        windowGeometry.moveCenter(centerPoint)
        self.move(windowGeometry.topLeft())
        
        # Initialise view components.
        self.init_menubar()
        self.init_updates()
        self.init_paths()
    

    def init_menubar(self):
        """
        Initialise window menubar.
        """
        menubar = self.menuBar()
        
        # Add File menu.
        fileMenu = menubar.addMenu("File")
        self.checkUpdatesAction = QAction("Check for Updates", self)
        fileMenu.addAction(self.checkUpdatesAction)
    
    
    """
    Menubar Methods
    """
    # Shows pop-up display already on latest version information.
    def showLatestVersion(self, version):
        popup = QMessageBox()
        popup.setWindowTitle("Check for Updates")
        popup.setText("Latest version v" + version + " already installed.")
        popup.setIcon(QMessageBox.Icon.Information)
        popup.setStandardButtons(QMessageBox.StandardButton.Ok)
        popup.exec()
    
    # Shows update downloading bar and message.
    def showDownloadingUpdate(self):
        self.updatesProgressBar.show()
        self.updatesLabel.show()
        
        self.updatesProgressBar.setValue(25)
        self.updatesLabel.setText("Downloading update...")
        
    # Shows update installing bar and message.
    def showInstallingUpdate(self):
        self.updatesProgressBar.show()
        self.updatesLabel.show()
        
        self.updatesProgressBar.setValue(75)
        self.updatesLabel.setText("Installing update...")
    
   
    def init_updates(self):
        """
        Initialises main view widgets.
        """
        
        # UPDATES PROGRESS BAR
        self.updatesProgressBar = QProgressBar(self)
        self.updatesProgressBar.setGeometry(30, 40, 400, 25)
        self.updatesProgressBar.setMaximum(100)
        self.generalLayout.addWidget(self.updatesProgressBar)
        self.updatesProgressBar.hide()
        
        # UPDATES LABEL
        self.updatesLabel = QLabel("BLANK")
        self.generalLayout.addWidget(self.updatesLabel)
        self.updatesLabel.hide()

        # VERSION LABEL
        self.versionLabel = QLabel("Version: ?")
        self.versionLabel.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.generalLayout.addWidget(self.versionLabel)


    def init_paths(self):
        """
        Initialises path view widgets.
        """
        
        # VIDEO FILE 
        self.filesLayout = QGridLayout()
        
        self.videoFileText = QLineEdit()
        self.filesLayout.addWidget(self.videoFileText, 0, 0)
        
        self.videoFileUpload = QPushButton("Upload Video")
        self.filesLayout.addWidget(self.videoFileUpload, 0, 1)
        
        # SAVE LOCATION       
        self.saveFileText = QLineEdit()
        self.filesLayout.addWidget(self.saveFileText, 1, 0)
        
        self.saveFileUpload = QPushButton("Choose Save Location")
        self.filesLayout.addWidget(self.saveFileUpload, 1, 1)
        
        self.generalLayout.addLayout(self.filesLayout)
        
    # Shows chosen video file path.
    def setVideoPath(self, path):
        self.videoFileText.setText(path)
        
    # Shows chosen save location path.
    def setSavePath(self, path):
        self.saveFileText.setText(path)