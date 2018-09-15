from graphicInterface.plotFigure import PlotFigure
from matplotlib.widgets import RectangleSelector
import matplotlib.patches as patches
from scipy import spatial
import numpy as np


class PlotInteractiveFigure(PlotFigure):
    """
            avg_model_data: Nx3 array for 3D point of model
            landmarks_3D: 68x3 array for 3D points of model's landmarks
    """
    def __init__(self,parent, model=None, landmarks=True, title=None):
        super().__init__(parent, model, landmarks, title)

        #self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        # self.fig.canvas.mpl_connect('button_release_event', self.ReleaseClick)
        self.myTree = None

        # Attach event listener
        self.RS = RectangleSelector(self.ax, self.square_select_callback, drawtype='box', useblit=True, button=[1, 3],
                                    minspanx=5, minspany=5, spancoords='pixels', interactive=True)

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
            print(index)
            if self.parent() is not None:
                self.parent().landmark_selected(self.landmarks_colors)

    #def onclick(self, event):
    #    print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
    #          ('double' if event.dblclick else 'single', event.button,
    #           event.x, event.y, event.xdata, event.ydata))
    #    self.selectNearestPixel(event.xdata, event.ydata)

    #def ReleaseClick(self, event):
    #    print("Released")
    #    print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
    #          ('double' if event.dblclick else 'single', event.button,
    #           event.x, event.y, event.xdata, event.ydata))

    def square_select_callback(self, eclick, erelease):
        'eclick and erelease are the press and release events'
        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata
        # print("(%3.2f, %3.2f) --> (%3.2f, %3.2f)" % (x1, y1, x2, y2))
        # print(" The button you used were: %s %s" % (eclick.button, erelease.button))
        rect = patches.Rectangle((min(x1, x2), min(y1, y2)), np.abs(x1 - x2), np.abs(y1 - y2),linewidth=1,edgecolor='r',facecolor='none', fill=True)
        self.get_ax().add_patch(rect)
        self.select_area(min(x1, x2), min(y1, y2), np.abs(x1 - x2), np.abs(y1 - y2))
        self.draw()

    def there_are_points_highlighted(self):
        if self.model.registration_points.shape[0] > 0:
            return True

        return False
