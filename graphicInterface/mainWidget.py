from PyQt5.QtWidgets import (QWidget, QGridLayout, QLabel, QComboBox)
from plotFigure import PlotFigure
from plotInteractiveFigure import PlotInteractiveFigure
from model import Model
from graphicInterface.upperToolbar import *


class MainWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        # Griglia centrale con i due plot
        grid_central = QGridLayout()
        self.setLayout(grid_central)
        sx_widget = PlotInteractiveFigure(self, Model("avgModel_bh_1779_NE.mat"), title="Template")
        dx_widget = PlotFigure(self, Model("M0001_NE00AM_F3D.wrl", "M0001_NE00AM_F3D.bnd", "M0001_NE00AM_F2D.png"), title="Face Model")
        grid_central.addWidget(sx_widget, 1, 0, 1, 2)
        sx_widget.drawData()
        grid_central.addWidget(dx_widget, 1, 2, 1, 2)
        dx_widget.drawData()
        grid_central.addWidget(UpperToolbar(self), 0, 0, 1, 4 )
        # Contenitore per i controlli