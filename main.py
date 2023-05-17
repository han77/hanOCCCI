
import sys
from os import path

if __name__ == '__main__':
	if __package__ is None:
		print(path.dirname( path.dirname( path.abspath(__file__) ) ))
		sys.path.append(path.dirname( path.dirname( path.abspath(__file__) ) ))
		from .GOCI2.GOCI2_get_lonlat import *
    
else:
    from .GOCI2 import *

a = GOCI2_get_lonlat()
