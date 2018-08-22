from graphicInterface.plotFigure import PlotFigure
from scipy import spatial
import numpy as np


class PlotInteractiveFigure(PlotFigure):
    """
            avg_model_data: Nx3 array for 3D point of model
            landmarks_3D: 68x3 array for 3D points of model's landmarks
    """
    def __init__(self,parent, model=None, landmarks=True, title=None):
        super().__init__(parent, model, landmarks, title)
        # Attach event listeners
        self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        # self.fig.canvas.mpl_connect('button_release_event', self.ReleaseClick)
        self.myTree = None


    def loadModel(self, model):
        self.myTree = None
        super().loadModel(model)

    def selectNearestPixel(self, x_coord, y_coord):
        if self.myTree is None:  # calculate kdtree only if is needed
            print("Calculating 2DTree...")
            self.myTree = spatial.cKDTree(self.model.landmarks_3D[:, 0:2])  # costruisce il KDTree con i punti del Model

        dist, index = self.myTree.query([[x_coord, y_coord]], k=1)
        if dist < 5:  # TODO: non sarebbe male normalizzare
            self.landmarks_colors[index[0]] = "y" if self.landmarks_colors[index[0]] == "r" else "r"
            self.drawData()
            if self.parent() is not None:
                self.parent().landmark_selected(self.landmarks_colors)

    def onclick(self, event):
        print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
              ('double' if event.dblclick else 'single', event.button,
               event.x, event.y, event.xdata, event.ydata))
        self.selectNearestPixel(event.xdata, event.ydata)

    def ReleaseClick(self, event):
        print("Released")
        print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
              ('double' if event.dblclick else 'single', event.button,
               event.x, event.y, event.xdata, event.ydata))

    #def loadLandmarks(self):
    #    self.ax.scatter(self.model.landmarks_3D[:, 0], self.model.landmarks_3D[:, 1], c=self.landmarks_colors)
