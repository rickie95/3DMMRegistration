from PyQt5.QtWidgets import QPushButton, QComboBox


class ControlPushButton(QPushButton):

    def __init__(self, text="Button", callback=None, enabled=True):
        super().__init__(text)
        self.clicked.connect(callback)
        self.setEnabled(enabled)


class PercentageComboBox(QComboBox):

    def __init__(self, ):
        super().__init__()
        for x in range(100, 20, -10):
            self.addItem(str(x) + "%", x)


class RegistrationMethodsCombobox(QComboBox):

    def __init__(self):
        super(RegistrationMethodsCombobox, self).__init__()
        # self.addItem("ICP", 0)
        self.addItem("CPD - Rigid", 1)
        self.addItem("CPD - Affine", 2)
        self.addItem("CPD - Deformable", 3)
