from PyQt5.Qt import *


class UpperToolbar(QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
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

        self.registBTN = QPushButton("Registra")
        self.registBTN.clicked.connect(self.registrate)
        self.registBTN.setEnabled(False)
        layoutGB1.addWidget(self.registBTN, 0, 2)

        label2 = QLabel("Percentuale di punti usati:")
        label2.setAlignment(Qt.AlignCenter)
        layoutGB1.addWidget(label2, 1, 0)

        self.percComboBox = QComboBox()
        for x in range(30, 110, 10):
            self.percComboBox.addItem(str(x) + "%", x)
        layoutGB1.addWidget(self.percComboBox, 1, 1)

        #  Gruppo MODELLO
        group2 = QGroupBox("Modello")
        layoutGB2 = QGridLayout()
        group2.setLayout(layoutGB2)

        loadTargetBTN = QPushButton("Carica Target")
        loadTargetBTN.clicked.connect(self.loadTarget)
        layoutGB2.addWidget(loadTargetBTN, 1, 0)

        loadSourceBTN = QPushButton("Carica Source")
        loadSourceBTN.clicked.connect(self.loadSource)
        layoutGB2.addWidget(loadSourceBTN, 0, 0)

        self.layout.addWidget(group1, 0, 0)
        self.layout.addWidget(group2, 0, 1)

        self.layout.setColumnStretch(0, 2)
        self.layout.setColumnStretch(1, 1)
        self.layout.setColumnStretch(2, 2)

    def registrate(self):
        method = self.registComboBox.currentData()
        percent = self.percComboBox.currentData()
        self.parent.registrate(method, percent)

    @pyqtSlot()
    def loadTarget(self):
        options = QFileDialog.Options()
        filters = "File MAT (*.mat);;File WRML (*.wrl)"
        fileName, _ = QFileDialog.getOpenFileName(self, "Carica un modello", "",
                                                  filters, "File WRML (*.wrl)", options=options)
        if fileName:
            self.parent.loadTarget(fileName)
            self.registBTN.setEnabled(True)

    @pyqtSlot()
    def loadSource(self):
        options = QFileDialog.Options()
        filters = "File MAT (*.mat);;File WRML (*.wrl)"
        fileName, _ = QFileDialog.getOpenFileName(self, "Carica un modello", "",
                                                  filters, "File WRML (*.wrl)", options=options)
        if fileName:
            self.parent.loadSource(fileName)
            self.registBTN.setEnabled(True)


class RegistrationMethodsCombobox(QComboBox):

    def __init__(self):
        super(RegistrationMethodsCombobox, self).__init__()
        #self.addItem("ICP", 0)
        self.addItem("CPD - Rigido", 1)
        self.addItem("CPD - Affine", 2)
        self.addItem("CPD - Deformabile", 3)



