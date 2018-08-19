from pointRegistration import *
from threading import Thread
from functools import partial
import numpy as np
from pycpd import *


def log(iteration, error, X, Y, ax):
    print(str(iteration), str(error))

class Registration:

    def __init__(self, method, source_model, target_model, perc, callback):
        #Thread.__init__(self)
        self.method = method
        self.source_model = target_model
        self.target_model = source_model
        self.perc = perc
        self.callback = callback

     #   self.run()


    #def run(self):
        # Decimate points
        source = self.decimate(self.source_model.model_data, self.perc)
        target = self.decimate(self.target_model.model_data, self.perc)
        # Add landmarks data
        source = np.concatenate((source, self.source_model.landmarks_3D), axis=0)
        target = np.concatenate((target, self.target_model.landmarks_3D), axis=0)

        if self.method == 0:  # ICP
            print("ICP non è attualmente implementato")
            pass
        if self.method == 1:  # CPD - RIGID
            reg = rigid_registration(**{'X': source, 'Y': target})
        if self.method == 2:  # CPD - AFFINE
            reg = affine_registration(**{'X': source, 'Y': target})
        if self.method == 3:  # CPD - DEFORMABLE / NON - RIGID
            reg = deformable_registration(** {'X': source, 'Y': target})

        reg.register(partial(log, ax=None))
        self.target_model.model_data = reg.transform_point_cloud(self.target_model.model_data)
        self.target_model.landmarks_3D = reg.transform_point_cloud(self.target_model.landmarks_3D)
        self.callback(self.target_model)



    def decimate(self, old_array, perc):
        if perc >= 100:
            return old_array

        le, _ = old_array.shape
        useful_range = np.arange(le)
        np.random.shuffle(useful_range)
        limit = int(le / 100 * perc)
        new_arr = np.empty((limit, 3))
        rr = np.arange(limit)
        for count in rr:
            new_arr[count] = old_array[useful_range[count]]

        return new_arr