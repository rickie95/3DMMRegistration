from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from graphicInterface.console import suppress_stdout_stderr
from PyQt5.QtWidgets import QSizePolicy
from matplotlib import pyplot
import numpy as np


class PlotFigure(FigureCanvas):

    def __init__(self, parent, model=None, landmarks=True, title=None):
        self.fig, self.ax = pyplot.subplots()
        self.title = title
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.setParent(parent)
        self.draw_landmarks = landmarks
        self.bgImage = None
        self.model = model
        self.registration_points = np.empty((0, 0))
        self.drawDisplacement = False
        self.landmarks_colors = None
        self.data_colors = None

        if model is not None:
            self.load_model(model)

    def load_model(self, model):
        self.model = model
        self.bgImage = self.model.bgImage
        if self.model.landmarks_3D is not None:
            self.landmarks_colors = np.full(self.model.landmarks_3D.shape[0], "r")
        self.data_colors = np.full(self.model.model_data.shape[0], "b")
        self.drawDisplacement = False

    def load_data(self):
        max_v = np.max(self.model.model_data[:, 2])
        min_v = np.min(self.model.model_data[:, 2])
        sizes = np.copy(self.model.model_data[:, 2])
        self.sizes = ((sizes + np.abs(min_v)) / np.abs(max_v)) + 0.5
        self.ax.scatter(self.model.model_data[:, 0], self.model.model_data[:, 1], self.sizes, c=self.data_colors)

    def load_landmarks(self):
        if self.draw_landmarks and self.model.landmarks_3D is not None:
            max_v = np.max(self.model.landmarks_3D[:, 2])
            min_v = np.min(self.model.landmarks_3D[:, 2])
            sizes = np.copy(self.model.landmarks_3D[:, 2])
            sizes = ((sizes + np.abs(min_v)) / np.abs(max_v)) + 0.5
            self.ax.scatter(self.model.landmarks_3D[:, 0], self.model.landmarks_3D[:, 1], sizes, c=self.landmarks_colors)

    def load_displacement(self):
        self.ax.scatter(self.model.displacement_map[:, 0], self.model.displacement_map[:, 1], s=0.5)

    def load_image(self):
        if self.bgImage is not None:
            img = pyplot.imread(self.bgImage)
            self.ax.imshow(img, extent=[-self.b * 1.05, self.b * 1.03, -self.b * 1.03, self.b * 1.05])  # SX DX BOTTOM UP

    def show_displacement(self):
        self.drawDisplacement = True if self.model.displacement_map is not None else False
        self.draw_landmarks = False

    def draw_data(self):
        self.ax.cla()
        if self.title is not None:
            self.ax.set_title(self.title)
        if self.model is not None:
            self.a = self.model.rangeX / 2
            self.b = self.model.rangeY / 2
            self.ax.set_xlim(-self.a * 1.1, self.a * 1.1)  # (-110, 110)
            self.ax.set_ylim(-self.b * 1.1, self.b * 1.1)  # (-100, 100)
            self.ax.set_xlabel('X axis')
            self.ax.set_ylabel('Y axis')
            if not self.drawDisplacement:
                self.load_data()
            else:
                self.load_displacement()

            self.load_landmarks()
            self.load_image()

        self.draw()
        self.flush_events()

    def restore_model(self):
        self.load_data()
        self.load_landmarks()
        self.load_image()
        self.draw()
        self.flush_events()

    def select_area(self, x_coord, y_coord, width, height):
        x_data = self.model.model_data[:, 0]
        y_data = self.model.model_data[:, 1]

        x_ind = np.where((x_coord <= x_data) & (x_data <= x_coord + width))
        y_ind = np.where((y_coord <= y_data) & (y_data <= y_coord + height))

        ind = np.intersect1d(np.array(x_ind), np.array(y_ind), assume_unique=True)
        self.highlight_data(ind)

    def highlight_data(self, indices):
        if indices[0] != -1:
            self.data_colors[indices] = "y"
            self.model.add_registration_points(indices)
            self.draw_data()
        else:
            self.data_colors[list(range(self.model.model_data.shape[0]))] = "b"
            self.model.add_registration_points([-1])
            self.draw_data()

    def landmarks(self, l):
        self.draw_landmarks = l

    def set_landmarks_colors(self, colors):
        self.landmarks_colors = colors
        self.draw_data()

    def set_data_colors(self, colors):
        self.data_colors = colors
        self.draw_data()

    def get_ax(self):
        return self.ax

    def update_plot_callback(self, iteration, error, X, Y, ax):
        self.ax.cla()
        print(iteration, error)
        self.ax.scatter(Y[:, 0],  Y[:, 1], self.sizes, c='b')
        if self.bgImage is not None:
            img = pyplot.imread(self.bgImage)
            self.ax.imshow(img, extent=[-self.model.rangeY/2 * 1.05, self.model.rangeY/2 * 1.03,
                                        -self.model.rangeY/2 * 1.03, self.model.rangeY/2 * 1.05])
        try:
            self.ax.text(0.87, 0.92, 'Iteration: {:d}\nError: {:06.4f}'.format(iteration, error),
                         horizontalalignment='center', verticalalignment='center', transform=self.ax.transAxes,
                         fontsize='x-large')
        except Exception as ex:
            print(ex)
        with suppress_stdout_stderr():
            self.draw()
        self.flush_events()

