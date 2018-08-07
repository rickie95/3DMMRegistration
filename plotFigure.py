from matplotlib import pyplot
import numpy as np
from scipy import spatial
import h5py


class plotFigure():
    """
        avg_model_data: Nx3 array for 3D point of model
        landmarks_3D: 68x3 array for 3D points of model's landmarks
    """
    def __init__(self):
        # Creating figure and canvas
        self.fig, self.ax = pyplot.subplots()
        # attach event callbacks
        self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        # self.fig.canvas.mpl_connect('button_release_event', self.ReleaseClick)

        # Loading face template point and landmarks
        avgModel_file = h5py.File('avgModel_bh_1779_NE.mat', 'r')
        self.avg_model_data = np.transpose(np.array(avgModel_file["avgModel"]))
        self.id_landmarks_3D = np.transpose(np.array(avgModel_file["idxLandmarks3D"]))
        self.landmarks_3D = np.transpose(np.array(avgModel_file["landmarks3D"]))
        sz = int(self.landmarks_3D.size/3)
        self.landmarks_colors = np.full(sz, "r")

        self.mytree = None

        self.drawData()
        # Do not insert nothing after drawData call

    def selectNearestPixel(self, x_coord, y_coord):
        if self.mytree is None:  # calculate kdtree only if is neeeded
            print("Calculating 2DTree...")
            self.mytree = spatial.cKDTree(self.landmarks_3D[:, 0:2])  # costruisce il KDTree con i punti del Model

        dist, index = self.mytree.query([[x_coord, y_coord]], k=1)
        if dist < 5:  # TODO: non sarebbe male normalizzare
            self.landmarks_colors[index[0]] = "y" if self.landmarks_colors[index[0]] == "r" else "r"
            self.drawData()


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

    def drawData(self):
        pyplot.cla()
        self.ax.scatter(self.avg_model_data[:, 0], self.avg_model_data[:, 1], s=0.5, c="blue")
        self.ax.scatter(self.landmarks_3D[:, 0], self.landmarks_3D[:, 1], c=self.landmarks_colors)
        pyplot.xlim(-120, 120)
        pyplot.ylim(-100, 100)
        pyplot.show()

plotFigure()





