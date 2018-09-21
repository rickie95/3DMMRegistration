import numpy as np
from threading import Thread
from graphicInterface.console import Logger
from pycpd.rigid_registration import rigid_registration
from pointRegistration.displacementMap import displacementMap
from pointRegistration.model import Model
from functools import partial
import time, datetime


class BatchRegistrationThread(Thread):

    def __init__(self, source, target_list, percentage, final_callback):
        Thread.__init__(self)
        self.source_model = source
        self.target_list = target_list
        self.perc = percentage
        self.finalCallback = final_callback
        self.should_stop = False
        Logger.addRow("Starting Batch Thread..")

    def run(self):
        source = self.source_model.getRegistrationPoints()

        try:
            for targ in self.target_list:
                Logger.addRow("Batch %d of %d:" % (self.target_list.index(targ) + 1, len(self.target_list)))
                path_wrl = targ[0:len(targ) - 3] + "bnd"
                t = Model(targ, path_wrl)
                target = BatchRegistrationThread.decimate(t.model_data, self.perc)
                Logger.addRow("Points decimated.")
                target = np.concatenate((target, t.landmarks_3D), axis=0)
                reg = rigid_registration(**{'X': source, 'Y': target})
                meth = "CPD Rigid"

                Logger.addRow("Starting registration with " + meth + ", using " + str(self.perc) + "% of points.")
                model = Model()

                reg_time = time.time()

                # Se si vuole visualizzare i progressi usare questa versione
                # data, reg_param = reg.register(partial(self.drawCallback, ax=None))
                data, reg_param = reg.register(partial(self.log, ax=None))

                model.setModelData(reg.transform_point_cloud(self.source_model.model_data))

                model.registration_params = reg_param
                model.setLandmarks(data[target.shape[0] - t.landmarks_3D.shape[0]: data.shape[0]])
                model.filename = t.filename
                # model.centerData()
                model.setDisplacementMap(displacementMap(model.model_data, t.model_data, 3))
                now = datetime.datetime.now()
                model.saveModel("./results/RIGID_REG_" + model.filename + "_%d_%d_%d_%d_%d.mat" %
                                (now.day, now.month, now.year, now.hour, now.minute))
                model.shootDisplacementMap("./results/RIGID_REG_" + model.filename + "_%d_%d_%d_%d_%d.mat" %
                                (now.day, now.month, now.year, now.hour, now.minute))
                Logger.addRow("Took " + str(round(time.time() - reg_time, 3)) + "s.")

        except Exception as ex:
            Logger.addRow(str(ex))
            print(ex)
        finally:
            self.finalCallback()

    def log(self, iteration, error, X, Y, ax):
        sss = "Iteration #" + str(iteration) + " error: " + str(error)
        Logger.addRow(sss)
        if self.should_stop:
            raise Exception("Registration has been stopped")

    @staticmethod
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
            new_arr[count] = old_array[useful_range[count]]

        return new_arr

    def stop(self):
        self.should_stop = True

