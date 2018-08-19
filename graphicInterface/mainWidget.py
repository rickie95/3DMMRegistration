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
        sx_widget = PlotInteractiveFigure(self, self.source_model, title="Template")
        self.dx_widget = PlotFigure(self, None, title="Face Model")
        grid_central.addWidget(sx_widget, 1, 0, 1, 2)
        sx_widget.drawData()
        grid_central.addWidget(self.dx_widget, 1, 2, 1, 2)
        self.dx_widget.drawData()
        grid_central.addWidget(UpperToolbar(self), 0, 0, 1, 4)
        # Contenitore per i controlli

    def loadTarget(self, path):
        path_bnd = path[0:len(path)-3] + "bnd"
        path_png = path[0:len(path)-3] + "png"
        self.target_model = Model(path, path_bnd, path_png)
        self.dx_widget.loadModel(self.target_model)
        self.dx_widget.drawData()
        self.parent().notify("File caricato correttamente: " + path)

    def registrate(self, method, percentage):
        print("registration with "+str(method)+", using "+str(percentage)+"% of points.")
        self.parent().setStatus("Busy...")
        Registration(method, self.source_model, self.target_model, percentage, self.registrateCallback)

    def registrateCallback(self, model):
        print("Registrazione completata")
        #  carica il template deformato
        #  caricalo sul plotFigure widget
        self.target_model = model
        self.dx_widget.loadModel(self.target_model)
        self.dx_widget.drawData()
        self.parent().setStatusReady()
