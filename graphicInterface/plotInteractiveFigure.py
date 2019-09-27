
from graphicInterface.plotFigure import PlotFigure
from matplotlib.widgets import RectangleSelector
import matplotlib.patches as patches
from scipy import spatial
import numpy as np


class PlotInteractiveFigure(PlotFigure):

    def __init__(self, parent, model=None, landmarks=True, title=None):
        super().__init__(parent, model, landmarks, title)
        self.myTree = None
        self.RS = RectangleSelector(self.ax, self.square_select_callback, drawtype='box', useblit=True, button=[1, 3],
                                    minspanx=5, minspany=5, spancoords='pixels', interactive=True)

    def load_model(self, model):
        self.myTree = None
        super().load_model(model)

    def select_nearest_pixel(self, x_coord, y_coord):
        if self.myTree is None:  # calculate kdtree only if is needed
            print("Calculating 2DTree...")
            self.myTree = spatial.cKDTree(self.model.landmarks_3D[:, 0:2])  # costruisce il KDTree con i punti del Model

        dist, index = self.myTree.query([[x_coord, y_coord]], k=1)
        if dist < 5:  # fixme: there should be some normalization mechanism
            self.landmarks_colors[index[0]] = "y" if self.landmarks_colors[index[0]] == "r" else "r"
            self.draw_data()
            print(index)
            if self.parent() is not None:
                self.parent().landmark_selected(self.landmarks_colors)

    def square_select_callback(self, eclick, erelease):
        # eclick and erelease are the press and release events
        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata
        rect = patches.Rectangle((min(x1, x2), min(y1, y2)), np.abs(x1 - x2), np.abs(y1 - y2),
                                 linewidth=1, edgecolor='r', facecolor='none', fill=True)
        self.get_ax().add_patch(rect)
        self.select_area(min(x1, x2), min(y1, y2), np.abs(x1 - x2), np.abs(y1 - y2))
        self.draw()

    def there_are_points_highlighted(self):
        if self.model.registration_points.shape[0] > 0:
            return True

        return False
