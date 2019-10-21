from matplotlib.widgets import Button
from matplotlib import pyplot


class PlotButtonCollection(object):

    def __init__(self, callback, parent):
        self.callback = callback

        ax_yminus = pyplot.axes([0,   0.07,  0.09, 0.05])
        ax_yplus = pyplot.axes( [0.1, 0.07,  0.09, 0.05])
        ax_xminus = pyplot.axes([0,   0.13, 0.09, 0.05])
        ax_xplus = pyplot.axes( [0.1, 0.13, 0.09, 0.05])
        ax_zminus = pyplot.axes([0,   0.01, 0.09, 0.05])
        ax_zplus = pyplot.axes( [0.1, 0.01, 0.09, 0.05])

        self.b_yplus = Button(ax_yplus, '+15°')
        self.b_yplus.on_clicked(self.rotate_y_plus)

        self.b_yminus = Button(ax_yminus, 'Y -15°')
        self.b_yminus.on_clicked(self.rotate_y_minus)

        self.b_xplus = Button(ax_xplus, '+15°')
        self.b_xplus.on_clicked(self.rotate_x_plus)

        self.b_xminus = Button(ax_xminus, 'X -15°')
        self.b_xminus.on_clicked(self.rotate_x_minus)

        self.b_zminus = Button(ax_zminus, 'Z -15°')
        self.b_zminus.on_clicked(self.rotate_z_minus)

        self.b_zplus = Button(ax_zplus, '+15°')
        self.b_zplus.on_clicked(self.rotate_z_plus)

    def rotate_x_plus(self, event):
        self.callback('x', 15)

    def rotate_x_minus(self, event):
        self.callback('x', -15)

    def rotate_y_plus(self, event):
        self.callback('y', 15)

    def rotate_y_minus(self, event):
        self.callback('y', -15)

    def rotate_z_plus(self, event):
        self.callback('z', +15)

    def rotate_z_minus(self, event):
        self.callback('z', -15)
