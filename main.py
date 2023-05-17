

import numpy as np
import math as m
import sys

from GOCI2 import GOCI2_get_lonlat
'''
def main(argv):
    X = np.arange(2780)
    X = (X - 1390) /2780. * 0.000007
    Y = np.arange(2780)
    Y = (Y -1390) /2780. * 0.000007
    print(X, Y)
    PlatformID = 'GOCI2'
    SatLon = 128.2
    SatHeight = 35786000.0
    SatSweep = 'x'

    dlons, dlats = GOCI2_get_lonlat(X, Y, PlatformID, SatLon, SatHeight, SatSweep)

    print(dlons, dlats)
'''
def Rx(theta):
  return np.matrix([[ 1, 0           , 0           ],
                   [ 0, m.cos(theta),-m.sin(theta)],
                   [ 0, m.sin(theta), m.cos(theta)]])
  
def Ry(theta):
  return np.matrix([[ m.cos(theta), 0, m.sin(theta)],
                   [ 0           , 1, 0           ],
                   [-m.sin(theta), 0, m.cos(theta)]])
  
def Rz(theta):
  return np.matrix([[ m.cos(theta), -m.sin(theta), 0 ],
                   [ m.sin(theta), m.cos(theta) , 0 ],
                   [ 0           , 0            , 1 ]])

def GetRxyzCounter(phi, theta, psi):
    #https://www.meccanismocomplesso.org/en/3d-rotations-and-euler-angles-in-python/
    print("phi =", phi)
    print("theta  =", theta)
    print("psi =", psi)
   
    #R = Rz(psi) * Ry(theta) * Rx(phi)
    Rtemp = np.matmul(Ry(theta), Rx(phi)) #순서 체크
    R = np.matmul(Rz(psi),Rtemp)
    print(np.round(R, decimals=2))
    return R

def XYZ2YZX_TRANS_MATRIX():
   trnas_mat = GetRxyzCounter(m.pi/2, 0.0, -m.pi/2)
   return trans_mat

def ConvertCartesianToGEOS(_pECEF, _dRefLongrad, _pGEOSAngle):
    print(_pECEF, _dRefLongrad)
    matRot = np.zeros(3,3)
    matRot = matRot+GetRxyzCounter(0.0,0.0,_dRefLongrad)
    vecGEOS_1 = np.matmul(matRot, _pECEF)
    print(vecGEOS_1)
    vecGEOS_2 = np.cross( XYZ2YZX_TRANS_MATRIX(), vecGEOS_1)
    print(vecGEOS_2)
    x = vecGEOS_2[0]
    y = vecGEOS_2[1]
    z = vecGEOS_2[2]
    dGRMeter = 4.22E+07
    vecGEOS_2[2] = z + dGRMeter
    #z 재설정
    z = vecGEOS_2[2]
    
    dx = m.atan2(x, z)
    dy = m.atan2(-y, m.sqrt(x*x+z*z))
    _pGEOSAngle = np.matrix([dx], [dy])
    return True;

def main(argv):
    #lat, lon degree unit
    lat = np.arange(18)*10 - 90
    lon = np.arange(36)*10 - 180
    print(lat, lon)

    # convert lat,lon to radians
    rlat = lat / 180 * m.pi
    rlon = lon / 180 * m.pi

    # lat,lon -> ECEF(x,y,z) Cartesian
    Re = 6370000  # earth radius
    x_ecef = Re * m.cos(rlat)*m.cos(rlon)
    y_ecef = Re * m.cos(rlat)*m.sin(rlon)
    z_ecef = Re * m.sin(rlat)
    pECEF = np.matrix([x_ecef], [y_ecef], [z_ecef])
    dRefLongr = 128.2 /180*m.pi
    print(pECEF, dRefLongr)

    for epECEF in pECEF:
       ret = ConvertCartesianToGEOS(epECEF, dRefLong, epAngle)
       print(epAngle)
    '''
    ret_pGEOSAngle = ConvertCartesianToGEOS(pECEF, dRefLong, pGEOSAngle)
    print(ret_pGEOSAngle)
    if (ret_pGEOSAngle== True) :
        print(pGEOSAngle)
    else:
       print("Calculation Error")
    '''  



if __name__ == "__main__":
    main(sys.argv[1:])

