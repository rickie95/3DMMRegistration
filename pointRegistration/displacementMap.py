import multiprocessing
import os
import pickle  # Look Morty, I'm a pickle!

import h5py
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import cKDTree

from graphicInterface.console import Logger
from pointRegistration.model import Model


class DisplacementMap(Model):

    def __init__(self, points, landmarks, points_color, landmarks_color, missed_points, missed_points_color,
                 missed_landmarks, missed_landmarks_color):
        self.init_attributes()
        self.set_points(points)
        self.set_landmarks(landmarks)
        self.points_color = points_color
        self.landmarks_color = landmarks_color
        self.missed_points = missed_points
        self.missed_points_color = missed_points_color
        self.missed_landmarks = missed_landmarks
        self.missed_landmarks_color = missed_landmarks_color

        self.rangeX = np.ptp(np.append(self.points[:, 0], self.missed_points[:, 0]))
        self.rangeY = np.ptp(np.append(self.points[:, 1], self.missed_points[:, 1]))

    @classmethod
    def compute_map(cls, source_model, target_model, max_dist=2):
        """:param source_model
            :type source_model Model

            :param target_model
            :type target_model Model

            :param max_dist
            :type max_dist number
         """

        source_points = source_model.points
        target_points = target_model.points

        hit_landmarks = None
        missed_landmarks = None
        landmarks_color = None
        missed_landmarks_color = None

        # Points KDTree
        tree = cKDTree(source_points)
        _, indices = tree.query(target_points, distance_upper_bound=max_dist, n_jobs=multiprocessing.cpu_count())
        # Indices contains source's neighbors indices to target's points used for query
        indices = set(indices)
        indices.discard(source_points.shape[0])
        indices = list(indices)
        hit_points = source_points[indices]
        missed_points = np.delete(source_points, indices, axis=0)  # Points without a feasible neighbor
        missed_color = "y"
        points_color = "b"
        # LandmarksKDTree
        if source_model.landmarks is not None and target_model.landmarks is not None:
            tree = cKDTree(source_model.landmarks)
            _, indices = tree.query(target_model.landmarks, distance_upper_bound=max_dist, n_jobs=multiprocessing.cpu_count())
            indices = set(indices)
            indices.discard(source_model.landmarks.shape[0])
            indices = list(indices)
            hit_landmarks = source_model.landmarks[indices]
            missed_landmarks = np.delete(source_model.landmarks, indices, axis=0)
            landmarks_color = "r"
            missed_landmarks_color = "p"

        Logger.addRow("Displacement map created.")
        return cls(points=hit_points, landmarks=hit_landmarks, points_color=points_color,
                   landmarks_color=landmarks_color, missed_points=missed_points, missed_landmarks=missed_landmarks,
                   missed_points_color=missed_color, missed_landmarks_color=missed_landmarks_color)

    def save_model(self, filename):
        name, file_extension = os.path.splitext(filename)

        if file_extension == ".h5py":
            self.save_h5py(filename)
        if file_extension == ".pickle":
            self.save_pickle(filename)

    def save_pickle(self, filename):
        name, file_extension = os.path.splitext(filename)
        missed_map = self.missed_points
        hit_map = self.points
        if self.landmarks is not None:
            missed_map = np.concatenate(missed_map, self.missed_landmarks)
            hit_map = np.concatenate(hit_map, self.landmarks)
        pickle.dump(missed_map, str(name+"_missed_points" + file_extension), "wb")
        pickle.dump(hit_map, str(name+"_hit_points" + file_extension), "wb")

    def save_h5py(self, filename):
        def encode_ss_utf_8(ss):
            return np.void(ss.encode('utf-8'))
        print("ok")
        # self = self.source_model.compute_displacement_map(self.target_model, 3)
        file = None
        try:
            file = h5py.File(filename, "w")
            file.create_dataset("points", data=self.points)
            file.create_dataset("missed_points", data=self.missed_points)
            file.attrs["points_color"] = encode_ss_utf_8(self.points_color)
            file.attrs["missed_points_color"] = encode_ss_utf_8(self.missed_points_color)
            if self.landmarks is not None:
                file.create_dataset("landmarks", data=self.landmarks)
                file.create_dataset("missed_landmarks", data=self.missed_landmarks)
                file.attrs["landmarks_color"] = encode_ss_utf_8(self.landmarks_color)
                file.attrs["missed_landmarks_color"] = encode_ss_utf_8(self.missed_landmarks_color)
        except Exception as ex:
            Logger.addRow("ERROR: Displacement map was not saved. =>" + str(ex))
        finally:
            if file is not None:
                file.close()

    @classmethod
    def load_model(cls, filename):
        try:
            file = h5py.File(filename, 'r')
            points = file.get("points").value
            missed_points = file.get("missed_points").value
            points_color = (file.attrs["points_color"]).tostring().decode('utf-8')
            missed_points_color = (file.attrs["missed_points_color"]).tostring().decode('utf-8')

            # If landmarks are not present a KeyError is raised
            landmarks = file.get("landmarks").value
            missed_landmarks = file.get("missed_landmarks").value
            landmarks_color = (file.attrs["landmarks_color"]).tostring().decode('utf-8')
            missed_landmarks_color = (file.attrs["missed_landmarks_color"]).tostring().decode('utf-8')

        except AttributeError:
            Logger.addRow("INFO: Displacement model has no landmarks.")
            landmarks = None
            landmarks_color = None
            missed_landmarks = None
            missed_landmarks_color = None
        except FileNotFoundError:
            Logger.addRow(f"ERROR: {filename} not found, check path.")

        except Exception as ex:
            Logger.addRow(f"ERROR: Problem during opening of {filename} =>" + str(ex))

        finally:
            displacement_model = cls(points=points, landmarks=landmarks,
                                     missed_points=missed_points,
                                     missed_landmarks=missed_landmarks,
                                     points_color=points_color,
                                     landmarks_color=landmarks_color,
                                     missed_points_color=missed_points_color,
                                     missed_landmarks_color=missed_landmarks_color)
        return displacement_model

    def shoot_displacement_map(self, filepath):
        plt.scatter(self.displacement_map[:, 0], self.displacement_map[:, 1], s=0.5)
        plt.savefig(str(filepath[0:-3]+"png"))
        plt.close()

    def rotate(self, axis, theta):
        super().rotate(axis, theta)
        try:
            self.missed_points = Model.rotate_model(axis, theta, self.missed_points)
            if self.missed_landmarks is not None:
                self.missed_landmarks = Model.rotate_model(axis, theta, self.missed_landmarks)
        except Exception as ex:
            print(ex)
