from graphicInterface.mainWidget import *


class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.mainWidget = MainWidget(self)
        self.setCentralWidget(self.mainWidget)
        self.resize(1000, 600)
        self.center()
        self.setWindowTitle('Shape Registrator')
        self.statusBar().showMessage("Ready.")
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def setStatus(self, message):
        self.statusBar().showMessage(message)

    def setStatusReady(self):
        self.statusBar().showMessage("Ready.")
