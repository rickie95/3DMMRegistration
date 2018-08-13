import open3d
import numpy as np
import copy
from pointRegistration.model import Model

def ICPregistration(model1, model2):
    threshold = 0.02
    initTrans = np.asarray[[1.0, 1.0, 1.0, 1.0],
                           [1.0, 1.0, 1.0, 1.0],
                           [1.0, 1.0, 1.0, 1.0]
                           [0.0, 0.0, 0.0, 1.0]]

    draw_registration_result(model1, model2, initTrans)

def draw_registration_result(source, target, transformation):
    source_temp = copy.deepcopy(source)
    target_temp = copy.deepcopy(target)
    source_temp.paint_uniform_color([1, 0.706, 0])
    target_temp.paint_uniform_color([0, 0.651, 0.929])
    source_temp.transform(transformation)
    open3d.draw_geometries([source_temp, target_temp])

mmm = Model("avgModel_bh_1779_NE.mat")
mmn = Model("M0001_NE00AM_F3D.wrl", "M0001_NE00AM_F3D.bnd", "M0001_NE00AM_F2D.png")
ICPregistration(mmm, mmn)