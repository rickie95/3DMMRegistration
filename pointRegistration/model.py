import ntpath
import os

import h5py
import numpy as np
from scipy.spatial.transform import Rotation

from graphicInterface.console import Logger
from pointRegistration import file3D


class Model:

    def __init__(self, path_data=None):
        """
        Create a model from a .wrl file (3D points) and a .bnd file (landmarks) or load
        both elements from a .mat file.
        :param path_data: path to the .wrl file
        :param path_landmarks: path to .bnd file (only for .wrl/.bnd case)
        :param image: path to the associated image (opt)
        """
        self.landmarks = None
        self.landmarks_color = None
        self.points = None
        self.points_color = None

        self.highlighted_color = "y"

        self.init_attributes()
        if path_data is not None:
            self.load_model(path_data)
            self.center_model()

    @classmethod
    def from_model(cls, model):
        copy = cls()
        copy.set_points(np.copy(model.points))
        if model.points_color is not None:
            copy.points_color = model.points_color
        if model.landmarks is not None:
            copy.set_landmarks(np.copy(model.landmarks))
            if model.landmarks_color is not None:
                copy.landmarks_color = model.landmarks_color
        copy.filename = model.filename
        return copy

    def init_attributes(self):
        self.bgImage = None
        self.registration_points = None
        self.registration_params = None
        self.displacement_map = None
        self.rangeX = None
        self.rangeY = None
        self.filename = None

    def center_model(self):
        # Not always scans are perfectly centered.
        # Median is not sensible to big extreme value clusters
        points_median = np.median(self.points, axis=0)
        self.points -= points_median
        if self.landmarks is not None:
            self.landmarks -= points_median

    def set_points(self, data):
        self.points = data
        self.rangeX = np.ptp(self.points[:, 0])
        self.rangeY = np.ptp(self.points[:, 1])
        self.points_color = "b"

    def set_landmarks(self, land):
        self.landmarks = land
        self.landmarks_color = "r"

    def add_registration_points(self, reg_points):
        if reg_points[0] == -1:
            self.registration_points = np.empty((0, 3), dtype=int)

        self.registration_points = np.unique(np.append(self.registration_points, reg_points))

    def init_registration_points(self):
        self.registration_points = np.empty((0, 3), dtype=int)

    def get_registration_points(self):
        self.registration_points = np.unique(self.registration_points)
        return np.array(self.points[self.registration_points])

    def has_registration_points(self):
        if self.registration_points.shape[0] > 0:
            return True
        return False

    def save_model(self, filename):
        model = {"model_data": self.points}

        if self.landmarks is not None:
            model["landmarks3D"] = self.landmarks
        if self.displacement_map is not None:
            model["displacement_map"] = self.displacement_map
        if self.registration_params is not None:
            for i in range(len(self.registration_params)):
                model[str("reg_param"+str(i))] = self.registration_params[i]

        file3D.save_file(filename, model)
        Logger.addRow(str("File saved: " + filename))

    def compute_displacement_map(self, target_model, distance):
        from pointRegistration.displacementMap import DisplacementMap
        if target_model is None:
            return None
        return DisplacementMap.compute_map(source_model=self, target_model=target_model, max_dist=distance)

    def rotate(self, axis, theta):
        self.points = Model.rotate_model(axis, theta, self.points)
        if self.landmarks is not None:
            self.landmarks = Model.rotate_model(axis, theta, self.landmarks)

    @staticmethod
    def rotate_model(axis, theta, data):
        theta = np.radians(theta)
        cos_t = np.cos(theta)
        sin_t = np.sin(theta)
        if axis == 'x':
            rotation_matrix = Rotation.from_quat([0, sin_t, 0, cos_t])
        if axis == 'y':
            rotation_matrix = Rotation.from_quat([sin_t, 0, 0, cos_t])
        if axis == 'z':
            rotation_matrix = Rotation.from_quat([0, 0, sin_t, cos_t])
        return rotation_matrix.apply(data)

    def load_model(self, path_data):
        self.filename, self.file_extension = os.path.splitext(path_data)

        if os.path.exists(self.filename + ".png"):
            self.bgImage = self.filename + ".png"

        if self.file_extension == ".mat":
            file = h5py.File(path_data, 'r')
            try:
                self.set_points(np.transpose(np.array(file["avgModel"])))
                self.set_landmarks(np.transpose(np.array(file["landmarks3D"])))
            except Exception as ex:
                print("File is not compatible:" + ex)

        if self.file_extension == ".wrl":
            self.set_points(file3D.load_wrml(path_data))
            self.set_landmarks(file3D.load_bnd(self.filename + ".bnd"))
            if self.bgImage is not None and os.path.exists(self.bgImage):
                self.bgImage = self.filename[:-3] + "F2D.png"

        if self.file_extension == ".off":
            self.set_points(file3D.load_off(path_data))

        row = "Model loaded: " + str(self.points.shape[0]) + " points"

        if self.landmarks is not None:
            row += " and " + str(self.landmarks.shape[0]) + " landmarks."

        self.init_registration_points()
        Logger.addRow(row)

    @staticmethod
    def __path_leaf__(path):
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)

    @staticmethod
    def decimate(old_array, percentage):
        if percentage >= 100:
            return old_array

        le, _ = old_array.shape
        useful_range = np.arange(le)
        np.random.shuffle(useful_range)
        limit = int(le / 100 * percentage)
        new_arr = np.empty((limit, 3))
        rr = np.arange(limit)
        for count in rr:
            new_arr[count] = old_array[useful_range[count]]

        return new_arr
