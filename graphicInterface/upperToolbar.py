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
        self.stopBTN.clicked.connect(self.stop_registration)
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
        loadSourceBTN.clicked.connect(self.load_source)
        layoutGB2.addWidget(loadSourceBTN, 0, 0)

        restoreBTN = QPushButton("Restore")
        restoreBTN.clicked.connect(self.restore)
        layoutGB2.addWidget(restoreBTN, 1, 0)

        loadTargetBTN = QPushButton("Load Target")
        loadTargetBTN.clicked.connect(self.load_target)
        layoutGB2.addWidget(loadTargetBTN, 0, 1)

        saveTargetBTN = QPushButton("Save Target")
        saveTargetBTN.clicked.connect(self.save_target)
        layoutGB2.addWidget(saveTargetBTN, 1, 1)

        batchBTN = QPushButton("Batch registration")
        batchBTN.clicked.connect(self.batch_reg)
        layoutGB2.addWidget(batchBTN, 0, 2)

        save_logBTN = QPushButton("Save log on file")
        save_logBTN.clicked.connect(self.savelog_onfile)
        layoutGB2.addWidget(save_logBTN, 1, 2)

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

    def savelog_onfile(self):
        self.parent.savelog_onfile()

    def stop_registration(self):
        self.parent.stop_registration_thread()
        self.registBTN.setEnabled(True)
        self.stopBTN.setEnabled(False)

    def restore(self):
        self.parent.restore_highlight()

    @pyqtSlot()
    def batch_reg(self):
        file_names = self.load_file(multiple_files=True)
        if file_names:
            method = self.registComboBox.currentData()
            percent = self.percComboBox.currentData()
            try:
                self.parent.registrate_batch(method, percent, file_names)
                self.registBTN.setEnabled(False)
                self.stopBTN.setEnabled(True)
            except Exception as ex:
                print(ex)

    @pyqtSlot()
    def load_target(self):
        file_name = self.load_file()

        if file_name:
            self.parent.load_target(file_name)
            self.registBTN.setEnabled(True)

    @pyqtSlot()
    def load_source(self):
        file_name = self.load_file()
        if file_name:
            self.parent.load_source(file_name)
            self.registBTN.setEnabled(True)

    def load_file(self, multiple_files=False):
        dlg = QFileDialog()
        options = dlg.Options()
        options |= QFileDialog.DontUseNativeDialog
        filters = "File MAT (*.mat);;File WRML (*.wrl)"
        if multiple_files:
            file_name, _ = dlg.getOpenFileNames(self, "Load a model", "", filters, "File WRML (*.wrl)", options=options)
        else:
            file_name, _ = dlg.getOpenFileName(self, "Load a model", "", filters, "File WRML (*.wrl)", options=options)

        return file_name

    @pyqtSlot()
    def save_target(self):
        dlg = QFileDialog()
        options = dlg.Options()
        options |= dlg.DontUseNativeDialog
        filters = "MAT File (*.mat);;File (*.*)"
        filename, _ = dlg.getSaveFileName(self, None, "Save model", filter=filters, initialFilter="MAT File (*.mat)",
                                          options=options)
        if filename:
            self.parent.save_target(filename)


class RegistrationMethodsCombobox(QComboBox):

    def __init__(self):
        super(RegistrationMethodsCombobox, self).__init__()
        # self.addItem("ICP", 0)
        self.addItem("CPD - Rigid", 1)
        self.addItem("CPD - Affine", 2)
        self.addItem("CPD - Deformable", 3)



