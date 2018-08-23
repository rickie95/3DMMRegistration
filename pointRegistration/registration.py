from pointRegistration import *
from threading import Thread
from functools import partial
import numpy as np
from pycpd import *
from pointRegistration.model import Model




class Registration(Thread):

    def __init__(self, method, source_model, target_model, perc, callback, drawCallback):
        Thread.__init__(self)
        self.method = method
        self.source_model = source_model
        self.target_model = target_model
        self.perc = perc
        self.callback = callback
        self.drawCallback = drawCallback
        self.should_stop = False

        #self.run()


    def run(self):
        print("hi there")
        # Decimate points
        source = self.decimate(self.source_model.model_data, self.perc)
        target = self.decimate(self.target_model.model_data, self.perc)
        # Add landmarks data
        source = np.concatenate((source, self.source_model.landmarks_3D), axis=0)
        target = np.concatenate((target, self.target_model.landmarks_3D), axis=0)

        if self.method == 0:  # ICP
            print("ICP non è attualmente implementato")
            return
        if self.method == 1:  # CPD - RIGID
            reg = rigid_registration(**{'X': source, 'Y': target})
        if self.method == 2:  # CPD - AFFINE
            reg = affine_registration(**{'X': source, 'Y': target})
        if self.method == 3:  # CPD - DEFORMABLE / NON - RIGID
            reg = deformable_registration(** {'X': source, 'Y': target})

        model = Model()

        try:
            # Se si vuole visualizzare i progressi usare questa versione
            # data, reg_param = reg.register(partial(self.drawCallback, ax=None))
            data, reg_param = reg.register(partial(self.log, ax=None))
            model.setModelData(data[0: target.shape[0] - self.target_model.landmarks_3D.shape[0]])
            model.setLandmarks(data[target.shape[0] - self.target_model.landmarks_3D.shape[0] : data.shape[0]])
            #model.centerData()
            self.callback(model)
        except Exception as ex:
            print(ex)
            return self.target_model  # Fail safe: rimetto il model di partenza

    def stop(self):
        self.should_stop = True

    def log(self, iteration, error, X, Y, ax):
        print(str(iteration), str(error))
        if self.should_stop:
            raise Exception("Registration has been stopped")

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
