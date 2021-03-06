from pointRegistration.registration_param import RegistrationParameters
from pointRegistration.model import Model
from graphicInterface.console import Logger
from threading import Thread
from functools import partial
from pycpd import *
import numpy as np
import time


class Registration(Thread):

    def __init__(self, method, source_model, target_model, perc, callback, iteration_callback=None):
        Thread.__init__(self)
        self.method = method
        self.source_model = source_model
        self.target_model = target_model
        self.percentage = perc
        self.callback = callback
        self.should_stop = False
        self.iteration_callback = iteration_callback
        self.registration_method = None

    def run(self):
        source = self.source_model.get_registration_points()
        target = Model.decimate(self.target_model.points, self.percentage)
        Logger.addRow("Points decimated.")
        if self.target_model.landmarks is not None:
            target = np.concatenate((target, self.target_model.landmarks), axis=0)
        Logger.addRow("Landmarks added.")

        ps = RegistrationParameters().get_params()

        if self.method == 1:  # CPD - RIGID
            self.registration_method = rigid_registration(**{'X': target, 'Y': source, 'sigma2': ps['sigma2'],
                                                             'max_iterations': ps['max_iterations'],
                                                             'tolerance': ps['tolerance'], 'w': ps['w']})
            method = "CPD Rigid"
        if self.method == 2:  # CPD - AFFINE
            self.registration_method = affine_registration(**{'X': target, 'Y': source, 'sigma2': ps['sigma2'],
                                                              'max_iterations': ps['max_iterations'],
                                                              'tolerance': ps['tolerance'], 'w': ps['w']})
            method = "CPD Affine"
        if self.method == 3:  # CPD - DEFORMABLE
            self.registration_method = deformable_registration(**{'X': target, 'Y': source, 'sigma2': ps['sigma2'],
                                                                  'max_iterations': ps['max_iterations'],
                                                                  'tolerance': ps['tolerance'], 'w': ps['w']})
            method = "CPD Deformable"

        Logger.addRow("Starting registration with " + method + ", using " + str(self.percentage) + "% of points.")
        model = Model()
        reg_time = time.time()

        try:
            self.registration_method.register(partial(self.interruptable_wrapper, ax=None))
            model = self.aligned_model(model)
        except InterruptedException as ex:
            Logger.addRow(str(ex))
            model = self.aligned_model(model)
        except Exception as ex:
            Logger.addRow("Err: " + str(ex))
            model = self.target_model  # Fail: back with the original target model
        finally:
            Logger.addRow("Took "+str(round(time.time()-reg_time, 3))+"s.")
            self.callback(model)

    def aligned_model(self, model):
        """
            Transforms all data points and landmarks of source model, applying the transformation obtained during the
            registration phase.
        :param model: A initialized and empty Model object
        :return: The input model, filled with transformed data points, landmarks, filename, registration parameters
            and displacement map oomputed between transformed source and target.
        """
        model.registration_params = self.registration_method.get_registration_parameters()
        points = self.registration_method.transform_point_cloud(self.source_model.points)
        if self.source_model.landmarks is not None:
            landmarks = self.registration_method.transform_point_cloud(self.source_model.landmarks)
            model.set_landmarks(landmarks)

        model.set_points(points)
        model.filename = self.target_model.filename

        # model.compute_displacement_map(self.target_model, 3)
        return model

    def stop(self):
        self.should_stop = True

    def log(self, iteration, error):
        row = "Iteration #" + str(iteration) + " error: " + str(error)
        Logger.addRow(row)

    def interruptable_wrapper(self, **kwargs):
        if self.should_stop:
            raise InterruptedException("Registration has been stopped")

        if self.iteration_callback is None:
            self.log(**kwargs)
        else:
            self.iteration_callback(**kwargs)


class InterruptedException(Exception):
    pass
