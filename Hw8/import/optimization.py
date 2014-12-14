import numpy as np
import cv, cv2
from scipy.optimize import leastsq
from numpy import array, dot, zeros


def calculate_projected_corners(corners_corresp, P):
    corners = []
    world_coord = np.zeros(4)
    row = len(corners_corresp)
    column = len(corners_corresp[0])
    
    d_geom = np.zeros(row*column*2)
    #print row, column
    #print "P is {}".format(P)
    count = 0
    for i in range(row):
        for j in range(column):
            world_coord[0] = j
            world_coord[1] = i
            #print "world coord is {}, {}".format(world_coord[0], world_coord[1])
            world_coord[2] = 0
            world_coord[3] = 1
                
            # compute the reprojection :
            corners_project = np.dot(P, world_coord)
            corners_project[0] = corners_project[0]/corners_project[2]
            corners_project[1] = corners_project[1]/corners_project[2]
            corners.append((corners_project[0], corners_project[1]))
            d_geom[count] = corners_project[0] - corners_corresp[i][j][0]
            d_geom[count+1] = corners_project[1] - corners_corresp[i][j][1]
            count += 2
    return corners, d_geom

def refine_param(K, Rts, corners_set, k1, k2):
    numIntrinsicParams = 7
    def ConvertToParams (K, Rts, k1, k2):
        r_vec = np.zeros ((1 ,3))
        rtsIdxStart = numIntrinsicParams
        params = np.zeros ( rtsIdxStart + len (Rts ) * 6 )
        params [0:3] = K[0 ,:]
        params [3] = K[1 , 1]
        params [4] = K[1 , 2]
        params [5] = k1
        params [6] = k2
        for i in range(len(Rts)):
            R = Rts[i]
            cv.Rodrigues2 (cv.fromarray(R), cv.fromarray(r_vec))
            params[ rtsIdxStart : rtsIdxStart +3] = r_vec[0] # turn r vec to 1?D
            rtsIdxStart += 3
            t_vec = Rts [i] [ : , 3 ]
            params [rtsIdxStart : rtsIdxStart +3] = t_vec
            rtsIdxStart += 3
        return params
    
    def ConvertFromParams ( params ) :
        k_vec = params [0: 5]
        K = array ([[ k_vec [0] , k_vec [1] , k_vec [2]] ,
        [0 , k_vec [3] , k_vec [4]] , [0 , 0 , 1]])
        k1 = params[5]
        k2 = params[6]
        rtParams = params [numIntrinsicParams : ]
        
        rtParams = rtParams.reshape ( len ( rtParams ) /6, 6)
        Rts = [ ]
        r_vec = np.zeros ((1 ,3)) # need t o be 2D f o r R od ri gue s 2
        for rtIdx in xrange ( len ( rtParams ) ) :
            params = rtParams [ rtIdx ]
            r_vec [0] = (params [ 0: 3] ) # r v e c i s 2D
            R = np.zeros ((3 ,3) ) # the rotation 3x3 matrix
            cv.Rodrigues2 (cv.fromarray ( r_vec ) , cv . fromarray (R) )
            t_vec = params [ 3: 6] # the tranlstion vector
            Rt = np.zeros ( ( 3 , 4 ) )
            Rt [ : , 0 ] = R[ : , 0 ]
            Rt [ : , 1 ] = R[ : , 1 ]
            Rt [ : , 2 ] = R[ : , 2 ]
            Rt [ : , 3 ] = t_vec
            Rts.append (Rt)
        return (K, Rts , k1 , k2 )
    def residuals(params) :
        # unpack the calibration parameters :
        (K, Rts , k1 , k2 ) = ConvertFromParams ( params )
        # xo = K[ 0 , 2]; yo = K[ 1 , 2] # the center pixel of image
        allRes = []
        for i in xrange ( len (Rts ) ) :
        
            P = np.dot (K, Rts[i] ) 
            # get points on the model plan as 4?vectors and image points as
            # 3?vector , both in homogeous coordinates
            corners_corresp = corners_set[i]
            corners_proj, d_geom = calculate_projected_corners(corners_corresp, P)
            allRes.append (d_geom)
        
        res = [row for resSet in allRes for row in resSet]
        #print max(res)
        return res
    
    initParams = ConvertToParams (K, Rts , k1 , k2 )
    #print "intial Param is {}".format(initParams)
    plsq = leastsq( residuals , initParams )
    finalParams = plsq [0]
    #print "final Param is {}".format(finalParams)
    return ConvertFromParams (finalParams)
