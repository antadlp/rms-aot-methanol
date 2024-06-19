import pandas as pd
import numpy as np
import time
import datetime
import sys
import os
import subprocess 


def estandar_nvt_000(**kwargs):

    dic = {}
    dic['gmx'] = {}
    dic['user'] = {}
    dic['integrator'] = {}
    dic['nsteps'] = {}
    dic['dt'] = {}
    dic['nstxout'] = {}
    dic['nstvout'] = {}
    dic['nstenergy'] = {}
    dic['nstlog'] = {}
    dic['constraints'] = {}
    dic['constraint-algorithm'] = {}
    dic['continuation'] = {}
    dic['shake-tol'] = {}
    dic['lincs-order'] = {}
    dic['lincs-iter'] = {}
    dic['lincs-warnangle'] = {}
    dic['morse'] = {}
    dic['cutoff_scheme'] = {}
    dic['ns_type'] = {}
    dic['nstlist'] = {}
    dic['rcoulomb'] = {}
    dic['rvdw'] = {}
    dic['DispCorr'] = {}
    dic['coulombtype'] = {}
    dic['pme-order'] = {}
    dic['fourierspacing'] = {}
    dic['Tcoupl'] = {}
    dic['tc-grps'] = {}
    dic['tau-t'] = {}
    dic['ref-t'] = {}
    dic['pcoupl'] = {}
    dic['pbc'] = {}
    dic['gen-vel'] = {}

    
    GMX = '/usr/local/apps/gromacs-2019.3/build/bin/gmx'
    gmx = kwargs.get('gmx', GMX)
    GMX = gmx
    dic['gmx'][0] = GMX

    USER = 'antonio'
    user = kwargs.get('user', USER)
    USER = user
    dic['user'][0] = USER
    
    path = '../data/inputs/mdp_options/input_variable_integrator.pkl'
    df_mdp_integrator = pd.read_pickle(path)
    INTEGRATOR = df_mdp_integrator['integrator'].loc[1]
    integrator = kwargs.get('integrator', INTEGRATOR)
    INTEGRATOR = integrator
    dic['integrator'][0] = INTEGRATOR

    path = '../data/inputs/mdp_options/input_variable_nsteps.pkl'
    df_mdp_nsteps = pd.read_pickle(path)
    NSTEPS = df_mdp_nsteps['nsteps'].loc[0]
    nsteps = kwargs.get('nsteps', NSTEPS)
    NSTEPS = nsteps
    dic['nsteps'][0] = NSTEPS

    path = '../data/inputs/mdp_options/input_variable_dt.pkl'
    df_mdp_dt = pd.read_pickle(path)
    DT = df_mdp_dt['dt'].loc[0]
    dt = kwargs.get('dt', DT)
    DT= dt 
    dic['dt'][0] = DT

    path = '../data/inputs/mdp_options/input_variable_nstxout.pkl'
    df_mdp_nstxout = pd.read_pickle(path)
    NSTXOUT = df_mdp_nstxout['nstxout'].loc[0]
    nstxout = kwargs.get('nstxout', NSTXOUT)
    NSTXOUT = nstxout
    dic['nstxout'][0] = NSTXOUT

    path = '../data/inputs/mdp_options/input_variable_nstvout.pkl'
    df_mdp_nstvout = pd.read_pickle(path)
    NSTVOUT = df_mdp_nstvout['nstvout'].loc[0]
    nstvout = kwargs.get('nstvout', NSTVOUT)
    NSTVOUT = nstvout
    dic['nstvout'][0] = NSTVOUT

    path = '../data/inputs/mdp_options/input_variable_nstenergy.pkl'
    df_mdp_nstenergy = pd.read_pickle(path)
    NSTENERGY = df_mdp_nstenergy['nstenergy'].loc[0]
    nstenergy = kwargs.get('nstenergy', NSTENERGY)
    NSTENERGY = nstenergy
    dic['nstenergy'][0] = NSTENERGY

    path = '../data/inputs/mdp_options/input_variable_nstlog.pkl'
    df_mdp_nstlog = pd.read_pickle(path)
    NSTLOG = df_mdp_nstlog['nstlog'].loc[0]
    nstlog = kwargs.get('nstlog', NSTLOG)
    NSTLOG = nstlog
    dic['nstlog'][0] = NSTLOG

    path = '../data/inputs/mdp_options/input_variable_constraints.pkl'
    df_mdp_constraints = pd.read_pickle(path)
    CONSTRAINTS = df_mdp_constraints['constraints'].loc[2]
    constraints = kwargs.get('constraints', CONSTRAINTS)
    CONSTRAINTS = constraints
    dic['constraints'][0] = CONSTRAINTS

    path = '../data/inputs/mdp_options/input_variable_constraint-algorithm.pkl'
    df_mdp_constraint_algorithm = pd.read_pickle(path)
    CONSTRAINT_ALGORITHM = df_mdp_constraint_algorithm['constraint-algorithm'].loc[0]
    constraint_algorithm = kwargs.get('constraint_algorithm', CONSTRAINT_ALGORITHM)
    CONSTRAINT_ALGORITHM = constraint_algorithm
    dic['constraint-algorithm'][0] = CONSTRAINT_ALGORITHM

    path = '../data/inputs/mdp_options/input_variable_continuation.pkl'
    df_mdp_continuation = pd.read_pickle(path)
    CONTINUATION = df_mdp_continuation['continuation'].loc[0]
    continuation = kwargs.get('continuation', CONTINUATION)
    CONTINUATION = continuation
    dic['continuation'][0] = CONTINUATION

    path = '../data/inputs/mdp_options/input_variable_shake-tol.pkl'
    df_mdp_shake_tol = pd.read_pickle(path)
    SHAKE_TOL = df_mdp_shake_tol['shake-tol'].loc[0]
    shake_tol = kwargs.get('shake_tol', SHAKE_TOL)
    SHAKE_TOL = shake_tol
    dic['shake-tol'][0] = SHAKE_TOL

    path = '../data/inputs/mdp_options/input_variable_lincs-order.pkl'
    df_mdp_lincs_order = pd.read_pickle(path)
    LINCS_ORDER = df_mdp_lincs_order['lincs-order'].loc[0]
    lincs_order = kwargs.get('lincs-order', LINCS_ORDER)
    LINCS_ORDER = lincs_order
    dic['lincs-order'][0] = LINCS_ORDER

    path = '../data/inputs/mdp_options/input_variable_lincs-iter.pkl'
    df_mdp_lincs_iter = pd.read_pickle(path)
    LINCS_ITER = df_mdp_lincs_iter['lincs-iter'].loc[0]
    lincs_iter = kwargs.get('lincs-iter', LINCS_ITER)
    LINCS_ITER = lincs_iter
    dic['lincs-iter'][0] = LINCS_ITER

    path = '../data/inputs/mdp_options/input_variable_lincs-warnangle.pkl'
    df_mdp_lincs_warnangle = pd.read_pickle(path)
    LINCS_WARNANGLE = df_mdp_lincs_warnangle['lincs-warnangle'].loc[0]
    lincs_warnangle = kwargs.get('lincs-warnangle', LINCS_WARNANGLE)
    LINCS_WARNANGLE = lincs_warnangle
    dic['lincs-warnangle'][0] = LINCS_WARNANGLE

    path = '../data/inputs/mdp_options/input_variable_morse.pkl'
    df_mdp_morse = pd.read_pickle(path)
    MORSE = df_mdp_morse['morse'].loc[0]
    morse = kwargs.get('morse', MORSE)
    MORSE = morse
    dic['morse'][0] = MORSE

    path = '../data/inputs/mdp_options/input_variable_cutoff-scheme.pkl'
    df_mdp_cutoff_scheme = pd.read_pickle(path)
    CUTOFF_SCHEME = df_mdp_cutoff_scheme['cutoff-scheme'].loc[0]
    cutoff_scheme = kwargs.get('cutoff_scheme', CUTOFF_SCHEME)
    CUTOFF_SCHEME = cutoff_scheme
    dic['cutoff_scheme'][0] = CUTOFF_SCHEME

    path = '../data/inputs/mdp_options/input_variable_ns_type.pkl'
    df_mdp_ns_type = pd.read_pickle(path)
    NS_TYPE = df_mdp_ns_type['ns_type'].loc[0]
    ns_type = kwargs.get('ns_type', NS_TYPE)
    NS_TYPE = ns_type
    dic['ns_type'][0] = NS_TYPE

    path = '../data/inputs/mdp_options/input_variable_nstlist.pkl'
    df_mdp_nstlist = pd.read_pickle(path)
    NSTLIST = df_mdp_nstlist['nstlist'].loc[3]
    nstlist = kwargs.get('nstlist', NSTLIST)
    NSTLIST = nstlist
    dic['nstlist'][0] = NSTLIST

    path = '../data/inputs/mdp_options/input_variable_rcoulomb.pkl'
    df_mdp_rcoulomb = pd.read_pickle(path)
    RCOULOMB = df_mdp_rcoulomb['rcoulomb'].loc[1]
    rcoulomb = kwargs.get('rcoulomb', RCOULOMB)
    RCOULOMB = rcoulomb 
    dic['rcoulomb'][0] = RCOULOMB

    path = '../data/inputs/mdp_options/input_variable_rvdw.pkl'
    df_mdp_vdwtype = pd.read_pickle(path)
    RVDW = df_mdp_vdwtype['rvdw'].loc[1]
    rvdw = kwargs.get('rvdw', RVDW)
    RVDW = rvdw
    dic['rvdw'][0] = RVDW

    path = '../data/inputs/mdp_options/input_variable_DispCorr.pkl'
    df_mdp_DispCorr = pd.read_pickle(path)
    DISPCORR = df_mdp_DispCorr['DispCorr'].loc[1]
    dispcorr = kwargs.get('dispcorr', DISPCORR)
    DISPCORR = dispcorr
    dic['DispCorr'][0] = DISPCORR

    path = '../data/inputs/mdp_options/input_variable_coulombtype.pkl'
    df_mdp_coulombtype = pd.read_pickle(path)
    COULOMBTYPE = df_mdp_coulombtype['coulombtype'].loc[0]
    coulombtype = kwargs.get('coulombtype', COULOMBTYPE)
    COULOMBTYPE = coulombtype
    dic['coulombtype'][0] = COULOMBTYPE


    path = '../data/inputs/mdp_options/input_variable_pme-order.pkl'
    df_mdp_pme_order = pd.read_pickle(path)
    PME_ORDER = df_mdp_pme_order['pme-order'].loc[0]
    pme_order = kwargs.get('pme-order', PME_ORDER)
    PME_ORDER = pme_order
    dic['pme-order'][0] = PME_ORDER

    path = '../data/inputs/mdp_options/input_variable_fourierspacing.pkl'
    df_mdp_fourierspacing = pd.read_pickle(path)
    FOURIERSPACING = df_mdp_fourierspacing['fourierspacing'].loc[0]
    fourierspacing = kwargs.get('fourierspacing', FOURIERSPACING)
    FOURIERSPACING = fourierspacing
    dic['fourierspacing'][0] = FOURIERSPACING

    path = '../data/inputs/mdp_options/input_variable_Tcoupl.pkl'
    df_mdp_Tcoupl = pd.read_pickle(path)
    TCOUPL = df_mdp_Tcoupl['Tcoupl'].loc[2]
    Tcoupl = kwargs.get('Tcoupl', TCOUPL)
    TCOUPL = Tcoupl
    dic['Tcoupl'][0] = TCOUPL

    path = '../data/inputs/mdp_options/input_variable_tc-grps.pkl'
    df_mdp_tc_grps = pd.read_pickle(path)
    TC_GRPS = df_mdp_tc_grps['tc-grps'].loc[0]
    tc_grps = kwargs.get('tc-grps', TC_GRPS)
    TC_GRPS = tc_grps
    dic['tc-grps'][0] = TC_GRPS

    path = '../data/inputs/mdp_options/input_variable_tau-t.pkl'
    df_mdp_tau_t = pd.read_pickle(path)
    TAU_T = df_mdp_tau_t['tau-t'].loc[0]
    tau_t = kwargs.get('tau_t', TAU_T)
    TAU_T = tau_t
    dic['tau-t'][0] = TAU_T

    path = '../data/inputs/mdp_options/input_variable_ref-t.pkl'
    df_mdp_ref_t = pd.read_pickle(path)
    REF_T = df_mdp_ref_t['ref-t'].loc[0]
    ref_t = kwargs.get('ref_t', REF_T)
    REF_T = ref_t
    dic['ref-t'][0] = REF_T

    path = '../data/inputs/mdp_options/input_variable_pcoupl.pkl'
    df_mdp_pcoupl = pd.read_pickle(path)
    PCOUPL = df_mdp_pcoupl['pcoupl'].loc[0]
    pcoupl = kwargs.get('pcoupl', PCOUPL)
    PCOUPL = pcoupl
    dic['pcoupl'][0] = PCOUPL

    path = '../data/inputs/mdp_options/input_variable_pbc.pkl'
    df_mdp_pbc = pd.read_pickle(path)
    PBC = df_mdp_pbc['pbc'].loc[0]
    pbc = kwargs.get('pbc', PBC)
    PBC = pbc
    dic['pbc'][0] = PBC

    path = '../data/inputs/mdp_options/input_variable_gen-vel.pkl'
    df_mdp_gen_vel = pd.read_pickle(path)
    GEN_VEL = df_mdp_gen_vel['gen-vel'].loc[0]
    gen_vel = kwargs.get('gen_vel', GEN_VEL)
    GEN_VEL = gen_vel
    dic['gen-vel'][0] = GEN_VEL


    return pd.DataFrame(dic)









