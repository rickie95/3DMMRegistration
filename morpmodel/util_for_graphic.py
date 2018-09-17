import numpy as np
from scipy.interpolate import LinearNDInterpolator
from numpy import dot, mean, std, argsort
from numpy.linalg import eigh
from scipy.spatial import ConvexHull
from matplotlib import path


class graphic_tools:
    _3DMM_obj = ()

    def __init__(self, _3dmm_obj):
        if _3dmm_obj is None:
            self._3DMM_obj = None
        else:
            self._3DMM_obj = _3dmm_obj

    def render3DMM(self, xIm, yIm, rgb, w, h):
        # need to perfomr the proj shape from the 3D model of the shape. The first column of projShape is xIm, the secondo is yIm.
        # The texture of the 3D model is the var rgb
        x_grid, y_grid = np.meshgrid([int(x) for x in range(w)], [int(y) for y in range(h)])
        _first_cord = np.transpose(xIm)
        _second_cord = np.transpose(yIm)
        # Interpolate z values on the grid
        coords = self._2linear_vects(_first_cord.reshape(_first_cord.shape[0],1), _second_cord.reshape(_second_cord.shape[0],1))
        Fr = LinearNDInterpolator(coords, np.transpose(rgb[:,0]))
        Fb = LinearNDInterpolator(coords, np.transpose(rgb[:,1]))
        Fg = LinearNDInterpolator(coords, np.transpose(rgb[:,2]))
        # Get values for each location
        imR = Fr(x_grid,y_grid)
        imG = Fb(x_grid,y_grid)
        imB = Fg(x_grid,y_grid)

        pts = np.column_stack([xIm, yIm])
        pts = np.round(pts)
        pts = np.unique(pts, axis=0)
        allPoints=np.column_stack((pts[:,0],pts[:,1]))
        hullPoints = ConvexHull(allPoints)
        bb = hullPoints.vertices
        bb = np.array(bb, dtype=np.intp)
        mask = self.inpolygon(x_grid, y_grid, pts[bb,0], pts[bb,1])
        mask = np.logical_not(mask)

        imR[mask] = 0
        imG[mask] = 0
        imB[mask] = 0
        # building image
        img = np.empty((imR.shape[0], imR.shape[1], 3))
        img[:,:,0] = imR
        img[:,:,1] = imG
        img[:,:,2] = imB
        #img = img*255
        return np.array(img,dtype=np.uint8)

    def inpolygon(self, xq, yq, xv, yv):
        shape = xq.shape
        xq = xq.reshape(-1)
        yq = yq.reshape(-1)
        xv = xv.reshape(-1)
        yv = yv.reshape(-1)
        q = [(xq[i], yq[i]) for i in range(xq.shape[0])]
        p = path.Path([(xv[i], yv[i]) for i in range(xv.shape[0])])
        return p.contains_points(q).reshape(shape)

    def denseResampling(self, defShape, proj_shape, img, S, R, t, visIdx):
        grid_step = 1
        max_sh = (np.amax(proj_shape, axis=0))
        max_sh = np.reshape(max_sh,(1,2),order='F')
        min_sh = np.amin(proj_shape, axis=0)
        min_sh = np.reshape(min_sh, (1,2), order='F')
        Xsampling = np.arange(min_sh[0,0], max_sh[0,0], grid_step, dtype='float')
        Ysampling = np.arange(max_sh[0,1], min_sh[0,1], -grid_step, dtype='float')
        # round the float numbers
        Xsampling = np.around(Xsampling)
        Ysampling = np.around(Ysampling)

        print ("SAMPLING THE GRID")
        x_grid, y_grid = np.meshgrid(Xsampling, Ysampling)
        print ("3D LOCATION INTERPOLATION")
        index = np.array(visIdx, dtype=np.intp)
        X = proj_shape[index, 0]
        Y = proj_shape[index, 1]
        coords = self._2linear_vects(X,Y)
        #coords = list(zip(X,Y))
        Fx = LinearNDInterpolator(coords, defShape[index, 0])
        Fy = LinearNDInterpolator(coords, defShape[index, 1])
        Fz = LinearNDInterpolator(coords, defShape[index, 2])
        print ("PIXEL SAMPLING")
        x = Fx(x_grid.flatten(order='F'), y_grid.flatten(order='F'))
        y = Fy(x_grid.flatten(order='F'), y_grid.flatten(order='F'))
        z = Fz(x_grid.flatten(order='F'), y_grid.flatten(order='F'))
        print ("IMAGE BUILDING")
        x = x[~np.isnan(x).any(axis=1)]
        y = y[~np.isnan(y).any(axis=1)]
        z = z[~np.isnan(z).any(axis=1)]
        mod3d = np.dstack([x, y, z])
        #mod3d = np.delete(mod3d, [0,1,2,3], axis=0) # c'erano 3 valori in piu dall'interpolazione...??
        mod3d = np.reshape(mod3d,(mod3d.shape[0],3))
        print ("FINAL RENDERING")
        projMod3d = np.transpose(self._3DMM_obj.getProjectedVertex(mod3d, S, R, t))
        colors = self.getRGBtexture(np.round(projMod3d), img)
        colors = self._3DMM_obj.transVertex(colors)
        print ("DONE DENSE RESAMPLING")
        return [mod3d,colors]

    def resampleRGB(self,P,colors,step):
        min_x = np.amin(P[0,:], axis=0)
        max_x = np.amax(P[0,:], axis=0)
        min_y = np.amin(P[1,:], axis=0)
        max_y = np.amax(P[1,:], axis=0)
        Xsampling = np.arange(min_x, max_x, step, dtype='float')
        Ysampling = np.arange(max_y, min_y, -step, dtype='float')
        x, y = np.meshgrid(Xsampling, Ysampling)
        _first_cord = np.transpose(P[0,:])
        _second_cord = np.transpose(P[1,:])
        coords = self._2linear_vects(_first_cord.reshape(_first_cord.shape[0],1), _second_cord.reshape(_second_cord.shape[0],1))
        #Fr = griddata(coords, np.transpose(colors[0, :]), (x, y), method='linear')
        #Fg = griddata(coords, np.transpose(colors[1, :]), (x, y))
        #Fb = griddata(coords, np.transpose(colors[2, :]), (x, y))

        Fr = LinearNDInterpolator(coords, np.transpose(colors[0, :]))
        Fb = LinearNDInterpolator(coords, np.transpose(colors[1, :]))
        Fg = LinearNDInterpolator(coords, np.transpose(colors[2, :]))

        texR = Fr(x,y)
        texG = Fb(x,y)
        texB = Fg(x,y)
        #remove Nan elements
        mask = np.isnan(texR)
        index = np.array(mask, dtype=np.intp)
        texR[mask] = 0
        texG[mask] = 0
        texB[mask] = 0
        img = np.empty((texR.shape[0], texR.shape[1], 3))
        img[:,:,0] = texR
        img[:,:,1] = texG
        img[:,:,2] = texB
        return img, Xsampling, Ysampling



        '''texR = np.nan_to_num(Fr(x, y))
        texG = np.nan_to_num(Fg(x, y))
        texB = np.nan_to_num(Fb(x, y))
        img = np.empty((texR.shape[0], texR.shape[1], 3))
        img[:, :, 0] = texR
        img[:, :, 1] = texG
        img[:, :, 2] = texB
        #img = img * 255
        return img, Xsampling, Ysampling'''

    def _2linear_vects(self, X,Y): # Creo le coordinate (X,Y) da passare alla funzione interpolatrice
        coords = np.empty((1, 2))
        for i in range(X.shape[0]):
            new_cord = np.array([X[i, 0], Y[i, 0]]).reshape(1, 2, order='F')
            coords = np.row_stack((coords, new_cord))
        coords = np.delete(coords, (0), axis=0)
        return coords

    def getRGBtexture(self, coordTex, tex):
        R = (tex[:,:,0]).flatten(order='F')
        G = (tex[:,:,1]).flatten(order='F')
        B = (tex[:,:,2]).flatten(order='F')
        #print(coordTex.shape)
        Xtex = np.round(coordTex[:,0])
        Ytex = np.round(coordTex[:,1])
        Xtex = np.maximum(Xtex, np.tile(1, Xtex.shape[0]))
        Ytex = np.maximum(Ytex, np.tile(1, Ytex.shape[0]))
        Xtex = np.minimum(Xtex, np.tile(tex.shape[1], Xtex.shape[0]))
        Ytex = np.minimum(Ytex, np.tile(tex.shape[0], Ytex.shape[0]))
        #I = (self.sub2ind(tex.shape, Ytex, Xtex)).astype(int)
        #I = np.sub2ind(tex.shape, Ytex, Xtex)
        I = Ytex + (Xtex - 1) * tex.shape[0]
        I = I.astype(int)
        #print(I.shape)
        Ri = R[I]
        Gi = G[I]
        Bi = B[I]
        colors = np.empty((Ri.shape[0],1))
        colors = np.hstack((colors, Ri.reshape(Ri.shape[0],1)))
        colors = np.hstack((colors, Gi.reshape(Gi.shape[0],1)))
        colors = np.hstack((colors, Bi.reshape(Bi.shape[0],1)))
        colors = np.delete(colors, (0), axis=1)
        colors = (colors.astype(float))/255.0

        return colors

    def renderFaceLossLess(self, defShape, projShape, img, S, R, T, renderingStep, visIdx):
        [mod3d, colors] = self.denseResampling(defShape, projShape, img, S, R, T, visIdx)
        frontal_view = self.build_image(np.transpose(mod3d), np.transpose(defShape), colors, renderingStep)
        return frontal_view, colors, mod3d

    def build_image(self, P_f, P, colors, step):
        print("START BUILD FRONTAL VIEW")
        min_x = np.amin(P[0,:])
        max_x = np.amax(P[0,:])
        min_y = np.amin(P[1,:])
        max_y = np.amax(P[1,:])
        Xsampling = np.arange(min_x, max_x, step, dtype='float')
        Ysampling = np.arange(max_y, min_y, -step, dtype='float')

        [x, y] = np.meshgrid(Xsampling, Ysampling)
        _first_cord = np.transpose(P_f[0,:])
        _second_cord = np.transpose(P_f[1,:])

        coords = self._2linear_vects(_first_cord.reshape(_first_cord.shape[0],1), _second_cord.reshape(_second_cord.shape[0],1))
        Fr = LinearNDInterpolator(coords, np.transpose(colors[0,:]))
        Fb = LinearNDInterpolator(coords, np.transpose(colors[1,:]))
        Fg = LinearNDInterpolator(coords, np.transpose(colors[2,:]))
        texR = np.nan_to_num(Fr(x, y))
        texG = np.nan_to_num(Fg(x, y))
        texB = np.nan_to_num(Fb(x, y))
        #mask = np.zeros((texR.shape[0], texR.shape[1]), dtype='bool')
        #for i in range(mask.shape[0]):
        #    for j in range(mask.shape[1]):
        #        if np.isnan(texR[i, j]):
        #            mask[i, j] = True
        #texR = texR[~mask]
        img = np.empty((texR.shape[0],texR.shape[1],3))
        img[:,:,0] = texR
        img[:,:,1] = texG
        img[:,:,2] = texB
        img = img*255
        #img = img[~mask]
        print("DONE")
        return np.array(img,dtype=np.uint8)

    def resize_imgs(self, img, size_row, size_col):
        rows = img.shape[0]
        cols = img.shape[1]
        # resize the rows
        if rows > size_row:
            diff = rows - size_row
            for i in range(diff):
                img = np.delete(img, (i), axis=0)
        else:
            diff = size_row - rows
            new_row = np.zeros((1, cols, 3))
            for i in range(diff):
                img = np.vstack([img, new_row])
        if cols > size_col:
            diff = cols - size_col
            for i in range(diff):
                img = np.delete(img, (i), axis=1)
        else:
            diff = size_col - cols
            new_col = np.zeros((img.shape[0],1, 3))
            #print img.shape
            #print new_col.shape
            for i in range(diff):
                img = np.hstack([img,new_col])
        return img

    #def sub2ind(self, array_shape, rows, cols):
     #   return rows*array_shape[1] + cols

    def avgModel(self, object):
        # creo il modello medio
        rows = object[0].frontalView.shape[0]
        cols = object[0].frontalView.shape[1]
        R_cumulative_matrix = object[0].frontalView[:, :, 0]
        G_cumulative_matrix = object[0].frontalView[:, :, 1]
        B_cumulative_matrix = object[0].frontalView[:, :, 2]
        for i in range(len(object)):
            current_R = object[i].frontalView[:, :, 0]
            current_G = object[i].frontalView[:, :, 1]
            current_B = object[i].frontalView[:, :, 2]
            R_cumulative_matrix = R_cumulative_matrix + current_R
            G_cumulative_matrix = G_cumulative_matrix + current_G
            B_cumulative_matrix = B_cumulative_matrix + current_B
        mean_R = R_cumulative_matrix / len(object)
        mean_G = G_cumulative_matrix / len(object)
        mean_B = B_cumulative_matrix / len(object)
        avgModel = np.empty((rows, cols, 3))
        avgModel[:,:,0] = mean_R
        avgModel[:,:,1] = mean_G
        avgModel[:,:,2] = mean_B

        return np.array(avgModel,dtype=np.uint8)

    def colors_AVG(self, object):
        cumulative_matrix_col = object[0].colors
        for i in range(len(object)):
            cumulative_matrix_col = cumulative_matrix_col + object[i].colors
        return cumulative_matrix_col/len(object)

    def deform_texture_fast(self, mean, eigenves, alpha, ex_to_ne):
        dim = eigenves.shape[0]/3
        alpha_full = np.tile(np.transpose(alpha), (eigenves.shape[0],1))
        tmp_eigen = alpha_full*eigenves
        sumVec = tmp_eigen.sum(axis=1)
        sumVec = sumVec.reshape((sumVec.shape[0],1), order='F')
        sumMat = np.reshape(np.transpose(sumVec), (3,dim), order='F')
        return mean + sumMat

    def cov(self,X):
        """
        Covariance matrix
        note: specifically for mean-centered data
        note: numpy's `cov` uses N-1 as normalization
        """
        return dot(X.T, X) / X.shape[0]
        # N = data.shape[1]
        # C = empty((N, N))
        # for j in range(N):
        #   C[j, j] = mean(data[:, j] * data[:, j])
        #   for k in range(j + 1, N):
        #       C[j, k] = C[k, j] = mean(data[:, j] * data[:, k])
        # return C

    def pca(self,data, pc_count=None):
        """
        Principal component analysis using eigenvalues
        note: this mean-centers and auto-scales the data (in-place)
        """
        data -= mean(data, 0)
        data /= std(data, 0)
        C = self.cov(data)
        E, V = eigh(C)
        key = argsort(E)[::-1][:pc_count]
        E, V = E[key], V[:, key]
        U = dot(data, V)  # used to be dot(V.T, data.T).T
        return U, E, V

    def PIL2array(self,img):
        return np.array(img.getdata(),
                           np.uint8).reshape(img.size[1], img.size[0], 3)

    def mse(self, imageA, imageB):
        # the 'Mean Squared Error' between the two images is the
        # sum of the squared difference between the two images;
        # NOTE: the two images must have the same dimension
        err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
        err /= float(imageA.shape[0] * imageA.shape[1])

        # return the MSE, the lower the error, the more "similar"
        # the two images are
        return err

    def compare_imgs(self,i1,i2):
        pairs = zip(i1.getdata(), i2.getdata())
        if len(i1.getbands()) == 1:
            # for gray-scale jpegs
            dif = sum(abs(p1 - p2) for p1, p2 in pairs)
        else:
            dif = sum(abs(c1 - c2) for p1, p2 in pairs for c1, c2 in zip(p1, p2))

        ncomponents = i1.size[0] * i1.size[1] * 3
        #print "Difference (percentage):", (dif / 255.0 * 100) / ncomponents
        return (dif / 255.0 * 100) / ncomponents

    def mean(self, obj):
        sum = 0
        for i in range(len(obj)):
            sum += obj[i].ssim_D
        return sum/len(obj)

    def plot_mesh(self, vertex, face, texture, texture_coords):
        # function to map texture (on a 2d image) to a 3d surface
        # It's not general, vertex was assigned both to FF and TF
        FF = face
        VV = vertex 
        TF = face
        VT = texture_coords 
        I = texture
        iscolor = True
        VT2 = VT
        sizep = 64
        [lambda1, lambda2, lambda3, jind] = self.calculateBarycentricInterpolationValues(sizep)
        Ir = I[:,:,0]
        Ig = I[:,:,1]
        Ib = I[:,:,2]
        Jr = np.zeros((sizep+1, sizep+1))
        Jg = np.zeros((sizep+1, sizep+1))
        Jb = np.zeros((sizep+1, sizep+1))

        #for i in range(FF.shape[0]):
        for i in range(1):
            # current triangles of the mesh
            V = VV[FF[i,:],:]
            Vt = VT2[TF[i,:],:]

            # Define the triangle as a surface
            x = np.matrix([[V[0,0], V[1,0]], [V[2,0], V[2,0]]])
            y = np.matrix([[V[0,1], V[1,1]], [V[2,1], V[2,1]]])
            z = np.matrix([[V[0,2], V[1,2]], [V[2,2], V[2,2]]])

            # Define the texture coordinates of the surface
            tx = np.matrix([Vt[0,0], Vt[1,0], Vt[2,0], Vt[2,0]])
            ty = np.matrix([Vt[0,1], Vt[1,1], Vt[2,1], Vt[2,1]])
            xy = np.matrix([ [[tx[0,0]], ty[0,0]], [tx[0,1], ty[0,1]], [tx[0,2], ty[0,2]], [tx[0,2], ty[0,2]] ])
            pos = np.zeros([lambda1.shape[0], 2])
            pos[:,0] = (xy[0,0]*lambda1+xy[1,0]*lambda2+xy[2,0]*lambda3).reshape((pos.shape[0]))
            pos[:,1] = (xy[0,1]*lambda1+xy[1,1]*lambda2+xy[2,1]*lambda3).reshape((pos.shape[0]))
            pos = np.round(pos)
            pos[:,0] = np.minimum(pos[:,0], I.shape[0])
            pos[:,1] = np.minimum(pos[:,1], I.shape[1])
            posind=(pos[:,0]-1)+(pos[:,1]-1)*I.shape[0]+1
            # indices
            jind = np.array(jind, dtype=np.intp)
            posind = np.array(posind, dtype=np.intp)
            Jr = Jr.flatten(order='F')
            Jg = Jr.flatten(order='F')
            Jb = Jr.flatten(order='F')
            Ir = Ir.flatten(order='F')
            Ig = Ir.flatten(order='F')
            Ib = Ir.flatten(order='F')

            J = np.zeros((sizep+1, sizep+1, 3)) 
            
            Jr[jind-1] = Ir[posind-1]
            J[:,:,0] = Jr.reshape((J.shape[0], J.shape[0]))

            Jg[jind-1] = Ig[posind-1]
            J[:,:,1] = Jg.reshape((J.shape[0], J.shape[0]))

            Jb[jind-1] = Ib[posind-1]
            J[:,:,2] = Jb.reshape((J.shape[0], J.shape[0]))

            
            
            
        return J


    def calculateBarycentricInterpolationValues(self, sizep):
        # Define a triangle in the upperpart of an square, because only that
        # part is used by the surface function
        x1 = sizep
        y1 = sizep
        x2 = sizep
        y2 = 0
        x3 = 0
        y3 = 0
        detT = (x1-x3)*(y2-y3) - (x2-x3)*(y1-y3)
        [x,y] = np.meshgrid(np.arange(0,sizep+1), np.arange(0,sizep+1))
        x = x.flatten()
        y = y.flatten()
        x = x.reshape((x.shape[0], 1))
        y = y.reshape((y.shape[0], 1))
        lambda1 = ((y2-y3)*(x-x3)+(x3-x2)*(y-y3))/detT
        lambda2 = ((y3-y1)*(x-x3)+(x1-x3)*(y-y3))/detT
        lambda3 = 1-lambda1-lambda2

        [jx,jy] = np.meshgrid(sizep-np.arange(0,sizep+1)+1, sizep-np.arange(0,sizep+1)+1)
        jind = (jx.flatten()-1)+(jy.flatten()-1)*(sizep+1)+1
        return np.reshape(lambda1, (lambda1.shape[0], 1)), np.reshape(lambda2, (lambda2.shape[0], 1)), np.reshape(lambda3, (lambda3.shape[0], 1)), jind
