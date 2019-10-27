from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QPushButton
from graphicInterface.rotatable_figure import RotatableFigure
from graphicInterface.upper_toolbar_controls import ControlPushButton
from graphicInterface.file_dialogs import *


class DisplacementMapWindow(QMainWindow):

    def __init__(self, parent, model):
        super().__init__(parent=parent)
        self.setWindowIcon(QIcon('resources/icon.png'))
        self.statusLabel = QLabel("Ready")
        self.setWindowTitle("Displacement Map")
        self.model = model
        self.rot_figure = None
        self.initUI()

    def initUI(self):
        central_widget = QWidget(self)
        grid_central = QGridLayout(self)
        central_widget.setLayout(grid_central)
        self.setCentralWidget(central_widget)
        self.setLayout(grid_central)
        self.rot_figure = RotatableFigure(parent=self, model=self.model, title="Displacement Map")
        self.toolbar = LowerToolbar(self)
        grid_central.addWidget(self.rot_figure, 0, 0, 19, 1)
        grid_central.addWidget(self.toolbar, 20, 0, 1, 1)
        if self.model is not None:
            self.toolbar.save_button.setEnabled(True)
        self.resize(600, 600)
        self.rot_figure.draw_data(clear=True)
        self.show()

    def save_displacement_map(self):
        filters = "Serialized Python Obj (*.pickle);;H5Py Compatible file (*.h5py)"
        filename = save_file_dialog(self, filters)
        if filename is not None:
            self.model.save_model(filename)

    def load_displacement_map(self):
        filters = "H5Py Compatible file (*.h5py)"
        filename = load_file_dialog(self, filters)
        if filename is not None:
            from pointRegistration.displacementMap import DisplacementMap
            self.model = DisplacementMap.load_model(filename)
            self.rot_figure.load_model(self.model)
            self.rot_figure.draw_data()
            self.toolbar.save_button.setEnabled(True)


class LowerToolbar(QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.save_button = ControlPushButton("Save on file", self.parent.save_displacement_map, False)
        load_button = ControlPushButton("Load from file..", self.parent.load_displacement_map)
        self.layout.addWidget(self.save_button, 0, 1, 1, 1)
        self.layout.addWidget(load_button, 0, 3, 1, 1)