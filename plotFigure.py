from matplotlib import pyplot
from mpl_toolkits import mplot3d
import numpy as np
from scipy import spatial
import h5py
from stl import mesh


class PlotFigure:

    def __init__(self):
        # Creating figure and canvas
        self.fig, self.ax = pyplot.subplots()
        self.axes = mplot3d.Axes3D(self.fig)
        # attach event callbacks

        # Loading face template point and landmarks


        # Do not insert nothing after drawData call

    def loadData(self, path):
        my_mesh = mesh.Mesh.from_file(path)
        self.axes.add_collection3d(mplot3d.art3d.Poly3DCollection(my_mesh.vectors))
        scale = my_mesh.points.flatten(-1)
        self.axes.auto_scale_xyz(scale, scale, scale)


    def drawData(self):
        pyplot.cla()
        self.loadData("F0001_NE00WH_F3D.stl")
        pyplot.show()


#s = PlotFigure()
#s.drawData()



