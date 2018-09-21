from scipy.spatial import cKDTree
import numpy as np
import multiprocessing


def displacementMap(source_points, target_points, max_dist=1.25):
    """ Restituisce i punti di source che distano più di max_dist dal punto più vicino di target. """
    tree = cKDTree(source_points)  # voglio i punti di source che hanno corrispondenza con i punti del target
    _, indices = tree.query(target_points, distance_upper_bound=max_dist, n_jobs=multiprocessing.cpu_count())
    # indices contiene tutti i punti che distano max_dist dal loro punto più vicino
    #indices_range = source_points.shape[0]
    ##displacement_indices = np.delete(np.arange(0, indices_range), indices)
    displacement_points = np.delete(source_points, indices, axis=0) # restituisco tutti i punti di source
    return displacement_points
