import pandas as pd
import numpy as np
import time
import datetime
import sys
import os
import subprocess 
import getpass


PATH_GRL1 = "../data/general/conf_grompp_params"

sys.path.append(PATH_GRL1)

from estandar_min_000 import *
from estandar_min_001 import *
from estandar_min_002 import *
from estandar_nvt_000 import *
from estandar_npt_000 import *

class call_grompp_conf(object):
    
    def call_estandar_min_000(self, **kwargs):
        
        dic = {}
        NSTEPS = kwargs.get('nsteps', 'NULL')

        if NSTEPS != 'NULL':
            dic['nsteps'] = NSTEPS

        return estandar_min_000(**dic)

    def call_estandar_min_001(self, **kwargs):
        
        dic = {}
        NSTEPS = kwargs.get('nsteps', 'NULL')
        
        if NSTEPS != 'NULL':
            dic['nsteps'] = NSTEPS
        return estandar_min_001(**dic)

    def call_estandar_min_002(self, **kwargs):
        
        dic = {}
        NSTEPS = kwargs.get('nsteps', 'NULL')
        
        if NSTEPS != 'NULL':
            dic['nsteps'] = NSTEPS
        return estandar_min_002(**dic)

    def call_estandar_nvt_000(self, **kwargs):
        
        dic = {}
        NSTEPS = kwargs.get('nsteps', 'NULL')
        DT = kwargs.get('dt', 'NULL')
        RCOULOMB = kwargs.get('rcoulomb', 'NULL')
        RVDW = kwargs.get('rvdw', 'NULL')
        TC_GRPS = kwargs.get('tc_grps', 'NULL')
        NSTXOUT = kwargs.get('nstxout', 'NULL')
        NSTVOUT = kwargs.get('nstvout', 'NULL')
        NSTENERGY = kwargs.get('nstenergy', 'NULL')
        NSTLOG = kwargs.get('nstlog', 'NULL')
        PBC = kwargs.get('pbc', 'NULL')
        TEMP = kwargs.get('temp', 'NULL')
        
        
        if NSTEPS != 'NULL':
            dic['nsteps'] = NSTEPS

        if DT != 'NULL':
            dic['dt'] = DT
            
        if RCOULOMB != 'NULL':
            dic['rcoulomb'] = RCOULOMB
            
        if RVDW != 'NULL':
            dic['rvdw'] = RVDW
            
        if TC_GRPS != 'NULL':
            dic['tc-grps'] = TC_GRPS
            
        if NSTXOUT != 'NULL':
            dic['nstxout'] = NSTXOUT            
            
        if NSTVOUT != 'NULL':
            dic['nstvout'] = NSTVOUT      
            
        if NSTENERGY != 'NULL':
            dic['nstenergy'] = NSTENERGY
            
        if NSTLOG != 'NULL':
            dic['nstlog'] = NSTLOG       
            
        if PBC != 'NULL':
            dic['pbc'] = PBC
            
        if TEMP != 'NULL':
            dic['ref_t'] = TEMP 
        
        dic['rlist'] = 1.5

        return estandar_nvt_000(**dic)

    def call_estandar_npt_000(self, **kwargs):
        
        dic = {}
        NSTEPS = kwargs.get('nsteps', 'NULL')
        DT = kwargs.get('dt', 'NULL')
        RCOULOMB = kwargs.get('rcoulomb', 'NULL')
        RVDW = kwargs.get('rvdw', 'NULL')
        TC_GRPS = kwargs.get('tc_grps', 'NULL')
        NSTXOUT = kwargs.get('nstxout', 'NULL')
        NSTVOUT = kwargs.get('nstvout', 'NULL')
        NSTENERGY = kwargs.get('nstenergy', 'NULL')
        NSTLOG = kwargs.get('nstlog', 'NULL')
        PBC = kwargs.get('pbc', 'NULL')
        TEMP = kwargs.get('temp', 'NULL')
        PCOULP = kwargs.get("pcoupl", "NULL")
        CONSTRAINT_ALGORITHM = kwargs.get('constraint_algorithm', "NULL")
        COULOMBTYPE = kwargs.get('coulombtype', "NULL")     
        
       
        if NSTEPS != 'NULL':
            dic['nsteps'] = NSTEPS

        if DT != 'NULL':
            dic['dt'] = DT
            
        if RCOULOMB != 'NULL':
            dic['rcoulomb'] = RCOULOMB
            
        if RVDW != 'NULL':
            dic['rvdw'] = RVDW
            
        if TC_GRPS != 'NULL':
            dic['tc-grps'] = TC_GRPS
            
        if NSTXOUT != 'NULL':
            dic['nstxout'] = NSTXOUT            
            
        if NSTVOUT != 'NULL':
            dic['nstvout'] = NSTVOUT      
            
        if NSTENERGY != 'NULL':
            dic['nstenergy'] = NSTENERGY
            
        if NSTLOG != 'NULL':
            dic['nstlog'] = NSTLOG 
            
        if PBC != 'NULL':
            dic['pbc'] = PBC
            
        if TEMP != 'NULL':
            dic['ref_t'] = TEMP
            
        if PCOULP != 'NULL':
            dic['pcoupl'] = PCOULP   
            
        if CONSTRAINT_ALGORITHM != 'NULL':
            dic['constraint_algorithm'] = CONSTRAINT_ALGORITHM
            
        if COULOMBTYPE != 'NULL':
            dic['coulombtype'] = COULOMBTYPE            
            
        dic['rlist'] = 1.5

        return estandar_npt_000(**dic)


    def call_estandar_nvt_001(self, **kwargs):
       
        dic = {}
        NSTEPS = kwargs.get('nsteps', 'NULL')
        DT = kwargs.get('dt', 'NULL')
        RCOULOMB = kwargs.get('rcoulomb', 'NULL')
        RVDW = kwargs.get('rvdw', 'NULL')
        TC_GRPS = kwargs.get('tc_grps', 'NULL')
        NSTXOUT = kwargs.get('nstxout', 'NULL')
        NSTVOUT = kwargs.get('nstvout', 'NULL')
        NSTENERGY = kwargs.get('nstenergy', 'NULL')
        NSTLOG = kwargs.get('nstlog', 'NULL')
        PBC = kwargs.get('pbc', 'NULL')
        TEMP = kwargs.get('temp', 'NULL')
        CONSTRAINT_ALGORITHM = kwargs.get('constraint_algorithm', "NULL")
        COULOMBTYPE = kwargs.get('coulombtype', "NULL")     
        
       
        if NSTEPS != 'NULL':
            dic['nsteps'] = NSTEPS

        if DT != 'NULL':
            dic['dt'] = DT
            
        if RCOULOMB != 'NULL':
            dic['rcoulomb'] = RCOULOMB
            
        if RVDW != 'NULL':
            dic['rvdw'] = RVDW
            
        if TC_GRPS != 'NULL':
            dic['tc-grps'] = TC_GRPS
            
        if NSTXOUT != 'NULL':
            dic['nstxout'] = NSTXOUT            
            
        if NSTVOUT != 'NULL':
            dic['nstvout'] = NSTVOUT      
            
        if NSTENERGY != 'NULL':
            dic['nstenergy'] = NSTENERGY
            
        if NSTLOG != 'NULL':
            dic['nstlog'] = NSTLOG 
            
        if PBC != 'NULL':
            dic['pbc'] = PBC
            
        if TEMP != 'NULL':
            dic['ref_t'] = TEMP
            
        if CONSTRAINT_ALGORITHM != 'NULL':
            dic['constraint_algorithm'] = CONSTRAINT_ALGORITHM
            
        if COULOMBTYPE != 'NULL':
            dic['coulombtype'] = COULOMBTYPE            
            
        dic['rlist'] = 1.5

        return estandar_nvt_000(**dic)



