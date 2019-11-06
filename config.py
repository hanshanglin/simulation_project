import logging
import numpy as np
#from simulation_random import two_normal_ran, exp_ran
INTMAX = 100000000000
OUTPUTLEVEL = logging.DEBUG
MAX_WAITING_QUEUE = 25
MAX_MACHINE_NUM = 10
np.random.seed(1000)


def SPINNING_RV():
    rv = int(np.around(np.random.normal(240, np.sqrt(120))))
    while rv<=0:
        rv = int(np.around(np.random.normal(240, np.sqrt(120))))
    return rv


# two_normal_ran(480, 200)[0]
def WEAVING_RV(): 
    rv = int(np.around(np.random.normal(480, np.sqrt(120))))
    while rv<=0:
        rv = int(np.around(np.random.normal(480, np.sqrt(200))))
    return rv


def FINISHING_RV():
    rv = int(np.around(np.random.exponential(120)))
    while rv<=0:
        rv = int(np.around(np.random.exponential(120)))
    return rv 


def PACKING_RV():
    rv = int(np.around(np.random.exponential(360)))
    while rv<=0:
        rv = int(np.around(np.random.exponential(120)))
    return rv 



RV_list = [SPINNING_RV, WEAVING_RV, FINISHING_RV, PACKING_RV]
TEMP_TEST = 0
