from PyQt5.Qt import *
from graphicInterface.console import Logger


class UpperToolbar(QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        #  "Registration" group
        registration_group = QGroupBox("Registration")
        registration_group_layout = QGridLayout()
        registration_group.setLayout(registration_group_layout)
        label = QLabel("Registration method:")
        label.setAlignment(Qt.AlignCenter)
        registration_group_layout.addWidget(label, 0, 0)

        self.registration_method_combobox = RegistrationMethodsCombobox()
        registration_group_layout.addWidget(self.registration_method_combobox, 0, 1)

        self.start_registration_button = QPushButton("Register")
        self.start_registration_button.clicked.connect(self.registrate)
        self.start_registration_button.setEnabled(False)
        registration_group_layout.addWidget(self.start_registration_button, 0, 2)

        self.stop_registration_button = QPushButton("Stop")
        self.stop_registration_button.clicked.connect(self.stop_registration)
        self.stop_registration_button.setEnabled(False)
        registration_group_layout.addWidget(self.stop_registration_button, 1, 2)

        point_percentage_label = QLabel("Percentage of points used:")
        point_percentage_label.setAlignment(Qt.AlignCenter)
        registration_group_layout.addWidget(point_percentage_label, 1, 0)

        self.point_percentage_combobox = QComboBox()
        for x in range(100, 20, -10):
            self.point_percentage_combobox.addItem(str(x) + "%", x)
        registration_group_layout.addWidget(self.point_percentage_combobox, 1, 1)

        #  "Model" group
        model_group = QGroupBox("Models")
        model_group_layout = QGridLayout()
        model_group.setLayout(model_group_layout)

        load_source_btn = QPushButton("Load Source")
        load_source_btn.clicked.connect(self.load_source)
        model_group_layout.addWidget(load_source_btn, 0, 0)

        restore_btn = QPushButton("Restore")
        restore_btn.clicked.connect(self.restore)
        model_group_layout.addWidget(restore_btn, 1, 0)

        load_target_btn = QPushButton("Load Target")
        load_target_btn.clicked.connect(self.load_target)
        model_group_layout.addWidget(load_target_btn, 0, 1)

        self.save_target_btn = QPushButton("Save Target")
        self.save_target_btn.clicked.connect(self.save_target)
        self.save_target_btn.setEnabled(False)
        model_group_layout.addWidget(self.save_target_btn, 1, 1)

        batch_btn = QPushButton("Batch registration")
        batch_btn.clicked.connect(self.batch_reg)
        model_group_layout.addWidget(batch_btn, 0, 2)

        self.show_displacement_btn = QPushButton("Show displacement map")
        self.show_displacement_btn.clicked.connect(self.show_displacement)
        self.show_displacement_btn.setEnabled(False)
        model_group_layout.addWidget(self.show_displacement_btn, 1, 2)

        #  LOGGER GROUP
        logger_group = QGroupBox("Log")
        logger_group_layout = QGridLayout()
        logger_group.setLayout(logger_group_layout)

        save_log_btn = QPushButton("Save log on file")
        save_log_btn.clicked.connect(self.savelog_onfile)
        logger_group_layout.addWidget(Logger.instance)
        logger_group_layout.addWidget(save_log_btn)

        self.layout.addWidget(registration_group, 0, 0)
        self.layout.addWidget(model_group, 0, 1)
        self.layout.addWidget(logger_group, 0, 2)

        self.layout.setColumnStretch(0, 2)
        self.layout.setColumnStretch(1, 1)
        self.layout.setColumnStretch(2, 4)

    def registrate(self):
        method = self.registration_method_combobox.currentData()
        percent = self.point_percentage_combobox.currentData()
        try:
            self.parent.registrate(method, percent)
            self.start_registration_button.setEnabled(False)
            self.stop_registration_button.setEnabled(True)
        except Exception as ex:
            print(ex)

    def show_displacement(self):
        self.parent.show_displacement_map()

    def savelog_onfile(self):
        self.parent.savelog_onfile()

    def stop_registration(self):
        self.parent.stop_registration_thread()
        self.stop_registration_button.setEnabled(False)

    def restore(self):
        self.parent.restore()

    @pyqtSlot()
    def batch_reg(self):
        file_names = self.load_file(multiple_files=True)
        if file_names:
            method = self.registration_method_combobox.currentData()
            percent = self.point_percentage_combobox.currentData()
            try:
                self.parent.registrate_batch(method, percent, file_names)
                self.start_registration_button.setEnabled(False)
                self.stop_registration_button.setEnabled(True)
            except Exception as ex:
                print(ex)

    @pyqtSlot()
    def load_target(self):
        file_name = self.load_file()

        if file_name:
            self.parent.load_target(file_name)
            self.start_registration_button.setEnabled(True)

    @pyqtSlot()
    def load_source(self):
        file_name = self.load_file()
        if file_name:
            self.parent.load_source(file_name)
            self.start_registration_button.setEnabled(True)

    def load_file(self, multiple_files=False):
        dlg = QFileDialog()
        options = dlg.Options()
        options |= QFileDialog.DontUseNativeDialog
        filters = "MAT File(*.mat);;WRML File (*.wrl);;OFF File (*.off)"
        if multiple_files:
            file_name, _ = dlg.getOpenFileNames(self, "Load a model", "", filters, "File WRML (*.wrl)", options=options)
        else:
            file_name, _ = dlg.getOpenFileName(self, "Load a model", "", filters, "File WRML (*.wrl)", options=options)

        return file_name

    @pyqtSlot()
    def save_target(self):
        self.parent.save_target()


class RegistrationMethodsCombobox(QComboBox):

    def __init__(self):
        super(RegistrationMethodsCombobox, self).__init__()
        # self.addItem("ICP", 0)
        self.addItem("CPD - Rigid", 1)
        self.addItem("CPD - Affine", 2)
        self.addItem("CPD - Deformable", 3)



