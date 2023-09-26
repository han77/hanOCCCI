import numpy as np
import scipy.interpolate

from L2wei_QA_GOCI2 import QAscores_GOCI2

# Always cast as multidimensional arrays, even if only passing one vector/spectrum
# Rrs = np.array([ [0.005, 0.007, 0.009, 0.010, 0.004] ])
Rrs = np.array([ [0.00107, 0.00429, 0.00378, 0.00411, 0.00143, -0.00022, 0.00008, 0.00007], \
    [0.00107, 0.00429, 0.00378, 0.00411, 0.00143, -0.00022, 0.00008, 0.080] ])
# wave = np.array([ [412, 440, 490, 555, 670] ])
wave = np.array([ [412, 443, 490, 510, 555, 620, 660, 680], \
    [412, 443, 490, 510, 555, 620, 660, 680] ])

test_lambda = np.array([412, 443, 490, 510, 555, 620, 660, 680])
test_Rrs = np.empty((Rrs.shape[0],len(test_lambda))) * np.nan

for i, Rrsi in enumerate(Rrs):
    test_Rrs[i,:] = scipy.interpolate.interp1d(wave[i,:], Rrsi)(test_lambda)

maxCos, cos, clusterID, totScore = QAscores_GOCI2(test_Rrs, test_lambda)
print(clusterID, totScore)