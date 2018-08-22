from graphicInterface.plotFigure import PlotFigure
from graphicInterface.plotInteractiveFigure import PlotInteractiveFigure
from pointRegistration.model import Model
from pointRegistration.registration import Registration
from graphicInterface.upperToolbar import *


class MainWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.source_model = Model("avgModel_bh_1779_NE.mat")
        self.target_model = None
        self.initUI()


    def initUI(self):
        # Griglia centrale con i due plot
        grid_central = QGridLayout(self)
        self.setLayout(grid_central)
        self.sx_widget = PlotInteractiveFigure(self, self.source_model, title="Sorgente")
        self.dx_widget = PlotFigure(self, None, title="Target")
        grid_central.addWidget(self.sx_widget, 1, 0, 1, 2)
        self.sx_widget.drawData()
        grid_central.addWidget(self.dx_widget, 1, 2, 1, 2)
        self.dx_widget.drawData()
        grid_central.addWidget(UpperToolbar(self), 0, 0, 1, 4)
        # Contenitore per i controlli

    def loadTarget(self, path):
        path_bnd = path[0:len(path)-3] + "bnd"
        path_png = path[0:len(path)-7] + "F2D.png"
        self.target_model = Model(path, path_bnd, path_png)
        self.dx_widget.loadModel(self.target_model)
        self.dx_widget.drawData()
        self.parent().notify("File caricato correttamente: " + path)

    def loadSource(self, path):
        path_bnd = path[0:len(path) - 3] + "bnd"
        path_png = path[0:len(path) - 7] + "F2D.png"
        self.source_model = Model(path, path_bnd, path_png)
        self.sx_widget.loadModel(self.source_model)
        self.sx_widget.drawData()
        self.parent().notify("File caricato correttamente: " + path)

    def landmark_selected(self, colors):
        self.dx_widget.setLandmarksColors(colors)
    def registrate(self, method, percentage):
        print("registration with "+str(method)+", using "+str(percentage)+"% of points.")
        self.parent().setStatus("Busy...")
        Registration(method, self.target_model, self.source_model, percentage, self.registrateCallback, self.dx_widget.updatePlotCallback)

    def registrateCallback(self, model):
        print("Registrazione completata")
        #  carica il template deformato
        #  caricalo sul plotFigure widget
        self.target_model = model
        self.target_model.bgImage = self.dx_widget.bgImage
        self.dx_widget.loadModel(self.target_model)
        self.dx_widget.drawData()
        self.parent().setStatusReady()
