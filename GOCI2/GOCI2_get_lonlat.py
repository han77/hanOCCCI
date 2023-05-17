# 2023.05.17 hhj

import datetime
import glob
import os
import re
import warnings

import numpy as np
from pyproj import Proj

warnings.filterwarnings('ignore')

#-----------------------------------------------------------------------------------------------------------------------------------

def GOCI2_get_lonlat(X, Y, PlatformID, SatLon, SatHeight, SatSweep, fmt=np.float32):

    '''

    Calculates the longitude and latitude of the center of the pixels,
    corresponding to the satellite image, using the fixed grid East/West and
    North/South scanning angle in radians of pixels.


    Parameters
    ----------
    X : ndarray
        A scalar 1-D array with the fixed grid East/West scanning
        angle in radians.

    Y : ndarray
        A scalar 1-D array with the fixed grid North/South scanning
        angle in radians.

    PlatformID : str
        Platform ID of satelite. Example: 'G16' or 'G17' or "GOCI2"

    SatLon : float
        Longitude of satellite in the nadir.

    SatHeight : float
        Height of satellite in meters.

    SatSweep : str
        Sweep-angle axis.

    fmt : dtype, optional, default np.float32
        The type of the returns.


    Returns
    -------
    Lons : dict
        Scalar 2-D array with the center longitude of the pixels.
        Undefined data are set as -999.99.

    Lats : dict
        Scalar 2-D array with the center latitude of the pixels.
        Undefined data are set as -999.99.

    '''

    X = X[:]*SatHeight
    Y = Y[:]*SatHeight
    X, Y = np.meshgrid(X, Y)
    proj = Proj(proj='geos', h=SatHeight, lon_0=SatLon, sweep=SatSweep)
    Lons, Lats = proj(X, Y, inverse=True)

    if PlatformID == 'G17':
        Lons = np.where(Lons>0,Lons-360,Lons)

    Lons = np.where((Lons>=-360.0)&(Lons<=360.0)&(Lats>=-90.0)&(Lats<=90.0),Lons,-999.99).astype(fmt)
    Lats = np.where((Lons>=-360.0)&(Lons<=360.0)&(Lats>=-90.0)&(Lats<=90.0),Lats,-999.99).astype(fmt)

    dict_Lons = {'long_name':'Longitude of center of pixels', 'standard_name':'pixels center longitude',
                 'units':'degrees_east', 'undef':-999.99, 'axis':'YX', 'dimensions':('y','x'), 'data':Lons}

    dict_Lats = {'long_name':'Latitude of center of pixels', 'standard_name':'pixels center latitude',
                 'units':'degrees_north', 'undef':-999.99, 'axis':'YX', 'dimensions':('y','x'), 'data':Lats}

    return dict_Lons, dict_Lats
