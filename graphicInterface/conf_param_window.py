from PyQt5.QtWidgets import QLabel, QMainWindow, QWidget, QGridLayout, QGroupBox, QLineEdit
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QValidator
from graphicInterface.upper_toolbar_controls import ControlPushButton
from pointRegistration.registration_param import RegistrationParameters


class EditConfWindow(QMainWindow):

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setWindowTitle("Edit configuration")
        self.setCentralWidget(ConfEditCentralWidget(self))
        self.resize(400, 200)
        self.show()


class ConfEditCentralWidget(QWidget):

    def __init__(self, parent):
        super(ConfEditCentralWidget, self).__init__(parent=parent)
        general_layout = QGridLayout()
        self.setLayout(general_layout)
        group = QGroupBox("Configuration parameters")
        general_layout.addWidget(group, 0, 0, 1, 6)

        general_layout.addWidget(ControlPushButton("Apply", self.apply_changes), 1, 4, 1, 1)
        general_layout.addWidget(ControlPushButton("Close", self.parent().close), 1, 5, 1, 1)

        layout_conf = QGridLayout()
        group.setLayout(layout_conf)

        layout_conf.addWidget(QLabel("Tolerance"), 0, 0)
        layout_conf.addWidget(QLabel("Max iterations for Local Registration"), 1, 0)
        layout_conf.addWidget(QLabel("Sigma<sup>2<sup>"), 2, 0)
        weight_label = QLabel("Weight <sub><a href=#>?</a></sub>")
        weight_label.setToolTip("Uniform distribution component in GMM for Expectation-Maximizazion step. "
                                "Must be in interval (0,1)")
        layout_conf.addWidget(weight_label, 3, 0)

        self.tolerance_input = ValidatedLineEdit('tolerance', DoubleNoneValidator(0.0000001, 1000, 7))
        layout_conf.addWidget(self.tolerance_input, 0, 1)

        self.max_iterations_input = ValidatedLineEdit('max_iterations', IntValidator(1, 999))
        layout_conf.addWidget(self.max_iterations_input, 1, 1)

        self.sigma_input = ValidatedLineEdit('sigma2', DoubleNoneValidator(0, 1, 6, nullable=True))
        layout_conf.addWidget(self.sigma_input, 2, 1)

        self.weight_input = ValidatedLineEdit('w', DoubleNoneValidator(-0.0000001, 1, 6))
        layout_conf.addWidget(self.weight_input, 3, 1)

        self.inputs = [self.tolerance_input, self.max_iterations_input, self.sigma_input, self.weight_input]

    def apply_changes(self):
        for value_input in self.inputs:
            if value_input.is_valid():
                RegistrationParameters.set_param(value_input.key, value_input.get_value())
            else:
                print(f"Parameter for {value_input.key} is invalid, using previous value.")
        RegistrationParameters.write_on_file()
        self.parent().parent().update_parameter_label()


class ValidatedLineEdit(QLineEdit):

    def __init__(self, key, validator=None):
        super(ValidatedLineEdit, self).__init__()
        self.key = key
        self.setText(str(RegistrationParameters.get_param(key)))
        self.validator = validator

    def get_value(self):
        text = self.text()

        if text.lower().find("none") > -1:
            return None

        return self.validator.type(text)

    def is_valid(self):
        state = self.validator.validate(self.text())
        if state == QValidator.Invalid:
            return False
        return True


class IntValidator(QValidator):

    def __init__(self, bottom, top):
        super(IntValidator, self).__init__()
        self.bottom = bottom
        self.top = top
        self.type = int

    def validate(self, p_str, p_int=None):
        try:
            if self.top > int(p_str) > self.bottom:
                return QValidator.Acceptable
        except ValueError:
            return QValidator.Invalid

        return QValidator.Invalid


class DoubleNoneValidator(QValidator):

    def __init__(self, bottom, top, digits, nullable=False):
        super(DoubleNoneValidator, self).__init__()
        self.bottom = bottom
        self.top = top
        self.digits = digits
        self.type = float
        self.nullable = nullable

    def validate(self, p_str, p_int=None):
        if self.nullable and p_str.lower().find('none') > -1:
            return QValidator.Acceptable
        try:
            if self.top > float(p_str) > self.bottom and len(p_str) <= (self.digits + 2):
                return QValidator.Acceptable
        except ValueError:
            return QValidator.Invalid

        return QValidator.Invalid
