import sys, requests, zipfile, os, urllib.request, shutil, subprocess, time
from functools import partial
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QMenuBar, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QLineEdit, QHBoxLayout, QGridLayout, QDialog, QMessageBox, QProgressBar

from model import *
from view import *
from controller import *

from timeline import *
from scvideo import *
from analysis import run_analysis

VERSION = "0.0.4"        

def main():
    """
    Application root main method.
    """
    app = QApplication([])
    
    model = Model()
    view = View()
    controller = Controller(model=model, view=view)
    
    view.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()