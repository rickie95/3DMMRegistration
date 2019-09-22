from graphicInterface.console import Logger
from scipy.spatial import cKDTree
import numpy as np
import multiprocessing


def displacementMap(source_model, target_model, max_dist=2):
    """
        Return source points with a distance from target neighbours greater than max_dist.

        :param source_model
        :type source_model Model

        :param target_model
        :type target_model Model

        :param max_dist
        :type max_dist number
     """

    source_points = source_model.model_data
    target_points = target_model.model_data

    if source_model.landmarks_3D is not None and target_model.landmarks_3D is not None:
        source_points = np.concatenate((source_points, source_model.landmarks_3D))
        target_points = np.concatenate((target_points, target_model.landmarks_3D))

    tree = cKDTree(source_points)
    _, indices = tree.query(target_points, distance_upper_bound=max_dist, n_jobs=multiprocessing.cpu_count())
    # Indices contains only points with distance < max_dist from the nearest point.
    displacement_points = np.delete(source_points, indices, axis=0)  # Purge closest points
    Logger.addRow("Displacement map created: "+str(displacement_points.size / 3)+" points.")
    return displacement_points
