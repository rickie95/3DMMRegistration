from graphicInterface.plotFigure import PlotFigure
from graphicInterface.plotInteractiveFigure import PlotInteractiveFigure
from pointRegistration.model import Model
from pointRegistration.registration import Registration
from graphicInterface.upperToolbar import *
from graphicInterface.console import Logger


class MainWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        Logger.addRow(str("Starting up.."))
        self.source_model = Model("avgModel_bh_1779_NE.mat")
        self.target_model = None
        self.initUI()
        self.registration_thread = None
        Logger.addRow(str("Ready."))

    def initUI(self):
        # Griglia centrale con i due plot
        grid_central = QGridLayout(self)
        self.setLayout(grid_central)
        self.sx_widget = PlotInteractiveFigure(self, self.source_model, title="Source")
        self.dx_widget = PlotFigure(self, None, title="Target")
        grid_central.addWidget(self.sx_widget, 1, 0, 1, 2)
        self.sx_widget.drawData()
        grid_central.addWidget(self.dx_widget, 1, 2, 1, 2)
        self.dx_widget.drawData()
        self.toolbar = UpperToolbar(self)
        grid_central.addWidget(self.toolbar, 0, 0, 1, 4)
        grid_central.setRowStretch(0, 1)
        grid_central.setRowStretch(1, 10)
        # Contenitore per i controlli

    def loadTarget(self, path):
        path_bnd = path[0:len(path)-3] + "bnd"
        path_png = path[0:len(path)-7] + "F2D.png"
        self.target_model = Model(path, path_bnd, path_png)
        self.dx_widget.loadModel(self.target_model)
        self.dx_widget.drawData()
        Logger.addRow(str("File loaded correctly: " + path))

    def loadSource(self, path):
        path_bnd = path[0:len(path) - 3] + "bnd"
        path_png = path[0:len(path) - 7] + "F2D.png"
        self.source_model = Model(path, path_bnd, path_png)
        self.sx_widget.loadModel(self.source_model)
        self.sx_widget.drawData()
        Logger.addRow(str("File loaded correctly: " + path))

    def landmark_selected(self, colors):
        self.dx_widget.setLandmarksColors(colors)

    def registrate(self, method, percentage):
        if self.registration_thread is None:
            self.parent().setStatus("Busy...")
            self.registration_thread = Registration(method, self.target_model, self.source_model, percentage, self.registrateCallback, self.dx_widget.updatePlotCallback)
            self.registration_thread.start()

    def stopRegistrationThread(self):
        if self.registration_thread is not None:
            Logger.addRow(str("Trying to stop registration thread..."))
            self.registration_thread.stop()

    def registrateCallback(self, model):
        Logger.addRow(str("Registration completed."))
        self.target_model = model
        self.target_model.bgImage = self.dx_widget.bgImage
        self.dx_widget.loadModel(self.target_model)
        self.dx_widget.setLandmarksColors(self.sx_widget.landmarks_colors)
        self.dx_widget.drawData()
        self.parent().setStatusReady()
        self.registration_thread = None
        self.toolbar.registBTN.setEnabled(True)
        self.toolbar.stopBTN.setEnabled(False)
