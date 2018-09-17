import numpy as np
from pointRegistration import file3DLoader
import h5py
from pathlib import Path
from graphicInterface.console import Logger

# todo: aggiungere il campo registration_points

class Model:

    def __init__(self, path_data=None, path_landmarks=None, image=None):
        """
        Create a model from a .wrl file (3D points) and a .bnd file (landmarks) or load
        both elements from a .mat file.
        :param path_data: path to the .wrl file
        :param path_landmarks: path to .bnd file (only for .wrl/.bnd case)
        :param image: path to the associated image (opt)
        """
        if path_data is not None:
            if path_landmarks is None:
                file = h5py.File(path_data, 'r')  # Caso .mat
                self.setModelData(np.transpose(np.array(file["avgModel"])))
                self.landmarks_3D = np.transpose(np.array(file["landmarks3D"]))
                Logger.addRow("Model loaded: " + str(self.model_data.shape[0]) + " points, " + str(
                    self.landmarks_3D.shape[0]) + " landmarks.")

            else:   # caso wrml + bnd
                self.setModelData(file3DLoader.loadWRML(path_data))
                self.landmarks_3D = file3DLoader.loadBND(path_landmarks)
                Logger.addRow("Model loaded: " + str(self.model_data.shape[0]) + " points, " + str(
                    self.landmarks_3D.shape[0]) + " landmarks.")

            self.centerData()

        self.bgImage = None
        self.registration_points = None  # Contains indices
        self.registration_params = None
        self.displacement_map = None

        if image is not None and Path(image).is_file():
            self.bgImage = image

    def centerData(self):
        # Not always scans are perfectly centered.
        # Median is unsensible to big extreme value clusters
        points_median = np.median(self.model_data, axis=0)
        self.model_data -= points_median
        self.landmarks_3D -= points_median

    def setDisplacementMap(self, disp):
        self.displacement_map = disp

    def setModelData(self, data):
        self.model_data = data
        self.rangeX = np.ptp(self.model_data[:, 0])
        self.rangeY = np.ptp(self.model_data[:, 1])

    def setLandmarks(self, land):
        self.landmarks_3D = land

    def addRegistrationPoints(self, reg_points):
        if reg_points[0] == -1:
            self.registration_points = np.empty((0, 3))

        if self.registration_points is None:
            self.registration_points = np.empty((0, 3), dtype=int)

        self.registration_points = np.append(self.registration_points, reg_points)

    def getRegistrationPoints(self):
        self.registration_points = np.unique(self.registration_points)
        return np.array(self.model_data[self.registration_points])

    def saveModel(self, filepath):
        f = h5py.File(filepath, "w")
        #f.create_dataset("model_data", data=self.model_data)
        #f.create_dataset("landmarks3D", data=self.landmarks_3D)
        if self.displacement_map is not None:
            f.create_dataset("displacement_map", data=self.displacement_map)
        if self.registration_params is not None:
            f.create_dataset("registration_params/scale_matrix", data=self.registration_params[0]) # scale
            f.create_dataset("registration_params/rotation_matrix", data=self.registration_params[1]) # rotation
            f.create_dataset("registration_params/traslation_matrix", data=self.registration_params[2]) # traslation
        f.close()
        Logger.addRow(str("File saved: " + filepath))

