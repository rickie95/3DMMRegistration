from graphicInterface.console import Logger
from pointRegistration.model import Model
from scipy.spatial import cKDTree
import numpy as np
import multiprocessing
import matplotlib.pyplot as plt
import pickle  # Look Morty, I'm a pickle!


class DisplacementMap(Model):

    def __init__(self, source_model, target_model, max_dist=2):
        """
            Return source points with a distance from target neighbours greater than max_dist.

            :param source_model
            :type source_model Model

            :param target_model
            :type target_model Model

            :param max_dist
            :type max_dist number
         """

        self.set_points(source_model.points)
        target_points = target_model.points

        # Points KDTree
        tree = cKDTree(target_points)
        _, indices = tree.query(self.points, distance_upper_bound=max_dist, n_jobs=multiprocessing.cpu_count())
        # Indices contains only points with distance < max_dist from the nearest point.
        for ind in list(set(indices)):
            self.points_color[ind] = "black"

        # LandmarksKDTree
        if source_model.landmarks is not None and target_model.landmarks is not None:
            self.set_landmarks(source_model.landmarks)
            target_landmarks = target_model.landmarks
            tree = cKDTree(target_landmarks)
            _, indices = tree.query(self.landmarks, distance_upper_bound=max_dist, n_jobs=multiprocessing.cpu_count())
            for ind in list(set(indices)):
                self.landmarks_color[ind] = "green"

        Logger.addRow("Displacement map created.")

    def save_displacement_map(self, filename):
        pickle.dump(self, open(filename, "wb"))

    def shoot_displacement_map(self, filepath):
        plt.scatter(self.displacement_map[:, 0], self.displacement_map[:, 1], s=0.5)
        plt.savefig(str(filepath[0:-3]+"png"))
        plt.close()
