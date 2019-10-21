from graphicInterface.console import Logger
from scipy.spatial.transform import Rotation
from pointRegistration import file3D
import matplotlib.pyplot as plt
import numpy as np
import h5py
import ntpath
import os
import pickle  # Look Morty, I'm a pickle!


class Model:

    def __init__(self, path_data=None):
        """
        Create a model from a .wrl file (3D points) and a .bnd file (landmarks) or load
        both elements from a .mat file.
        :param path_data: path to the .wrl file
        :param path_landmarks: path to .bnd file (only for .wrl/.bnd case)
        :param image: path to the associated image (opt)
        """

        self.bgImage = None
        self.registration_points = None
        self.registration_params = None
        self.displacement_map = None
        self.landmarks_3D = None
        self.model_data = None
        self.rangeX = None
        self.rangeY = None
        self.filename = None

        if path_data is not None:
            self.load_model(path_data)
            self.center_data()

    def center_data(self):
        # Not always scans are perfectly centered.
        # Median is not sensible to big extreme value clusters
        points_median = np.median(self.model_data, axis=0)
        self.model_data -= points_median
        if self.landmarks_3D is not None:
            self.landmarks_3D -= points_median

    def set_displacement_map(self, disp):
        self.displacement_map = disp

    def set_model_data(self, data):
        self.model_data = data
        self.rangeX = np.ptp(self.model_data[:, 0])
        self.rangeY = np.ptp(self.model_data[:, 1])

    def set_landmarks(self, land):
        self.landmarks_3D = land

    def add_registration_points(self, reg_points):
        if reg_points[0] == -1:
            self.registration_points = np.empty((0, 3), dtype=int)

        self.registration_points = np.unique(np.append(self.registration_points, reg_points))

    def init_registration_points(self):
        self.registration_points = np.empty((0, 3), dtype=int)

    def get_registration_points(self):
        self.registration_points = np.unique(self.registration_points)
        return np.array(self.model_data[self.registration_points])

    def has_registration_points(self):
        if self.registration_points.shape[0] > 0:
            return True
        return False

    def save_model(self, filepath):
        model = {"model_data": self.model_data}

        if self.landmarks_3D is not None:
            model["landmarks3D"] = self.landmarks_3D
        if self.displacement_map is not None:
            model["displacement_map"] = self.displacement_map
        if self.registration_params is not None:
            for i in range(len(self.registration_params)):
                model[str("reg_param"+str(i))] = self.registration_params[i]

        file3D.save_file(filepath, model)
        Logger.addRow(str("File saved: " + filepath))

    def save_displacement_map(self, filename):
        pickle.dump(self.displacement_map, open(filename, "wb"))

    def shoot_displacement_map(self, filepath):
        plt.scatter(self.displacement_map[:, 0], self.displacement_map[:, 1], s=0.5)
        plt.savefig(str(filepath[0:-3]+"png"))
        plt.close()

    def rotate(self, axis, theta):
        self.model_data = Model.rotate_data(axis, theta, self.model_data)
        if self.landmarks_3D is not None:
            self.landmarks_3D = Model.rotate_data(axis, theta, self.landmarks_3D)

    @staticmethod
    def rotate_data(axis, theta, data):
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
            self.set_model_data(np.transpose(np.array(file["avgModel"])))
            self.landmarks_3D = np.transpose(np.array(file["landmarks3D"]))

        if self.file_extension == ".wrl":
            self.set_model_data(file3D.load_wrml(path_data))
            self.landmarks_3D = file3D.load_bnd(self.filename + ".bnd")
            if self.bgImage is not None and os.path.exists(self.bgImage):
                self.bgImage = self.filename[:-3] + "F2D.png"

        if self.file_extension == ".off":
            self.set_model_data(file3D.load_off(path_data))

        row = "Model loaded: " + str(self.model_data.shape[0]) + " points"

        if self.landmarks_3D is not None:
            row += " and " + str(self.landmarks_3D.shape[0]) + " landmarks."

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
