'''
    This file contains all constants values of the general settings. 
'''

from dataclasses import dataclass

#################### Scale factors ####################
@dataclass
class Classification:
    HIGH:   int  = 10 # Must be a positive integer
    MEDIUM: int  =  5 # Must be a positive integer
    LOW:    int  =  1 # Must be a positive integer
#######################################################