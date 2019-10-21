from graphicInterface.main_widget import *
from pointRegistration.registration_param import RegistrationParameters
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QStatusBar, QWidget, QPushButton


class DisplacementMapWindow(QMainWindow):

    def __init__(self, parent, model):
        super().__init__(parent=parent)
        self.setWindowIcon(QIcon('resources/icon.png'))
        self.statusLabel = QLabel("Ready")
        self.setWindowTitle("Displacement Map")
        self.model = model
        self.initUI()

    def initUI(self):
        central_widget = QWidget(self)
        grid_central = QGridLayout(self)
        central_widget.setLayout(grid_central)
        self.setCentralWidget(central_widget)
        self.setLayout(grid_central)
        grid_central.addWidget(RotatableFigure(parent=self, model=self.model, title="Displacement Map"), 0, 0, 19, 1)
        grid_central.addWidget(LowerToolbar(self), 20, 0, 1, 1)
        self.resize(800, 600)
        statusBar = QStatusBar()
        self.setStatusBar(statusBar)
        #statusBar.addWidget(self.statusLabel)
        #statusBar.addPermanentWidget(QLabel(RegistrationParameters().to_string()))
        #self.setWindowTitle('Shape Registrator')
        #self.setStatus("Ready.")
        self.show()


class LowerToolbar(QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(QPushButton("Save Displacement Map on File"), 0, 1, 1, 1)
        self.layout.addWidget(QPushButton("xxxx"), 0, 3, 1, 1)