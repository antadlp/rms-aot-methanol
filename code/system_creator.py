import pandas as pd
import numpy as np
import time
import datetime
import sys
import os
import subprocess 
from herramientas import *

herr = herramientas()



def sys_isooctano(**kwargs):
    
    dP_LVL1 = kwargs.get("dP_LVL1", {})

    num_mols = kwargs.get('num_mols', 500) # 333
    NUM_MOLS = num_mols

    dens = kwargs.get('dens', 0.692) # https://en.wikipedia.org/wiki/2,2,4-Trimethylpentane
    DENS = dens
    
    GMX = '/usr/local/apps/gromacs-2019.3/build/bin/gmx'
    gmx = kwargs.get('gmx', GMX)
    de = kwargs.get("de", 0.35)

    PATH_ISOPDB = "../data/pdbs/G016_unitedatom_optimised_geometry.pdb"
    PATH_ISOXYZ = "../data/xyz/isooctane.xyz"
    path_isoc_pdb_united = kwargs.get('path_isoc_pdb_united', PATH_ISOPDB)      # paths de donde sea
    path_isoc_xyz_allatom = kwargs.get('path_isoc_xyz_allatom', PATH_ISOXYZ) # paths de donde sea
    
    PATH_GRL1 = dP_LVL1['GRL1']

    cmd = ['mkdir', '-p', PATH_GRL1]
    process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)

    PATH_INDIVIDUAL_STRUCTURES = os.path.join(PATH_GRL1, 'individual_structures')
    cmd = ['mkdir', '-p', PATH_INDIVIDUAL_STRUCTURES]
    process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)

    PATH_CELDAS_INICIALES = os.path.join(PATH_GRL1, 'celdas_iniciales')
    cmd = ['mkdir', '-p', PATH_CELDAS_INICIALES]
    process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)

    PATH_ISOC_XYZ_ALLATOM = os.path.join(PATH_INDIVIDUAL_STRUCTURES, 'isoctano_allatom.xyz')
    PATH_ISOC_PDB_UNITED = os.path.join(PATH_INDIVIDUAL_STRUCTURES, 'isoctano_united.pdb')
    PATH_CELDA0 = os.path.join(PATH_CELDAS_INICIALES, 'celda0.gro')

    cmd = ['cp', path_isoc_pdb_united, PATH_ISOC_PDB_UNITED]
    process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)
    cmd = ['cp', path_isoc_xyz_allatom, PATH_ISOC_XYZ_ALLATOM]
    process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)

    # Creando celda 0 
    # gmx insert-molecules -ci isooctane_united.pdb -nmol 1000 -box 14 14 14 -o caja_isooctano.gro
    # lado_celda0 queda fijado con NUM_MOLS
    lado_celda0 = herr.vol_cube_length(PATH_ISOC_XYZ_ALLATOM, DENS, NUM_MOLS)
    lado_celda0 = np.around(lado_celda0, decimals=4)
    lado_celda0 = kwargs.get("lado_celda0", lado_celda0)
    
    cmd = [gmx, 'insert-molecules',
           '-ci', PATH_ISOC_PDB_UNITED,
           '-nmol', NUM_MOLS,
           '-box', lado_celda0, lado_celda0, lado_celda0,
           '-o', PATH_CELDA0]
    
    cmd = [str(item) for item in cmd]
    process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)
    
    # Haciendo grande la caja
    L = lado_celda0
    cmd = [gmx, 'editconf',
           '-f', PATH_CELDA0,          # input 
           '-box', L+de, L+de, L+de,      # input
           '-o', PATH_CELDA0]          # output
    cmd = [str(item) for item in cmd]
    process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)    

    return PATH_CELDA0
    
    
def rm_packmol_nomed(**kwargs):
    
    PATH_PDB_AOT = "../data/inputs/reverce_micelles/pdbs/63UD_allatom_optimised_geometry2.pdb"
    PATH_PDB_NA = "../data/inputs/reverce_micelles/pdbs/E0XM_allatom_optimised_geometry.pdb"
    PATH_PDB_H2O = "../data/inputs/reverce_micelles/pdbs/spce_hoh.pdb"    
    
    USER = getpass.getuser()
    user = kwargs.get('user', USER) #<--
    
    PATH_GRL = '/home/{}/Documents/gromacs-data-analysis/'.format(user)
    path_grl = kwargs.get('path_grl', PATH_GRL) #<--
    
    num_aot = kwargs.get("num_aot", 50) #<--
    num_h2o = kwargs.get("num_h2o", 300) #<--
    num_na = kwargs.get("num_na", num_aot) #<--
    
    r_inner = kwargs.get("r_inner", 16.0) # determina tamaño #<--
    r_adjust = kwargs.get("r_adjust", 10.0) # distancia desde r_inner #<--
    
    dr_h2o = kwargs.get("dr_h2o", 0.5) #<--
    dr_na = kwargs.get("dr_na", dr_h2o) #<--
    
    tol = kwargs.get("tol", 2.0) #<--
    
    PATH_PDB_AOT = kwargs.get("path_pdb_aot", PATH_PDB_AOT) #<--
    PATH_PDB_NA = kwargs.get("path_pdb_na", PATH_PDB_NA) #<--
    PATH_PDB_H2O = kwargs.get("path_pdb_h2o", PATH_PDB_H2O) #<--
    
    path_outpack = kwargs.get("path_outpack", 'packmol_input_rm.inp') #<--
    path_outpdb = kwargs.get("path_outpdb", 'rm_nomed_0x.pdb') #<--

    f = open(path_outpack, 'w')
    
    r_outter = r_inner + r_adjust
    r_h2o = r_inner - dr_h2o
    r_na = r_inner - dr_na

    f.write('tolerance 2.0 \n')
    f.write('\n')
    pathaot = os.path.split(PATH_PDB_AOT)[-1]
    f.write('structure {}\n'.format(pathaot))
    f.write('  number {}\n'.format(num_aot))
    f.write('  atoms 31\n')
    f.write('    inside sphere 0. 0. 0. {} \n'.format(r_inner))
    f.write('  end atoms\n')
    f.write('  atoms 62\n')
    f.write('    outside sphere 0. 0. 0. {}\n'.format(r_outter))
    f.write('  end atoms\n')
    f.write('end structure \n')
    f.write('\n')
    pathh2o = os.path.split(PATH_PDB_H2O)[-1]
    f.write('structure {}\n'.format(pathh2o))
    f.write('   number {}\n'.format(num_h2o))
    f.write('   inside sphere 0. 0. 0. {}\n'.format(r_h2o))
    f.write('end structure\n')
    f.write('\n')
    pathna = os.path.split(PATH_PDB_NA)[-1]
    f.write('structure {}\n'.format(pathna))
    f.write('   number {}\n'.format(num_na))
    f.write('   inside sphere 0. 0. 0. {}\n'.format(r_na))
    f.write('end structure\n')
    f.write('\n')
    pathoutpdb = os.path.split(path_outpdb)[-1]
    f.write('output {}\n'.format(path_outpdb))

    f.close()  
    
    dic = {}
    dic['path_grl'] = path_grl
    dic['path_pdb_aot'] = PATH_PDB_AOT
    dic['path_pdb_na'] = PATH_PDB_NA
    dic['path_pdb_h2o'] = PATH_PDB_H2O
    dic['path_outpack'] = path_outpack
    dic['path_outpdb'] = path_outpdb
    
    return dic
    
    
    
    
def create_packmol_rm_nomed(**kwargs):
    
    PATH_PDB_AOT = "../data/inputs/reverce_micelles/pdbs/63UD_allatom_optimised_geometry2.pdb"
    PATH_PDB_NA = "../data/inputs/reverce_micelles/pdbs/E0XM_allatom_optimised_geometry.pdb"
    PATH_PDB_H2O = "../data/inputs/reverce_micelles/pdbs/spce_hoh.pdb"  
    
    USER = getpass.getuser()
    user = kwargs.get("user", USER) #<--
    
    PACKMOL_RUN = "/home/{}/packmol-master/packmol".format(user)
    packmol_run = kwargs.get("packmol_run", PACKMOL_RUN) #<--
    
    NUM_AOT = 50
    num_aot = kwargs.get("num_aot", NUM_AOT) #<--
    NUM_NA = num_aot
    num_na = kwargs.get("num_na", NUM_NA) #<--
    NUM_H2O = 300
    num_h2o = kwargs.get("num_h2o", NUM_H2O) #<--
    
    r_inner = kwargs.get("r_inner", 16.0) # determina tamaño #<--
    r_adjust = kwargs.get("r_adjust", 10.0) # distancia desde r_inner #<--
    dr_h2o = kwargs.get("dr_h2o", 0.5) #<--
    dr_na = kwargs.get("dr_na", dr_h2o) #<--
    tol = kwargs.get("tol", 2.0) #<--
    

    SYS_NAME = "eicke-01"
    sys_name = kwargs.get("name_din", SYS_NAME) #<--

    PATH_GRL0 = "/home/{}/Documents/rm_001x/".format(user)
    PATH_GRL0 = kwargs.get("path_grl0", PATH_GRL0)
    
    PATH_GRL1 = os.path.join(PATH_GRL0, sys_name)
    PATH_PACKMOL = os.path.join(PATH_GRL1, "packmol-files")

    packmol_name = sys_name + "_packmol.inp"
    pdb_name = sys_name + ".pdb"

    paths_to_create = [PATH_GRL0,
                       PATH_GRL1,
                       PATH_PACKMOL]
    for path in paths_to_create:
        cmd = ['mkdir', '-p', path]
        cmd = [str(item) for item in cmd]
        process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)

    PATH_OUTPACK = os.path.join(PATH_PACKMOL, packmol_name)
    PATH_OUTPDB = os.path.join(PATH_PACKMOL, pdb_name)
    
    PATH_PDB_AOT = kwargs.get("path_pdb_aot", PATH_PDB_AOT) #<--
    PATH_PDB_NA = kwargs.get("path_pdb_na", PATH_PDB_NA) #<--
    PATH_PDB_H2O = kwargs.get("path_pdb_h2o", PATH_PDB_H2O) #<--    

    dic = rm_packmol_nomed(num_aot=num_aot,
                           num_na=num_na,
                           num_h2o=num_h2o,
                           path_pdb_aot=PATH_PDB_AOT,
                           path_pdb_h2o=PATH_PDB_H2O,
                           path_pdb_na=PATH_PDB_NA,
                           r_inner=r_inner,
                           r_adjust=r_adjust,
                           dr_h2o=dr_h2o,
                           dr_na=dr_na,
                           tol=tol,
                           path_outpack=PATH_OUTPACK,
                           path_outpdb=PATH_OUTPDB)

    paths_to_copy = [dic['path_pdb_aot'],
                     dic['path_pdb_na'],
                     dic['path_pdb_h2o'],
                     dic['path_outpack']]
    paths_to_tmp = [os.path.split(path)[-1] for path in paths_to_copy]

    for path_cp, path_here in zip(paths_to_copy, paths_to_tmp):
        cmd = ['cp', path_cp, path_here]
        cmd = [str(item) for item in cmd]
        process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)

    t = time.time()
    cmd = [packmol_run, '<', os.path.split(PATH_OUTPACK)[-1]]
    cmd = [str(item) for item in cmd]
    cmd = ' '.join(cmd)
    process = subprocess.run(cmd, check=True, shell=True, stdout=subprocess.PIPE, universal_newlines=True)   
    print("time created packmol struct: {}".format(time.time() - t))

    for path in paths_to_tmp:
        cmd = ['rm', path]
        cmd = [str(item) for item in cmd]
        process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)

    paths_to_sysdir = [os.path.join(PATH_PACKMOL, path) for path in paths_to_tmp[:-1]]
    for path_cp, path_there in zip(paths_to_copy[:-1], paths_to_sysdir):
        cmd = ['cp', path_cp, path_there]
        cmd = [str(item) for item in cmd]
        process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)

    return PATH_OUTPDB


    
def rm_box(path):
    

    dic = {}
    dic['id'] = {}
    dic['atype'] = {}
    dic['resname'] = {}
    dic['num_mol'] = {}
    dic['x'] = {}
    dic['y'] = {}
    dic['z'] = {}
    dic['symbol'] = {}

    with open(path, 'r') as f:
        idx = 0
        for line in f:
            sp = line.split()
            if sp[0] in ['HETATM']:
                if sp[3] == "UDD":
                    dic['id'][idx] = int(sp[1])
                    dic['atype'][idx] = str(sp[2])
                    dic['resname'][idx] = str(sp[3])
                    dic['num_mol'][idx] = int(sp[5])
                    dic['x'][idx] = float(sp[6])
                    dic['y'][idx] = float(sp[7])
                    dic['z'][idx] = float(sp[8])
                    dic['symbol'][idx] = str(sp[11])
                    idx+=1
                else:
                    pass

    df = pd.DataFrame(dic)

    r2 = []
    for idx in df.index:
        r = df[['x', 'y', 'z']].loc[idx].values 
        r2.append(np.dot(r, r))

    ra = df.loc[[np.argmax(r2)]][['x', 'y', 'z']]
    ra = ra.values

    d2b = []
    for idx in df.index:
        rb = df[['x', 'y', 'z']].loc[idx].values
        d2b.append(np.linalg.norm(rb-ra))

    dab = max(d2b)
    
    _ = (6/4)*np.ceil(dab)    # dab + (2/4)*dab 
    
    return _, np.ceil(np.divide(_, 10))
    



def wrapper_crear_caja_centrar(**kwargs):
    
    gmx = kwargs.get("gmx", '/usr/local/gromacs/bin/gmx') #<==
    L = kwargs.get("L", 15.0) #<==
    
    PATH_FOLDER_CELDA0 = kwargs.get("path_folder_celda0", "NULL") #<==
    NAME_DIN = kwargs.get("name_din", "NULL") #<==
    PATH_OUTPDB = kwargs.get("path_outpdb", "NULL") #<==
    PATH_RMNOMEDC = os.path.join(PATH_FOLDER_CELDA0, NAME_DIN + "_rmnomedc.gro")

    cmd = [gmx, 'editconf',
           '-f', PATH_OUTPDB,            # input
           '-o', PATH_RMNOMEDC,          # output
           '-c',                         # option
           '-box', L[1], L[1], L[1]]     # input
    cmd = [str(item) for item in cmd]
    process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)
    
    return PATH_RMNOMEDC


def wrapper_create_isobox(**kwargs):
    
    gmx = kwargs.get("gmx", '/usr/local/gromacs/bin/gmx')  #<==
    PATH_FOLDER_CELDA0 = kwargs.get("path_folder_celda0", "NULL")  #<==
    PATH_ISOBOX = os.path.join(PATH_FOLDER_CELDA0, "cajaisooctano.gro")  #<==
 
    PATH_ISOPDB = "../data/inputs/reverce_micelles/pdbs/isoctano_unitedatom_optimised_geometry.pdb"
    PATH_ISOPDB = kwargs.get("path_iso_pdb", PATH_ISOPDB)
    cmd = [gmx, 'insert-molecules',
           '-ci', PATH_ISOPDB,           # input
           '-nmol', 500,                 # input
           '-o', PATH_ISOBOX,            # output
           '-box', 5.0, 5.0, 5.0]        # input
    cmd = [str(item) for item in cmd]
    process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)
    
    return PATH_ISOBOX



def wrapper_solvatar_rm(**kwargs):
    
    gmx = kwargs.get("gmx", '/usr/local/gromacs/bin/gmx')  #<==
    L = kwargs.get("L", 50.0)
        
    PATH_FOLDER_CELDA0 = kwargs.get("path_folder_celda0", "NULL")  #<==
    PATH_RMNOMEDC = kwargs.get("path_rmnomedc", "NULL")  #<==
    PATH_ISOBOX = kwargs.get("path_isobox", "NULL")  #<==
    PATH_TOPOL = kwargs.get("path_topol", "NULL")  #<==
    
    NAME_CELDA0 = kwargs.get("name_celda0", "NULL")
    PATH_CELDA0 = os.path.join(PATH_FOLDER_CELDA0, NAME_CELDA0 + ".gro")

    cmd = [gmx, 'solvate',
           '-cp', PATH_RMNOMEDC,      # input
           '-cs', PATH_ISOBOX,        # input
           '-p',  PATH_TOPOL,         # input
           '-o',  PATH_CELDA0]    # output
    cmd = [str(item) for item in cmd]
    process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)
    
    # Haciendo grande la caja
    cmd = [gmx, 'editconf',
           '-f', PATH_CELDA0,          # input 
           '-box', L+2, L+2, L+2,      # input
           '-o', PATH_CELDA0]          # output
    cmd = [str(item) for item in cmd]
    process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)    
    
    return PATH_CELDA0


def create_no_rm(**kwargs):
    
    PATH_PDB_AOT = "../data/inputs/reverce_micelles/pdbs/63UD_allatom_optimised_geometry2.pdb"
    PATH_PDB_NA = "../data/inputs/reverce_micelles/pdbs/E0XM_allatom_optimised_geometry.pdb"
    PATH_PDB_H2O = "../data/inputs/reverce_micelles/pdbs/spce_hoh.pdb"     
    gmx = kwargs.get("gmx", "NULL")
    
    PATH_BUILD_CELDA0 = os.path.join("./", "celda0")
    PATH_BUILD_CELDA0 = kwargs.get("path_folder_celda0", PATH_BUILD_CELDA0)
    
    NAME_CELDA0 = kwargs.get("name_celda0", "celda0")
    PATH_CELDA0 = os.path.join(PATH_BUILD_CELDA0, NAME_CELDA0 + ".gro")

    PATH_PDB_AOT = "../data/inputs/reverce_micelles/pdbs/63UD_allatom_optimised_geometry2.pdb"
    PATH_PDB_AOT = kwargs.get("path_pdb_aot", PATH_PDB_AOT)
    
    PATH_PDB_NA = "../data/inputs/reverce_micelles/pdbs/E0XM_allatom_optimised_geometry.pdb"
    PATH_PDB_NA = kwargs.get("path_pdb_na", PATH_PDB_NA)
    
    PATH_PDB_H2O = "../data/inputs/reverce_micelles/pdbs/spce_hoh.pdb"
    PATH_PDB_H2O = kwargs.get("path_pdb_h2o", PATH_PDB_H2O)

    cmd = ['mkdir', '-p', PATH_BUILD_CELDA0]
    cmd = [str(item) for item in cmd]
    process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)    
    
    num_aot = kwargs.get("num_aot", 97)
    num_h2o = kwargs.get("num_h2o", 970)
    L = kwargs.get("L", 11)

    ### crear caja 

    # adicionar aots
    # 1) gmx insert-molecules -ci 63UD_allatom_optimised_geometry2.pdb -nmol 97 
    #    -box 11.0 11.0 11.0 -o caja.gro -seed -1
    cmd = [gmx, 'insert-molecules',
           '-ci', PATH_PDB_AOT,         # input
           '-nmol', num_aot,        # input
           '-box', L, L, L,         # input
           '-o', PATH_CELDA0]       # output
    cmd = [str(item) for item in cmd]
    process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)


    # adicionar nas
    # 2) gmx insert-molecules -f caja.gro -ci spce_hoh.pdb
    # -nmol 970 -box 11.0 11.0 11.0 -o caja.gro -seed -1
    cmd = [gmx, 'insert-molecules',
           '-f', PATH_CELDA0,       # input 
           '-ci', PATH_PDB_NA,          # input
           '-nmol', num_aot,        # input
           '-box', L, L, L,         # input
           '-o', PATH_CELDA0]       # output
    cmd = [str(item) for item in cmd]
    process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)

    # 3) gmx insert-molecules -f caja.gro -ci E0XM_allatom_optimised_geometry.pdb -nmol 97
    #    -box 11.0 11.0 11.0 -o caja.gro -seed -1
    cmd = [gmx, 'insert-molecules',
           '-f', PATH_CELDA0,       # input 
           '-ci', PATH_PDB_H2O,         # input
           '-nmol', num_h2o,        # input
           '-box', L, L, L,         # input
           '-o', PATH_CELDA0]       # output
    cmd = [str(item) for item in cmd]
    process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)

    # Haciendo grande la caja
    cmd = [gmx, 'editconf',
           '-f', PATH_CELDA0,          # input 
           '-box', L+2, L+2, L+2,      # input
           '-o', PATH_CELDA0]          # output
    cmd = [str(item) for item in cmd]
    process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)
    
    return PATH_CELDA0




def create_dfcube_001(**kwargs):

    ex = np.array([1, 0, 0])
    ey = np.array([0, 1, 0])
    ez = np.array([0, 0, 1])

    N = 20
    L = 10
    a = np.array([0, 0, 0])
    symbol="He"

    N = kwargs.get("N", N)
    L = kwargs.get("L", L)
    center = kwargs.get("center", a)
    symbol = kwargs.get("symbol", symbol)
    
    a = center
    rs = np.linspace(0, L, N+1)
    k = 0
    p = a + k*ez
    df = herr.add_atom_df(p=p, symbol=symbol)
    
    # z0
    for k in rs[1:]:
        p = a + k*ez
        df = herr.add_atom_df(p=p, symbol=symbol, create=False, df=df)

    a = df[['x', 'y', 'z']].loc[df.index[-1]].values
    for k in rs:
        p = a + k*ex
        df = herr.add_atom_df(p=p, symbol=symbol, create=False, df=df)

    a = df[['x', 'y', 'z']].loc[df.index[-1]].values
    for k in rs:
        p = a - k*ez
        df = herr.add_atom_df(p=p, symbol=symbol, create=False, df=df)

    a = df[['x', 'y', 'z']].loc[df.index[-1]].values
    for k in rs:
        p = a - k*ex
        df = herr.add_atom_df(p=p, symbol=symbol, create=False, df=df)    


        ####

    a = df[['x', 'y', 'z']].loc[df.index[-1]].values
    for k in rs:
        p = a + k*ey
        df = herr.add_atom_df(p=p, symbol=symbol, create=False, df=df)

    a = df[['x', 'y', 'z']].loc[df.index[-1]].values
    for k in rs:
        p = a + k*ez
        df = herr.add_atom_df(p=p, symbol=symbol, create=False, df=df)

    a = df[['x', 'y', 'z']].loc[df.index[-1]].values
    for k in rs:
        p = a - k*ey
        df = herr.add_atom_df(p=p, symbol=symbol, create=False, df=df)    

        
    c = center
    ###
#     a = np.array([L, 0, L])  
    a = np.array([c[0] + L, c[1], c[2] + L])  
    for k in rs:
        p = a + k*ey
        df = herr.add_atom_df(p=p, symbol=symbol, create=False, df=df)       

    a = df[['x', 'y', 'z']].loc[df.index[-1]].values
    for k in rs:
        p = a - k*ex
        df = herr.add_atom_df(p=p, symbol=symbol, create=False, df=df) 


    ###
    a = np.array([c[0] + L, c[1], c[2]])  
    for k in rs:
        p = a + k*ey
        df = herr.add_atom_df(p=p, symbol=symbol, create=False, df=df)   

    a = df[['x', 'y', 'z']].loc[df.index[-1]].values
    for k in rs:
        p = a - k*ex
        df = herr.add_atom_df(p=p, symbol=symbol, create=False, df=df) 

    ### 
    a = np.array([c[0] + L, c[1] + L, c[2]])  
    for k in rs:
        p = a + k*ez
        df = herr.add_atom_df(p=p, symbol=symbol, create=False, df=df)
                   
                   
                   
    return df


def water_density(temp):

    a1 = -3.983035
    a2 = 301.797
    a3 = 522528.9
    a4 = 69.34881
    a5 = 999.97495
    
    A = (temp + a1)**2
    B = temp + a2
    C = a3*(temp + a4)
    # grados centigrados
    # return a5*(1-(A*B/C)) Kg/m3
    
    
    return a5*(1-(A*B/C))*1e-3 # g/cm3

def kelvin2Celsius(kelvins):
    return kelvins - 273.15

def sys_aguas(**kwargs):
    
    dP_LVL1 = kwargs.get("dP_LVL1", {})

    num_mols = kwargs.get('num_mols', 500) # 333
    NUM_MOLS = num_mols

#     dens = kwargs.get('dens', 0.692) g/cm3 # https://en.wikipedia.org/wiki/2,2,4-Trimethylpentane
    temp = kwargs.get('temp', 25.0)
    dens = water_density(temp)
    DENS = dens
    
    GMX = '/usr/local/apps/gromacs-2019.3/build/bin/gmx'
    gmx = kwargs.get('gmx', GMX)
    de = kwargs.get("de", 0.5)
    
    PATH_GRO_SPC216_DATA="../data/inputs/reverce_micelles/gros/spc216.gro"
    PATH_GRO_AGUA_DATA = kwargs.get("path_gro_agua", PATH_GRO_SPC216_DATA)
    NAME_AGUA = kwargs.get("name_agua", "agua.gro")
    
    PATH_GRL1 = dP_LVL1['GRL1']
    PATH_INDIVIDUAL_STRUCTURES = os.path.join(PATH_GRL1, 'individual_structures')
    PATH_CELDAS_INICIALES = os.path.join(PATH_GRL1, 'celdas_iniciales')

    PATH_GRO_SPC216 = os.path.join(PATH_INDIVIDUAL_STRUCTURES, "spc216.gro")
    PATH_ALLATOM_SPC216 = os.path.join(PATH_INDIVIDUAL_STRUCTURES, "spc216.xyz")
    PATH_GRO_AGUA = os.path.join(PATH_INDIVIDUAL_STRUCTURES, NAME_AGUA)
    PATH_CELDA0 = os.path.join(PATH_CELDAS_INICIALES, 'celda0.gro')
    
    herr.wrapper_create_dirs([PATH_GRL1, PATH_INDIVIDUAL_STRUCTURES, PATH_CELDAS_INICIALES])
    
    cmd = ["obabel", PATH_GRO_SPC216_DATA, "-O", PATH_ALLATOM_SPC216]
    cmd = [str(item) for item in cmd]
    process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)    

    herr.copy_file_to(path_in=PATH_GRO_SPC216_DATA, path_out=PATH_GRO_SPC216)
    herr.copy_file_to(path_in=PATH_GRO_AGUA_DATA, path_out=PATH_GRO_AGUA)

    lado_celda0 = herr.vol_cube_length(PATH_ALLATOM_SPC216, DENS, NUM_MOLS)
    lado_celda0 = np.around(lado_celda0, decimals=4)
    cmd = [gmx, 'insert-molecules',
           '-ci', PATH_GRO_AGUA, # antes PATH_GRO_SPC216
           '-nmol', NUM_MOLS,
           '-box', lado_celda0, lado_celda0, lado_celda0,
           '-o', PATH_CELDA0]
    
    cmd = [str(item) for item in cmd]
    process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)
    
    # Haciendo grande la caja
    L = lado_celda0
    L = L+de
    L = np.round(L, decimals=3)
    cmd = [gmx, 'editconf',
           '-f', PATH_CELDA0,          # input 
           '-box', L, L, L,      # input
           '-o', PATH_CELDA0]          # output
    cmd = [str(item) for item in cmd]
    process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)    

    return PATH_CELDA0
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
