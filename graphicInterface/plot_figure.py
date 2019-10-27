import numpy as np
from PyQt5.QtWidgets import QSizePolicy
from matplotlib import pyplot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from graphicInterface.console import suppress_stdout_stderr


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
        self.drawDisplacement = False
        self.landmarks_colors = None
        self.data_colors = None
        self.scale_width = None
        self.scale_height = None
        self.legend_handlers = []
        self.legend_has_been_drawn = True

        if model is not None:
            self.load_model(model)

    def load_model(self, model):
        self.model = model
        self.drawDisplacement = False

    def load_data(self, data, color, marker='o', points_size=0.5, label=""):
        if data is None or data.shape[0] == 0:
            return
        append = False
        if label != "":
            label += f" ({data.shape[0]})"
            append = True
        max_v = np.max(data[:, 2])
        min_v = np.min(data[:, 2])
        sizes = np.copy(data[:, 2])
        self.sizes = ((sizes + np.abs(min_v)) / np.abs(max_v)) + 0.5
        legend_handler, = self.ax.plot(data[:, 0], data[:, 1], c=color, marker=marker, linestyle='None',
                                       markersize=points_size, label=label)
        if append:
            self.legend_handlers.append(legend_handler)

    def load_displacement(self):
        self.ax.plot(self.model.displacement_map[:, 0], self.model.displacement_map[:, 1])

    def load_image(self):
        if self.bgImage is not None:
            img = pyplot.imread(self.bgImage)
            self.ax.imshow(img, extent=[-self.scale_height * 1.05, self.scale_height * 1.03, -self.scale_height * 1.03,
                                        self.scale_height * 1.05])  # SX DX BOTTOM UP

    def show_displacement(self):
        self.drawDisplacement = True if self.model.displacement_map is not None else False
        self.draw_landmarks = False

    def clear(self):
        self.ax.cla()

    def draw_data(self, clear=False):
        if clear:
            self.ax.cla()
        if self.title is not None:
            self.ax.set_title(self.title)
        if self.model is not None:
            self.ax.autoscale()
            self.ax.set_aspect('equal')
            self.ax.set_xlabel('X axis')
            self.ax.set_ylabel('Y axis')

            self.load_data(self.model.points, self.model.points_color, label="Points")
            if self.model.landmarks is not None:
                self.load_data(self.model.landmarks, self.model.landmarks_color, points_size=5, label="Landmarks")
            try:
                self.load_data(self.model.points[self.model.registration_points], 'y', label="Registration Points")
            except Exception as ex:
                pass

            try:
                self.load_data(self.model.missed_points, self.model.missed_points_color, marker='v',
                               label="Missed Points")
                self.load_data(self.model.missed_landmarks, self.model.missed_landmarks_color, size=5, marker='v',
                               label="Missed Landmarks")
            except Exception as ex:
                pass
            """if len(self.legend_handlers) > 0 and self.legend_has_been_drawn:
                self.ax.legend(handles=self.legend_handlers)
                self.legend_has_been_drawn = False
            """
            self.load_image()
        self.draw()

    def draw(self, clear=False):
        if clear is True:
            self.clear()
        super().draw()
        self.flush_events()

    def restore_model(self):
        self.ax.cla()
        self.draw_data()

    def landmarks(self, l):
        self.draw_landmarks = l

    def set_landmarks_colors(self, colors):
        self.model.landmarks_color = colors
        self.draw_data()

    def set_data_colors(self, colors):
        self.model.points_color = colors
        self.draw_data()

    def get_ax(self):
        return self.ax

    def update_plot_callback(self, iteration, error, X, Y, ax):
        self.ax.cla()
        print(iteration, error)
        self.ax.scatter(Y[:, 0], Y[:, 1], 0.1, c='r')
        self.ax.scatter(X[:, 0], X[:, 1], 0.1, c='b')
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
            super().draw()
        self.flush_events()

    def has_model(self):
        if self.model is not None:
            return True

        return False
