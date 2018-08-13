from matplotlib import pyplot
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QSizePolicy


class PlotFigure(FigureCanvas):

    def __init__(self, parent, model=None, landmarks=True, title=None):
        # Creating figure and canvas
        self.fig = Figure(figsize=(5,4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.title = title
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.setParent(parent)
        self.draw_landmarks = landmarks
        if model is not None:
            self.model = model
        #self.drawData()

    def loadData(self):
        #self.ax.plot([0.2, 0.5], [0.2, 0.5])
        self.ax.scatter(self.model.model_data[:, 0], self.model.model_data[:, 1], s=0.5, c="blue")

    def loadLandmarks(self):
        self.ax.scatter(self.model.landmarks_3D[:, 0], self.model.landmarks_3D[:, 1], c="r")

    def drawData(self):
        self.ax.cla()
        if self.title is not None:
            self.ax.set_title(self.title)
        a = self.model.rangeX/2
        b = self.model.rangeY/2
        #print(a, b, a/b)
        #ratio = a/b
        self.ax.set_xlim(-a*1.1, a*1.1) # (-110, 110)
        self.ax.set_ylim(-b*1.1, b*1.1) # (-100, 100)
        self.loadData()
        if self.draw_landmarks:
            self.loadLandmarks()
        if self.model.bgImage is not None:
            img = pyplot.imread(self.model.bgImage)
            # SX DX BOTTOM UP
            self.ax.imshow(img, extent=[-b*1.05, b*1.03, -b*1.03, b*1.05])
        self.draw()

    def setModel(self, model):
        self.model = model

    def landmarks(self, l):
        self.draw_landmarks = l

#m = Model("F0001_NE00WH_F3D.wrl", "F0001_NE00WH_F3D.bnd", "F0001_NE00WH_F2D.png")
#m = Model("M0001_NE00AM_F3D.wrl", "M0001_NE00AM_F3D.bnd", "M0001_NE00AM_F2D.png")
#s = PlotFigure(m)
#s.drawData()



