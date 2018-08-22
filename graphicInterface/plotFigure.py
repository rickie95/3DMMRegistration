from matplotlib import pyplot
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QSizePolicy
import numpy as np
import time

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
        self.bgImage = None
        self.model = model

        if model is not None:
            self.loadModel(model)

    def loadModel(self, model):
        self.model = model
        self.bgImage = self.model.bgImage
        sz = int(self.model.landmarks_3D.size / 3)
        self.landmarks_colors = np.full(sz, "r")

    def loadData(self):
        #self.ax.plot([0.2, 0.5], [0.2, 0.5])
        self.ax.scatter(self.model.model_data[:, 0], self.model.model_data[:, 1], s=0.5, c="blue")

    def loadLandmarks(self):
        self.ax.scatter(self.model.landmarks_3D[:, 0], self.model.landmarks_3D[:, 1], c=self.landmarks_colors)

    def drawData(self):
        self.ax.cla()
        if self.title is not None:
            self.ax.set_title(self.title)
        if self.model is not None:
            a = self.model.rangeX/2
            b = self.model.rangeY/2
            #print(a, b, a/b)
            #ratio = a/b
            self.ax.set_xlim(-a*1.1, a*1.1) # (-110, 110)
            self.ax.set_ylim(-b*1.1, b*1.1) # (-100, 100)
            self.loadData()
            if self.draw_landmarks:
                self.loadLandmarks()
            if self.bgImage is not None:
                img = pyplot.imread(self.bgImage)
                # SX DX BOTTOM UP
                self.ax.imshow(img, extent=[-b*1.05, b*1.03, -b*1.03, b*1.05])
        self.draw()

    #def setModel(self, model):
    #    self.model = model
    #    self.bgImage = self.model.bgImage

    def landmarks(self, l):
        self.draw_landmarks = l

    def setLandmarksColors(self, colors):
        self.landmarks_colors = colors
        self.drawData()

    def updatePlotCallback(self, iteration, error, X, Y, ax):
        self.ax.cla()
        print(iteration, error)
        self.ax.scatter(Y[:,0],  Y[:,1], Y[:,2], c='b')
        if self.bgImage is not None:
            img = pyplot.imread(self.bgImage)
            # SX DX BOTTOM UP
            self.ax.imshow(img, extent=[-self.model.rangeY/2 * 1.05, self.model.rangeY/2 * 1.03, -self.model.rangeY/2* 1.03, self.model.rangeY/2 * 1.05])
        try:
            self.ax.text(0.87, 0.92, 'Iteration: {:d}\nError: {:06.4f}'.format(iteration, error),
                    horizontalalignment='center', verticalalignment='center', transform=self.ax.transAxes,
                    fontsize='x-large')
        except Exception as ex:
            print(ex)
        self.draw()
        self.flush_events()

#m = Model("F0001_NE00WH_F3D.wrl", "F0001_NE00WH_F3D.bnd", "F0001_NE00WH_F2D.png")
#m = Model("M0001_NE00AM_F3D.wrl", "M0001_NE00AM_F3D.bnd", "M0001_NE00AM_F2D.png")
#s = PlotFigure(m)
#s.drawData()



