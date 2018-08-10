from PyQt5.QtWidgets import (QApplication, QWidget,QDesktopWidget, QMainWindow,
                             QGridLayout, QPushButton, QLabel, QComboBox)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from plotFigure import PlotFigure
from plotInteractiveFigure import PlotInteractiveFigure
from model import Model
import sys


class Window(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.mainWidget = MainWidget(self)
        self.setCentralWidget(self.mainWidget)
        self.resize(1000, 600)
        self.center()
        self.setWindowTitle('Shape Registrator')
        self.statusBar().showMessage("Ready.")
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


# CLASSE MAIN WIDGET: organizza il layout della finestra e contiene i due plotWidget, bottoni ed altro
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
        grid_central.addWidget(sx_widget, 0, 0, 1, 2)
        sx_widget.drawData()
        grid_central.addWidget(dx_widget, 0, 2, 1, 2)
        dx_widget.drawData()
        #grid_central.addWidget(QLabel("Metodo di registrazione:"), 1, 0)
        #grid_central.addWidget(QComboBox(self), 1, 1)
        #grid_central.addWidget(QLabel("Modello da caricare:"), 1, 2)
        # Contenitore per i controlli


if __name__ == "__main__":

    app = QApplication(sys.argv)

    w = Window()

    sys.exit(app.exec_())
