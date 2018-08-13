from PyQt5.Qt import *


class UpperToolbar(QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        #  Gruppo REGISTRAZIONE
        group1 = QGroupBox("Registrazione")
        layoutGB1 = QGridLayout()
        group1.setLayout(layoutGB1)
        label = QLabel("Metodo di registrazione:")
        label.setAlignment(Qt.AlignCenter)
        layoutGB1.addWidget(label, 0, 0)

        self.registComboBox = RegistrationMethodsCombobox()
        layoutGB1.addWidget(self.registComboBox, 0, 1)

        registBTN = QPushButton("Registra")
        registBTN.clicked.connect(self.registrate)
        layoutGB1.addWidget(registBTN, 1, 1)


        #  Gruppo MODELLO
        group2 = QGroupBox("Modello")
        layoutGB2 = QGridLayout()
        group2.setLayout(layoutGB2)
        layoutGB2.addWidget(LoadModelButton("Carica.."), 0, 0)

        restoreBTN = QPushButton("Ripristina")
        layoutGB2.addWidget(restoreBTN, 1, 0)

        self.layout.addWidget(group1, 0, 0)
        self.layout.addWidget(group2, 0, 1)

        self.layout.setColumnStretch(0, 2)
        self.layout.setColumnStretch(1, 1)
        self.layout.setColumnStretch(2, 3)

    def registrate(self):
        method = self.registComboBox.currentText()
        self.parent().registrate(method)


class RegistrationMethodsCombobox(QComboBox):

    def __init__(self):
        super(RegistrationMethodsCombobox, self).__init__()
        self.addItem("ICP", 1)
        self.addItem("CPD", 2)


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


