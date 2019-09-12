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
        # self.ax.plot([0.2, 0.5], [0.2, 0.5])
        self.ax.scatter(self.model.model_data[:, 0], self.model.model_data[:, 1], s=0.5, c=self.data_colors)

    def load_landmarks(self):
        self.ax.scatter(self.model.landmarks_3D[:, 0], self.model.landmarks_3D[:, 1], c=self.landmarks_colors)

    def load_displacement(self):
        self.ax.scatter(self.model.displacement_map[:, 0], self.model.displacement_map[:, 1], s=0.5)

    def show_displacement(self):
        self.drawDisplacement = True if self.model.displacement_map is not None else False

    def draw_data(self):
        self.ax.cla()
        if self.title is not None:
            self.ax.set_title(self.title)
        if self.model is not None:
            a = self.model.rangeX/2
            b = self.model.rangeY/2
            # print(a, b, a/b)
            # ratio = a/b
            self.ax.set_xlim(-a*1.1, a*1.1)  # (-110, 110)
            self.ax.set_ylim(-b*1.1, b*1.1)  # (-100, 100)
            if not self.drawDisplacement:
                self.load_data()
            else:
                self.load_displacement()
            if self.draw_landmarks and self.model.landmarks_3D is not None:
                self.load_landmarks()
            if self.bgImage is not None:
                img = pyplot.imread(self.bgImage)
                # SX DX BOTTOM UP
                self.ax.imshow(img, extent=[-b*1.05, b*1.03, -b*1.03, b*1.05])
        self.draw()
        self.flush_events()

    # def setModel(self, model):
    #    self.model = model
    #    self.bgImage = self.model.bgImage

    def select_area(self, x_coord, y_coord, width, height):
        x_data = self.model.model_data[:, 0]
        y_data = self.model.model_data[:, 1]

        x_ind = np.where((x_coord <= x_data) & (x_data <= x_coord + width))
        y_ind = np.where((y_coord <= y_data) & (y_data <= y_coord + height))

        x_data = y_data = None
        ind = np.intersect1d(np.array(x_ind), np.array(y_ind), assume_unique=True)
        x_ind = y_ind = None
        self.highlight_data(ind)  # evidenzio i punti relativi agli indici

        # if self.parent() is not None and self.title == "Source":
        # self.parent().data_selected(x_coord, y_coord, width, height)

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
        self.ax.scatter(Y[:, 0],  Y[:, 1], Y[:, 2], c='b')
        if self.bgImage is not None:
            img = pyplot.imread(self.bgImage)
            # SX DX BOTTOM UP
            self.ax.imshow(img, extent=[-self.model.rangeY/2 * 1.05, self.model.rangeY/2 * 1.03,
                                        -self.model.rangeY/2 * 1.03, self.model.rangeY/2 * 1.05])
        try:
            self.ax.text(0.87, 0.92, 'Iteration: {:d}\nError: {:06.4f}'.format(iteration, error),
                         horizontalalignment='center', verticalalignment='center', transform=self.ax.transAxes,
                         fontsize='x-large')
        except Exception as ex:
            print(ex)
        self.draw()
        self.flush_events()
