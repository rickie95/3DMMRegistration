from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QComboBox, QPushButton, QAction, QFileDialog, QGroupBox
from PyQt5.QtCore import pyqtSlot
from PyQt5.Qt import *


class UpperToolbar(QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        #bc1 = bigCell(self, QLabel("Metodo di registrazione:"), registrationMethodsCombobox())
        #bc2 = bigCell(self, QLabel("Carica modello:"), LoadModelButton("Scegli.."))
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        group1 = QGroupBox("Registrazione")
        layoutGB1 = QGridLayout()
        group1.setLayout(layoutGB1)
        label = QLabel("Metodo di registrazione:")
        label.setAlignment(Qt.AlignCenter)
        layoutGB1.addWidget(label, 0, 0)
        layoutGB1.addWidget(registrationMethodsCombobox(), 0, 1)
        layoutGB1.addWidget(AlignButton("Registra"), 1, 1)

        group2 = QGroupBox("Modello")
        layoutGB2 = QGridLayout()
        group2.setLayout(layoutGB2)
        layoutGB2.addWidget(LoadModelButton("Carica.."), 0, 0)
        layoutGB2.addWidget(LoadModelButton("Ripristina"), 1, 0)

        self.layout.addWidget(group1, 0, 0)
        self.layout.addWidget(group2, 0, 1)

        self.layout.setColumnStretch(0, 2)
        self.layout.setColumnStretch(1, 1)
        self.layout.setColumnStretch(2, 3)


class bigCell(QWidget):

    def __init__(self, parent, w1, w2):
        super().__init__(parent)
        self.initUI(w1, w2)

    def initUI(self, w1, w2):
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.layout.setColumnStretch(0,3)
        self.layout.setColumnStretch(1,2)
        self.layout.setColumnStretch(2,2)
        self.layout.setColumnStretch(3,3)
        self.layout.addWidget(w1, 0, 1)
        self.layout.addWidget(w2, 0, 2)

class registrationMethodsCombobox(QComboBox):

    def __init__(self):
        super(registrationMethodsCombobox, self).__init__()
        methods = ["ICP", "CPD"]
        self.addItems(methods)

class LoadModelButton(QPushButton):

    def __init__(self, arg):
        super(LoadModelButton, self).__init__(arg)

        self.clicked.connect(self.onClickAction)

    @pyqtSlot()
    def onClickAction(self):
        options = QFileDialog.Options()
        filters = "File MAT (*.mat);;File WRML (*.wrl)"
        fileName, _ = QFileDialog.getOpenFileName(self, "Carica un modello", "",
                                                  filters, "File WRML (*.wrl)", options=options)
        if fileName:
            print(fileName)

class AlignButton(QPushButton):

    def __init__(self, arg):
        super(AlignButton, self).__init__(arg)
