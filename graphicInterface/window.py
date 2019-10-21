from graphicInterface.main_widget import *
from graphicInterface.console import Logger
from pointRegistration.registration_param import RegistrationParameters
from PyQt5.QtGui import QIcon


class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('resources/icon.png'))
        Logger()
        self.statusLabel = QLabel("")
        self.initUI()

    def initUI(self):
        self.mainWidget = MainWidget(self)
        self.setCentralWidget(self.mainWidget)
        self.resize(1000, 600)
        self.center()
        statusBar = QStatusBar()
        self.setStatusBar(statusBar)
        statusBar.addWidget(self.statusLabel)
        statusBar.addPermanentWidget(QLabel(RegistrationParameters().to_string()))
        self.setWindowTitle('Shape Registrator')
        self.setStatus("Ready.")
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def setStatus(self, message):
        self.statusLabel.setText(message)

    def setStatusReady(self):
        self.setStatus("Ready")
