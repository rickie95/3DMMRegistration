from functools import partial
import matplotlib.pyplot as plt
from pycpd import *
from pointRegistration.model import Model
import numpy as np

def visualize(iteration, error, X, Y, ax):
    plt.cla()
    ax.scatter(X[:,0],  X[:,1], X[:,2], color='red', label='Target')
    ax.scatter(Y[:,0],  Y[:,1], Y[:,2], color='blue', label='Source')
    #ax.text2D(0.87, 0.92, 'Iteration: {:d}\nError: {:06.4f}'.format(iteration, error), horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize='x-large')
    print(error)
    ax.legend(loc='upper left', fontsize='x-large')
    plt.draw()
    plt.pause(0.001)

def main():
    mmm = Model("avgModel_bh_1779_NE.mat")
    mmn = Model("M0001_NE00AM_F3D.wrl", "M0001_NE00AM_F3D.bnd", "M0001_NE00AM_F2D.png")
    ppp = np.loadtxt("pippo.txt")
    fig = plt.figure()
    ax = fig.add_subplot(111)
    callback = partial(visualize, ax=ax)

    reg = rigid_registration(**{'X': mmm.model_data, 'Y': mmn.model_data, 'sigma2':0.01})
    reg.register(callback)
    plt.show()

if __name__ == '__main__':
    main()