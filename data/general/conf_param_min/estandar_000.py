import pandas as pd
import numpy as np
import time
import datetime
import sys
import os
import subprocess 


def estandar_000(**kwargs):

    dic = {}
    dic['gmx'] = {}
    dic['user'] = {}
    dic['define'] = {}
    dic['integrator'] = {}
    dic['nsteps'] = {}
    dic['nstenergy'] = {}
    dic['nstlog'] = {}
    dic['nstxout_compressed'] = {}
    dic['constraint_algorithm'] = {}
    dic['constraints'] = {}
    dic['cutoff_scheme'] = {}
    dic['coulombtype'] = {}
    dic['rcoulomb'] = {}
    dic['vdwtype'] = {}
    dic['rvdw'] = {}
    dic['dispcorr'] = {}
    
    GMX = '/usr/local/apps/gromacs-2019.3/build/bin/gmx'
    gmx = kwargs.get('gmx', GMX)
    GMX = gmx
    dic['gmx'][0] = GMX

    USER = 'antonio'
    user = kwargs.get('user', USER)
    USER = user
    dic['user'][0] = USER

    #s = '../../inputs/m'

    path = '../../inputs/mdp_options/input_variable_define.pkl'
    df_mdp_define = pd.read_pickle(path)
    DEFINE = df_mdp_define['define'].loc[0]
    define = kwargs.get('define', DEFINE)
    DEFINE = define
    dic['define'][0] = DEFINE
    
    path = '../../inputs/mdp_options/input_variable_integrator.pkl'
    df_mdp_integrator = pd.read_pickle(path)
    INTEGRATOR = df_mdp_integrator['integrator'].loc[6]
    integrator = kwargs.get('integrator', INTEGRATOR)
    INTEGRATOR = integrator
    dic['integrator'][0] = INTEGRATOR

    path = '../../inputs/mdp_options/input_variable_nsteps.pkl'
    df_mdp_nsteps = pd.read_pickle(path)
    NSTEPS = df_mdp_nsteps['nsteps'].loc[0]
    nsteps = kwargs.get('nsteps', NSTEPS)
    NSTEPS = nsteps
    dic['nsteps'][0] = NSTEPS
    
    path = '../../inputs/mdp_options/input_variable_nstenergy.pkl'
    df_mdp_nstenergy = pd.read_pickle(path)
    NSTENERGY = df_mdp_nstenergy['nstenergy'].loc[0]
    nstenergy = kwargs.get('nstenergy', NSTENERGY)
    NSTENERGY = nstenergy
    dic['nstenergy'][0] = NSTENERGY

    path = '../../inputs/mdp_options/input_variable_nstlog.pkl'
    df_mdp_nstlog = pd.read_pickle(path)
    NSTLOG = df_mdp_nstlog['nstlog'].loc[0]
    nstlog = kwargs.get('nstlog', NSTLOG)
    NSTLOG = nstlog
    dic['nstlog'][0] = NSTLOG

    path = '../../inputs/mdp_options/input_variable_nstxout-compressed.pkl'
    df_mdp_nstxout_compressed = pd.read_pickle(path)
    NSTXOUT_COMPRESSED = df_mdp_nstxout_compressed['nstxout-compressed'].loc[0]
    nstxout_compressed = kwargs.get('nstxout_compressed', NSTXOUT_COMPRESSED)
    NSTXOUT_COMPRESSED = nstxout_compressed
    dic['nstxout_compressed'][0] = NSTXOUT_COMPRESSED

    path = '../../inputs/mdp_options/input_variable_constraint-algorithm.pkl'
    df_mdp_constraint_algorithm = pd.read_pickle(path)
    CONSTRAINT_ALGORITHM = df_mdp_constraint_algorithm['constraint-algorithm'].loc[0]
    constraint_algorithm = kwargs.get('constraint_algorithm', CONSTRAINT_ALGORITHM)
    CONSTRAINT_ALGORITHM = constraint_algorithm
    dic['constraint_algorithm'][0] = CONSTRAINT_ALGORITHM

    path = '../../inputs/mdp_options/input_variable_constraints.pkl'
    df_mdp_constraints = pd.read_pickle(path)
    CONSTRAINTS = df_mdp_constraints['constraints'].loc[1]
    constraints = kwargs.get('constraints', CONSTRAINTS)
    CONSTRAINTS = constraints
    dic['constraints'][0] = CONSTRAINTS

    path = '../../inputs/mdp_options/input_variable_cutoff-scheme.pkl'
    df_mdp_cutoff_scheme = pd.read_pickle(path)
    CUTOFF_SCHEME = df_mdp_cutoff_scheme['cutoff-scheme'].loc[0]
    cutoff_scheme = kwargs.get('cutoff_scheme', CUTOFF_SCHEME)
    CUTOFF_SCHEME = cutoff_scheme
    dic['cutoff_scheme'][0] = CUTOFF_SCHEME

    path = '../../inputs/mdp_options/input_variable_coulombtype.pkl'
    df_mdp_coulombtype = pd.read_pickle(path)
    COULOMBTYPE = df_mdp_coulombtype['coulombtype'].loc[2]
    coulombtype = kwargs.get('coulombtype', COULOMBTYPE)
    COULOMBTYPE = coulombtype
    dic['coulombtype'][0] = COULOMBTYPE

    path = '../../inputs/mdp_options/input_variable_rcoulomb.pkl'
    df_mdp_rcoulomb = pd.read_pickle(path)
    RCOULOMB = df_mdp_rcoulomb['rcoulomb'].loc[0]
    rcoulomb = kwargs.get('rcoulomb', RCOULOMB)
    RCOULOMB = rcoulomb 
    dic['rcoulomb'][0] = RCOULOMB

    path = '../../inputs/mdp_options/input_variable_vdwtype.pkl'
    df_mdp_vdwtype = pd.read_pickle(path)
    VDWTYPE = df_mdp_vdwtype['vdwtype'].loc[0]
    vdwtype = kwargs.get('vdwtype', VDWTYPE)
    VDWTYPE = vdwtype
    dic['vdwtype'][0] = VDWTYPE

    path = '../../inputs/mdp_options/input_variable_rvdw.pkl'
    df_mdp_vdwtype = pd.read_pickle(path)
    RVDW = df_mdp_vdwtype['rvdw'].loc[0]
    rvdw = kwargs.get('rvdw', RVDW)
    RVDW = rvdw
    dic['rvdw'][0] = RVDW

    path = '../../inputs/mdp_options/input_variable_DispCorr.pkl'
    df_mdp_DispCorr = pd.read_pickle(path)
    DISPCORR = df_mdp_DispCorr['DispCorr'].loc[1]
    dispcorr = kwargs.get('dispcorr', DISPCORR)
    DISPCORR = dispcorr
    dic['dispcorr'][0] = DISPCORR


    return pd.DataFrame(dic)









