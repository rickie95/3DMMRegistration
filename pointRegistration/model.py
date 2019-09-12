from graphicInterface.console import Logger
from pointRegistration import file3DLoader
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np
import h5py
import ntpath
import os


class Model:

    def __init__(self, path_data=None, path_landmarks=None, image=None):
        """
        Create a model from a .wrl file (3D points) and a .bnd file (landmarks) or load
        both elements from a .mat file.
        :param path_data: path to the .wrl file
        :param path_landmarks: path to .bnd file (only for .wrl/.bnd case)
        :param image: path to the associated image (opt)
        """

        self.bgImage = None
        self.registration_points = np.empty((0, 3), dtype=int)  # Contains indices
        self.registration_params = None
        self.displacement_map = None

        if image is not None and Path(image).is_file():
            self.bgImage = image

        if path_data is not None:
            self.filename, self.file_extension = os.path.splitext(path_data)

            if self.file_extension == ".mat":
                file = h5py.File(path_data, 'r')
                self.set_model_data(np.transpose(np.array(file["avgModel"])))
                self.landmarks_3D = np.transpose(np.array(file["landmarks3D"]))

            if self.file_extension == ".wrl":
                self.set_model_data(file3DLoader.loadWRML(path_data))
                self.landmarks_3D = file3DLoader.loadBND(path_landmarks)

            if self.file_extension == ".off":
                self.set_model_data(self.read_off(path_data))
                self.landmarks_3D = None

            row = "Model loaded: " + str(self.model_data.shape[0]) + " points"

            if self.landmarks_3D is not None:
                row += " and " + str(self.landmarks_3D.shape[0]) + " landmarks."

            Logger.addRow(row)
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
            self.registration_points = np.empty((0, 3))

        self.registration_points = np.append(self.registration_points, reg_points)

    def get_registration_points(self):
        self.registration_points = np.unique(self.registration_points)
        return np.array(self.model_data[self.registration_points])

    def save_model(self, filepath):

        '''with open("save.off", 'w') as file:
            file.write("OFF\n")
            file.write(str(str(self.model_data.shape[0]) + " 0 0\n"))

            for index in range(self.model_data.shape[0]):
                row = "{0} {1} {2}\n"
                x, y, z = np.array(self.model_data[index]).tolist()
                file.write(row.format(x, y, z))


        return'''

        f = h5py.File(filepath, "w")
        f.create_dataset("model_data", data=self.model_data)
        if self.landmarks_3D is not None:
            f.create_dataset("landmarks3D", data=self.landmarks_3D)
        if self.displacement_map is not None:
            f.create_dataset("displacement_map", data=self.displacement_map)
        if self.registration_params is not None:
            f.create_dataset("scale_matrix", data=self.registration_params[0])  # scale
            f.create_dataset("rotation_matrix", data=self.registration_params[1])  # rotation
            f.create_dataset("traslation_matrix", data=self.registration_params[2])  # traslation
        f.close()
        Logger.addRow(str("File saved: " + filepath))

    def shoot_displacement_map(self, filepath):
        plt.scatter(self.displacement_map[:, 0], self.displacement_map[:, 1], s=0.5)
        plt.savefig(str(filepath[0:-3]+"png"))
        plt.close()

    def transform(self, scale_matrix=None, rotation_matrix=None, translation_matrix=None):
        if scale_matrix is not None:
            self.model_data *= scale_matrix
        if rotation_matrix is not None:
            self.model_data *= rotation_matrix
        if translation_matrix is not None:
            self.model_data *= translation_matrix

    @staticmethod
    def __path_leaf__(path):
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)

    @staticmethod
    def read_off(file, faces_required=False):
        """
        Reads vertices and faces from an off file.

        :param file: path to file to read
        :type file: str
        :param faces_required: True if the function should return faces also
        :type: bool
        :return: vertices and faces as lists of tuples
        :rtype: [(float)], [(int)]
        """

        assert os.path.exists(file)

        with open(file, 'r') as fp:
            lines = fp.readlines()
            lines = [line.strip() for line in lines]

            assert (lines[0] == 'OFF'), "Invalid preambole"

            parts = lines[1].split(' ')
            assert (len(parts) == 3), "Need exactly 3 parameters on 2nd line (n_vertices, n_faces, n_edges)."

            num_vertices = int(parts[0])
            assert num_vertices > 0

            num_faces = int(parts[1])
            assert num_faces > 0

            vertices = []
            for i in range(num_vertices):
                vertex = lines[2 + i].split(' ')
                vertex = [float(point) for point in vertex]
                assert (len(vertex) == 3), str("Invalid vertex row on line " + str(i))

                vertices.append(vertex)

            if num_vertices > len(vertices):
                row = "WARNING: some vertices were not loaded correctly: {0} declared vs {1} loaded."
                Logger.addRow(row.format(num_vertices, len(vertices)))

            vertices = np.asarray(vertices)

            if faces_required:
                faces = []
                for i in range(num_faces):
                    face = lines[2 + num_vertices + i].split(' ')
                    face = [int(index) for index in face]

                    assert face[0] == len(face) - 1
                    for index in face:
                        assert 0 <= index < num_vertices

                    assert len(face) > 1

                    faces.append(face)
                return vertices, faces

            return vertices

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
