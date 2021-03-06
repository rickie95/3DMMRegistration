import matplotlib.patches as patches
import numpy as np
from matplotlib.widgets import RectangleSelector
from scipy import spatial

from graphicInterface.console import suppress_stdout_stderr
from graphicInterface.plot_figure import PlotFigure


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
        if self.myTree is None:
            print("Calculating 2DTree...")
            self.myTree = spatial.cKDTree(self.model.landmarks_3D[:, 0:2])  # costruisce il KDTree con i punti del Model

        dist, index = self.myTree.query([[x_coord, y_coord]], k=1)
        if dist < 5:
            self.landmarks_colors[index[0]] = "y" if self.landmarks_colors[index[0]] == "r" else "r"
            self.draw()
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
        return self.model.has_registration_points()

    def select_area(self, x_coord, y_coord, width, height):
        with suppress_stdout_stderr():
            x_data = self.model.points[:, 0]
            y_data = self.model.points[:, 1]

            x_ind = np.where((x_coord <= x_data) & (x_data <= x_coord + width))
            y_ind = np.where((y_coord <= y_data) & (y_data <= y_coord + height))

            ind = np.intersect1d(np.array(x_ind), np.array(y_ind), assume_unique=True)
            self.highlight_data(ind)

    def highlight_data(self, indices):
        if indices[0] != -1:
            self.model.add_registration_points(indices)
            self.draw_data()
        else:
            self.model.init_registration_points()
            self.draw_data()
