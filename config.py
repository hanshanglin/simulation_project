import logging
from simulation_random import two_normal_ran, exp_ran
INTMAX = 100000000000
OUTPUTLEVEL = logging.INFO
MAX_WAITING_QUEUE = 25
MAX_MACHINE_NUM = 10
def SPINNING_RV(): return two_normal_ran(240, 120)[0]
def WEAVING_RV(): return two_normal_ran(480, 200)[0]
def FINISHING_RV(): return exp_ran(120)
def PACKING_RV(): return exp_ran(360)
RV_list = [SPINNING_RV, WEAVING_RV, FINISHING_RV, PACKING_RV]
TEMP_TEST = 0