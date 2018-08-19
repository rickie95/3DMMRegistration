from functools import partial
import matplotlib.pyplot as plt
from pycpd import *
from pointRegistration.model import Model
import numpy as np

import time

def visualize(iteration, error, X, Y, ax):
    plt.cla()
    color_target = np.full_like(np.empty(int(X.size/3) - 66), 'w', dtype=str)
    color_source = np.full_like(np.empty(int(Y.size/3) - 83), 'w', dtype=str)
    color_target = np.concatenate((color_target, np.full_like(np.empty(66), 'yellow', dtype=str)))
    color_source = np.concatenate((color_source, np.full_like(np.empty(83), 'k', dtype=str)))
    #color_source = np.reshape(color_source, (-1, 1))
    #color_target = np.reshape(color_target, (-1, 1))
    ax.scatter(X[:,0],  X[:,1], c=color_target, label='Red: Target')
    ax.scatter(Y[:,0],  Y[:,1], c=color_source, label='Blu: Source')
    ax.text(0.87, 0.92, 'Iteration: {:d}\nError: {:06.4f}'.format(iteration, error), horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize='x-large')
    print(iteration, error)
    ax.legend(loc='upper left', fontsize='x-large')
    plt.draw()
    plt.pause(0.001)

def decimate(old_array, perc):
    if perc >= 100:
        return old_array

    le, _ = old_array.shape
    useful_range = np.arange(le)
    np.random.shuffle(useful_range)
    limit = int(le / 100 * perc)
    new_arr = np.empty((limit, 3))
    rr = np.arange(limit)

    for count in rr:
        new_arr[count] = old_array[range[count]]

    return new_arr

def main():
    mmm = Model("avgModel_bh_1779_NE.mat")
    mmn = Model("M0001_NE00AM_F3D.wrl", "M0001_NE00AM_F3D.bnd", "M0001_NE00AM_F2D.png")
    fig = plt.figure()
    ax = fig.add_subplot(111)
    callback = partial(visualize, ax=ax)

    st = time.clock()
    partial_target = decimate(mmn.model_data, 30)
    partial_model = decimate(mmm.model_data, 50)

    target = np.concatenate((partial_model, mmm.landmarks_3D), axis=0)
    source = np.concatenate((partial_target, mmn.landmarks_3D), axis=0)
    reg = rigid_registration(**{'X': source, 'Y': target})
    reg.register(callback)
    et = time.clock() - st
    print(et)
    plt.show()


if __name__ == '__main__':
    main()


