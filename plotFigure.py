from matplotlib import pyplot
from model import Model


class PlotFigure:

    def __init__(self, model=None, landmarks=True):
        # Creating figure and canvas
        self.fig, self.ax = pyplot.subplots()
        self.draw_landmarks = landmarks
        if model is not None:
            self.model = model

    def loadData(self):
        self.ax.scatter(self.model.model_data[:, 0], self.model.model_data[:, 1], s=0.5, c="blue")

    def loadLandmarks(self):
        self.ax.scatter(self.model.landmarks_3D[:, 0], self.model.landmarks_3D[:, 1], c="r")

    def drawData(self):
        pyplot.cla()
        a = 93
        b = -93
        pyplot.xlim(b, a) # (-110, 110)
        pyplot.ylim(b, a) # (-100, 100)
        self.loadData()
        if self.draw_landmarks:
            self.loadLandmarks()
        if self.model.bgImage is not None:
            img = pyplot.imread(self.model.bgImage)
            self.ax.imshow(img, extent=[b, a, b, a])
        pyplot.show()

    def setModel(self, model):
        self.model = model

    def landmarks(self, l):
        self.draw_landmarks = l



print("")
m = Model("F0001_NE00WH_F3D.wrl", "F0001_NE00WH_F3D.bnd", "F0001_NE00WH_F2D.png")
s = PlotFigure(m)
s.drawData()



