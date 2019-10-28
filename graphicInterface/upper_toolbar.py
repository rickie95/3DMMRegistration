from graphicInterface.file_dialogs import *
from PyQt5.Qt import *
from graphicInterface.console import Logger
from graphicInterface.upper_toolbar_controls import *


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

        self.start_registration_button = ControlPushButton("Start Registration", self.registrate, False)
        registration_group_layout.addWidget(self.start_registration_button, 0, 2)

        self.stop_registration_button = ControlPushButton("Stop", self.stop_registration, False)
        registration_group_layout.addWidget(self.stop_registration_button, 1, 2)

        point_percentage_label = QLabel("Target's points used:")
        point_percentage_label.setAlignment(Qt.AlignCenter)
        registration_group_layout.addWidget(point_percentage_label, 1, 0)

        self.point_percentage_combobox = PercentageComboBox()
        registration_group_layout.addWidget(self.point_percentage_combobox, 1, 1)

        #  "Model" group
        model_group = QGroupBox("Models")
        model_group_layout = QGridLayout()
        model_group.setLayout(model_group_layout)

        model_group_layout.addWidget(ControlPushButton("Load Source", self.load_source, True), 0, 0)
        model_group_layout.addWidget(ControlPushButton("Restore", self.restore, True), 1, 0)
        model_group_layout.addWidget(ControlPushButton("Load Target", self.load_target, True), 0, 1)

        self.save_target_btn = ControlPushButton("Save Target", self.save_target, False)
        model_group_layout.addWidget(self.save_target_btn, 1, 1)

        model_group_layout.addWidget(ControlPushButton("Batch registration", self.batch_reg, False), 0, 2)

        self.show_displacement_btn = ControlPushButton("Show Displacement Map", self.show_displacement, True)
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
        self.parent.load_target()

    @pyqtSlot()
    def load_source(self):
        self.parent.load_source()

    @pyqtSlot()
    def save_target(self):
        self.parent.save_target()
