from PyQt5.QtWidgets import QApplication
from graphicInterface.window import *
import sys

if __name__ == "__main__":

    app = QApplication(sys.argv)

    w = Window()
    sys.exit(app.exec_())
