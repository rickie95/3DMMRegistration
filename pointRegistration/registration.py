from pointRegistration import *
from threading import Thread
from functools import partial
import numpy as np
from pycpd import *
from pointRegistration.displacementMap import displacementMap
from pointRegistration.model import Model
from graphicInterface.console import Logger
import time


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

    def run(self):
        # Decimate points
        #source = self.decimate(self.source_model.model_data, self.perc)
        source = self.source_model.getRegistrationPoints()
        target = self.decimate(self.target_model.model_data, self.perc)
        Logger.addRow("Points decimated.")
        # Add landmarks data
        #source = np.concatenate((source, self.source_model.landmarks_3D), axis=0)
        target = np.concatenate((target, self.target_model.landmarks_3D), axis=0)
        Logger.addRow("Landmarks added.")

        if self.method == 0:  # ICP
            print("ICP non è attualmente implementato")
            return
        if self.method == 1:  # CPD - RIGID
            reg = rigid_registration(**{'X': source, 'Y': target})
            meth = "CPD Rigid"
        if self.method == 2:  # CPD - AFFINE
            reg = affine_registration(**{'X': source, 'Y': target})
            meth = "CPD Affine"
        if self.method == 3:  # CPD - DEFORMABLE / NON - RIGID
            reg = deformable_registration(** {'X': source, 'Y': target})
            meth = "CPD Deformable"

        Logger.addRow("Starting registration with " + meth + ", using " + str(self.perc) + "% of points.")
        model = Model()

        reg_time = time.time()
        try:
            # Se si vuole visualizzare i progressi usare questa versione
            # data, reg_param = reg.register(partial(self.drawCallback, ax=None))
            data, reg_param = reg.register(partial(self.log, ax=None))

            if self.method == 1:  # Transform the whole point set if CPD Rigid
                model.setModelData(reg.transform_point_cloud(self.source_model.model_data))
            else:
                model.setModelData(data[0: target.shape[0] - self.target_model.landmarks_3D.shape[0]])

            model.setLandmarks(data[target.shape[0] - self.target_model.landmarks_3D.shape[0] : data.shape[0]])
            #model.centerData()
            model.setDisplacementMap(displacementMap(model.model_data, self.target_model.model_data, 3))
        except Exception as ex:
            Logger.addRow(str(ex))
            model = self.target_model  # Fail safe: rimetto il model di partenza
        finally:
            Logger.addRow("Took "+str(round(time.time()-reg_time, 3))+"s.")
            self.callback(model)

    def stop(self):
        self.should_stop = True

    def log(self, iteration, error, X, Y, ax):
        sss = "Iteration #" + str(iteration) + " error: " + str(error)
        Logger.addRow(sss)
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
