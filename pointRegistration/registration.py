from pointRegistration.displacementMap import displacementMap
from pointRegistration.registration_param import RegistrationParameters
from pointRegistration.model import Model
from graphicInterface.console import Logger
from threading import Thread
from functools import partial
from pycpd import *
import numpy as np
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
        source = self.source_model.get_registration_points()
        target = Model.decimate(self.target_model.model_data, self.perc)
        Logger.addRow("Points decimated.")
        # Add landmarks data
        # source = np.concatenate((source, self.source_model.landmarks_3D), axis=0)
        if self.target_model.landmarks_3D is not None:
            target = np.concatenate((target, self.target_model.landmarks_3D), axis=0)
        Logger.addRow("Landmarks added.")

        ps = RegistrationParameters().getParams()

        if self.method == 1:  # CPD - RIGID
            reg = rigid_registration(**{'X': source, 'Y': target, 'sigma2': ps['sigma2'],
                                        'max_iterations': ps['max_iterations'], 'tolerance': ps['tolerance'],
                                        'w': ps['w']})
            meth = "CPD Rigid"
        else:
            Logger.addRow("Method not supported. Don't worry, I'm gonna use CPD rigid and save the day.")
            reg = rigid_registration(**{'X': source, 'Y': target, 'sigma2': ps['sigma2'],
                                        'max_iterations': ps['max_iterations'], 'tolerance': ps['tolerance'],
                                        'w': ps['w']})
            meth = "CPD Rigid"

        Logger.addRow("Starting registration with " + meth + ", using " + str(self.perc) + "% of points.")
        model = Model()

        reg_time = time.time()
        try:
            # Uncomment the following line if you want to see the progress in the widget
            data, reg_param = reg.register(partial(self.drawCallback, ax=None))
            # data, reg_param = reg.register(partial(self.log, ax=None))

            if self.method == 1:  # Transform the whole point set if CPD Rigid
                model.set_model_data(reg.transform_point_cloud(self.source_model.model_data))
            else:
                model.set_model_data(data[0: target.shape[0] - self.target_model.landmarks_3D.shape[0]])

            model.registration_params = reg_param
            if self.target_model.landmarks_3D is not None:
                model.set_landmarks(data[target.shape[0] - self.target_model.landmarks_3D.shape[0]: data.shape[0]])
            else:
                model.set_landmarks(None)
            model.filename = self.target_model.filename
            # model.centerData()
            model.set_displacement_map(displacementMap(model.model_data, self.target_model.model_data, 3))
        except Exception as ex:
            Logger.addRow("Err: "+str(ex))
            model = self.target_model  # Fail safe: rimetto il model di partenza
        finally:
            Logger.addRow("Took "+str(round(time.time()-reg_time, 3))+"s.")
            self.callback(model)

    def stop(self):
        self.should_stop = True

    def log(self, iteration, error, X, Y, ax):
        row = "Iteration #" + str(iteration) + " error: " + str(error)
        Logger.addRow(row)
        if self.should_stop:
            raise Exception("Registration has been stopped")
