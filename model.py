import numpy as np
import file3DLoader
import h5py

class Model:

    def __init__(self, path_data, path_landmarks=None, image=None):
        """
        Create a model from a .wrl file (3D points) and a .bnd file (landmarks)
        :param path_data: path to the .wrl file
        :param path_landmarks: path to .bnd file
        """
        if path_landmarks is None:  # Caso wrl+bnd
            file = h5py.File(path_data, 'r')  # Caso .mat
            self.model_data = np.transpose(np.array(file["avgModel"]))
            self.landmarks_3D = np.transpose(np.array(file["landmarks3D"]))
        else:
            self.model_data = file3DLoader.loadWRML(path_data)
            self.landmarks_3D = file3DLoader.loadBND(path_landmarks)

        self.bgImage = image

        # finally center data in (0, 0)
        self.centerData()

    def centerData(self):
        # Not always scans are perfectly centered.
        # We use median 'cause is unsensible to big extreme value clusters
        points_median = np.median(self.model_data, axis=0)
        self.model_data -= points_median
        self.landmarks_3D -= points_median
