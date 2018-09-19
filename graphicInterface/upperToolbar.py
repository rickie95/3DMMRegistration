from PyQt5.Qt import *
from graphicInterface.console import Logger


class UpperToolbar(QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        #  Gruppo REGISTRAZIONE
        group1 = QGroupBox("Registration")
        layoutGB1 = QGridLayout()
        group1.setLayout(layoutGB1)
        label = QLabel("Registration method:")
        label.setAlignment(Qt.AlignCenter)
        layoutGB1.addWidget(label, 0, 0)

        self.registComboBox = RegistrationMethodsCombobox()
        layoutGB1.addWidget(self.registComboBox, 0, 1)

        self.registBTN = QPushButton("Register")
        self.registBTN.clicked.connect(self.registrate)
        self.registBTN.setEnabled(False)
        layoutGB1.addWidget(self.registBTN, 0, 2)

        self.stopBTN = QPushButton("Stop")
        self.stopBTN.clicked.connect(self.stopRegistration)
        self.stopBTN.setEnabled(False)
        layoutGB1.addWidget(self.stopBTN, 1, 2)

        label2 = QLabel("Percentage of points used:")
        label2.setAlignment(Qt.AlignCenter)
        layoutGB1.addWidget(label2, 1, 0)

        self.percComboBox = QComboBox()
        for x in range(100, 20, -10):
            self.percComboBox.addItem(str(x) + "%", x)
        layoutGB1.addWidget(self.percComboBox, 1, 1)

        #  Gruppo MODELLO
        group2 = QGroupBox("Models")
        layoutGB2 = QGridLayout()
        group2.setLayout(layoutGB2)

        loadSourceBTN = QPushButton("Load Source")
        loadSourceBTN.clicked.connect(self.loadSource)
        layoutGB2.addWidget(loadSourceBTN, 0, 0)

        restoreBTN = QPushButton("Restore")
        restoreBTN.clicked.connect(self.restore)
        layoutGB2.addWidget(restoreBTN, 1, 0)

        loadTargetBTN = QPushButton("Load Target")
        loadTargetBTN.clicked.connect(self.loadTarget)
        layoutGB2.addWidget(loadTargetBTN, 0, 1)

        saveTargetBTN = QPushButton("Save Target")
        saveTargetBTN.clicked.connect(self.saveTarget)
        layoutGB2.addWidget(saveTargetBTN, 1, 1)

        batchBTN = QPushButton("Batch registration")
        batchBTN.clicked.connect(self.batchReg)
        layoutGB2.addWidget(batchBTN, 0, 2)

        #  LOGGER GROUP
        group3 = QGroupBox("Log")
        layoutGB3 = QGridLayout()
        group3.setLayout(layoutGB3)

        layoutGB3.addWidget(Logger.instance)

        self.layout.addWidget(group1, 0, 0)
        self.layout.addWidget(group2, 0, 1)
        self.layout.addWidget(group3, 0, 2)

        self.layout.setColumnStretch(0, 2)
        self.layout.setColumnStretch(1, 1)
        self.layout.setColumnStretch(2, 4)


    def registrate(self):
        method = self.registComboBox.currentData()
        percent = self.percComboBox.currentData()
        try:
            self.parent.registrate(method, percent)
            self.registBTN.setEnabled(False)
            self.stopBTN.setEnabled(True)
        except Exception as ex:
            print(ex)

    @pyqtSlot()
    def batchReg(self):
        options = QFileDialog.Options()
        filters = "File MAT (*.mat);;File WRML (*.wrl)"
        fileNames, _ = QFileDialog.getOpenFileNames(self, "Load a model", "",
                                                  filters, "File WRML (*.wrl)", options=options)
        if fileNames:
            method = self.registComboBox.currentData()
            percent = self.percComboBox.currentData()
            try:
                self.parent.registrate_batch(method, percent, fileNames)
                self.registBTN.setEnabled(False)
                self.stopBTN.setEnabled(True)
            except Exception as ex:
                print(ex)


    def stopRegistration(self):
        self.parent.stopRegistrationThread()
        self.registBTN.setEnabled(True)  # sarebbe da riabilitare successivamente
        self.stopBTN.setEnabled(False)

    def restore(self):
        self.parent.restoreHighlight()

    @pyqtSlot()
    def loadTarget(self):
        options = QFileDialog.Options()
        filters = "File MAT (*.mat);;File WRML (*.wrl)"
        fileName, _ = QFileDialog.getOpenFileName(self, "Load a model", "",
                                                  filters, "File WRML (*.wrl)", options=options)
        if fileName:
            self.parent.loadTarget(fileName)
            self.registBTN.setEnabled(True)

    @pyqtSlot()
    def loadSource(self):
        options = QFileDialog.Options()
        filters = "File MAT (*.mat);;File WRML (*.wrl)"
        fileName, _ = QFileDialog.getOpenFileName(self, "Load a model", "",
                                                  filters, "File WRML (*.wrl)", options=options)
        if fileName:
            self.parent.loadSource(fileName)
            self.registBTN.setEnabled(True)

    @pyqtSlot()
    def saveTarget(self):
        options = QFileDialog.Options()
        filters = "MAT File (*.mat);;File (*.*)"
        filename, _ = QFileDialog.getSaveFileName(self, None, "Save model", filter=filters,
                                    initialFilter="MAT File (*.mat)", options=options)
        if filename:
            self.parent.saveTarget(filename)


class RegistrationMethodsCombobox(QComboBox):

    def __init__(self):
        super(RegistrationMethodsCombobox, self).__init__()
        #self.addItem("ICP", 0)
        self.addItem("CPD - Rigid", 1)
        self.addItem("CPD - Affine", 2)
        self.addItem("CPD - Deformable", 3)



