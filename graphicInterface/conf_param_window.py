from PyQt5.QtWidgets import QLabel, QMainWindow, QWidget, QGridLayout, QGroupBox, QLineEdit
from PyQt5.QtGui import QIntValidator, QDoubleValidator


class EditConfWindow(QMainWindow):

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setWindowTitle("Edit configuration")
        self.setCentralWidget(ConfEditCentralWidget())
        self.resize(400, 200)
        self.show()


class ConfEditCentralWidget(QWidget):

    def __init__(self):
        super(ConfEditCentralWidget, self).__init__()
        general_layout = QGridLayout()
        self.setLayout(general_layout)
        group = QGroupBox("Configuration parameters")
        general_layout.addWidget(group)
        layout_conf = QGridLayout()
        group.setLayout(layout_conf)

        layout_conf.addWidget(QLabel("Tolerance"), 0, 0)
        layout_conf.addWidget(QLabel("Max iterations for Local Registration"), 1, 0)
        layout_conf.addWidget(QLabel("Sigma^2"), 2, 0)
        layout_conf.addWidget(QLabel("Weight for uniform distribution component in GMM for Expectation-Maximizazion "
                                     "step: w in (0,1)"), 3, 0)

        self.tolerance_input = ValidatedLineEdit(QDoubleValidator(1000, 0.0000001, 7))
        layout_conf.addWidget(self.tolerance_input, 0, 1)
        self.max_iterations_input = ValidatedLineEdit(QIntValidator(1, 999))
        layout_conf.addWidget(self.max_iterations_input, 1, 1)
        self.sigma_input = ValidatedLineEdit(QDoubleValidator(0, 1, 6))  #fixme check if input range is ok
        layout_conf.addWidget(self.sigma_input, 2, 1)
        self.weight_input = ValidatedLineEdit(QDoubleValidator(0, 1, 6))
        layout_conf.addWidget(self.weight_input, 3, 1)


class ValidatedLineEdit(QLineEdit):

    def __init__(self, validator=None):
        super(ValidatedLineEdit, self).__init__()
        if validator is not None:
            self.setValidator(validator)

    def get_value(self):
        return self.text()