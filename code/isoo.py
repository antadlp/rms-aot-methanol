import sys
import getpass
from herramientas import *
from system_creator import *
from groFile import *


herr = herramientas()
call_grompp = call_grompp_conf()


class isoo(object):

    PATH_ISO_RM = "../data/general/forcefields/G016_ffbonded_zero_charge.itp"
    PATH_GROMOS54A7_ATB = "../data/general/forcefields/ffnonbonded_gromos54a7_atb_original.itp"
    
    def set_paths_lvl0(self, **kwargs):

        user = getpass.getuser()
        PATH_GRL_0_0 = kwargs.get("path_grl_0_0", "/home/{}/Documents".format(user))
        NAME_CARPET0 = kwargs.get("name_carpet0", "isoo_tests_00x")

        PATH_GRL0 = os.path.join(PATH_GRL_0_0, NAME_CARPET0)

        PATH_DATA = os.path.join(PATH_GRL0, 'data')
        PATH_PLOTS = os.path.join(PATH_DATA, 'plots')
        PATH_PLOT_DENS = os.path.join(PATH_PLOTS, 'densities')
        PATH_PLOT_SURFT = os.path.join(PATH_PLOTS, 'surfT')
        PATH_TABLES = os.path.join(PATH_DATA, 'tables')
        PATH_XVG_GRACE = os.path.join(PATH_DATA, 'xvg_grace')
        PATH_XVG_DAT = os.path.join(PATH_DATA, 'xvg_dat')

        herr.wrapper_create_dirs([PATH_PLOT_DENS, PATH_PLOT_SURFT, PATH_TABLES, PATH_XVG_GRACE,
                                 PATH_XVG_DAT])
        
        dic = {}
        dic['GRL0'] = PATH_GRL0
        dic['DATA'] = PATH_DATA
        dic['PLOTS'] = PATH_PLOTS
        dic['PLOT_DENS'] = PATH_PLOT_DENS
        dic['PLOT_SURFT'] = PATH_PLOT_SURFT
        dic['TABLES'] = PATH_TABLES
        dic['XVG_GRACE'] = PATH_XVG_GRACE
        dic['XVG_DAT'] = PATH_XVG_DAT

        return dic

    
    def set_paths_lvl1(self, **kwargs):
    
        user = getpass.getuser()
        
        dP_LVL0 = kwargs.get("dP_LVL0", {})
        
        NAME_DIN = kwargs.get("name_din", "din_epsx")
        NAME_CICLO = NAME_DIN

        NAME_TOPOL = 'topol.top'
        NAME_MIN1 = 'min1'
        NAME_MIN2 = 'min2'
        NAME_NVT1 = 'nvt1'
        NAME_NPT1 = 'npt1'
        
        PATH_GRL0 = dP_LVL0['GRL0']

        PATH_GRL1 = os.path.join(PATH_GRL0, NAME_DIN)
        PATH_GRLMIN1 = os.path.join(PATH_GRL1, NAME_MIN1)
        PATH_GRLMIN2 = os.path.join(PATH_GRL1, NAME_MIN2)
        PATH_GRLNVT1 = os.path.join(PATH_GRL1, NAME_NVT1)
        PATH_GRLNPT1 = os.path.join(PATH_GRL1, NAME_NPT1)
        PATH_TOPOL = os.path.join(PATH_GRL1, NAME_TOPOL)

        herr.wrapper_create_dirs([PATH_GRLMIN1, PATH_GRLMIN2, PATH_GRLNVT1, PATH_GRLNPT1])

        # min 1
        PATH_MIN1_MDP = os.path.join(PATH_GRLMIN1, NAME_MIN1 + '.mdp') 
        PATH_MIN1_TPR = os.path.join(PATH_GRLMIN1, NAME_MIN1 + '.tpr') 
        PATH_MIN1_PTOPOL = os.path.join(PATH_GRLMIN1, NAME_MIN1 + '.top')
        PATH_MIN1_PMDP = os.path.join(PATH_GRLMIN1, NAME_MIN1 + '_dump' + '.mdp')

        # mdrun min1
        PATH_MIN1_TRR = os.path.join(PATH_GRLMIN1, NAME_MIN1 + '.trr')
        PATH_MIN1_CONFOUT = os.path.join(PATH_GRLMIN1, NAME_MIN1 + '.gro')
        PATH_MIN1_EDR = os.path.join(PATH_GRLMIN1, NAME_MIN1 + '.edr')
        PATH_MIN1_LOG = os.path.join(PATH_GRLMIN1, NAME_MIN1 + '.log')

        # min 2
        PATH_MIN2_MDP = os.path.join(PATH_GRLMIN2, NAME_MIN2 + '.mdp') 
        PATH_MIN2_TPR = os.path.join(PATH_GRLMIN2, NAME_MIN2 + '.tpr') 
        PATH_MIN2_PTOPOL = os.path.join(PATH_GRLMIN2, NAME_MIN2 + '.top')
        PATH_MIN2_PMDP = os.path.join(PATH_GRLMIN2, NAME_MIN2 + '_dump' + '.mdp')

        # mdrun min 2
        PATH_MIN2_TRR = os.path.join(PATH_GRLMIN2, NAME_MIN2 + '.trr')
        PATH_MIN2_CONFOUT = os.path.join(PATH_GRLMIN2, NAME_MIN2 + '.gro')
        PATH_MIN2_EDR = os.path.join(PATH_GRLMIN2, NAME_MIN2 + '.edr')
        PATH_MIN2_LOG = os.path.join(PATH_GRLMIN2, NAME_MIN2 + '.log')
        PATH_MIN2_CPT = os.path.join(PATH_GRLMIN2, NAME_MIN2 + '.cpt')

        # nvt 1
        PATH_NVT1_MDP = os.path.join(PATH_GRLNVT1, NAME_NVT1 + '.mdp') 
        PATH_NVT1_TPR = os.path.join(PATH_GRLNVT1, NAME_NVT1 + '.tpr') 
        PATH_NVT1_PTOPOL = os.path.join(PATH_GRLNVT1, NAME_NVT1 + '.top')
        PATH_NVT1_PMDP = os.path.join(PATH_GRLNVT1, NAME_NVT1 + '_dump' + '.mdp')

        # mdrun nvt 1
        PATH_NVT1_TRR = os.path.join(PATH_GRLNVT1, NAME_NVT1 + '.trr')
        PATH_NVT1_CONFOUT = os.path.join(PATH_GRLNVT1, NAME_NVT1 + '.gro')
        PATH_NVT1_EDR = os.path.join(PATH_GRLNVT1, NAME_NVT1 + '.edr')
        PATH_NVT1_LOG = os.path.join(PATH_GRLNVT1, NAME_NVT1 + '.log')
        PATH_NVT1_CPT = os.path.join(PATH_GRLNVT1, NAME_NVT1 + '.cpt')

        # npt 1
        PATH_NPT1_MDP = os.path.join(PATH_GRLNPT1, NAME_NPT1 + '.mdp') 
        PATH_NPT1_TPR = os.path.join(PATH_GRLNPT1, NAME_NPT1 + '.tpr') 
        PATH_NPT1_PTOPOL = os.path.join(PATH_GRLNPT1, NAME_NPT1 + '.top')
        PATH_NPT1_PMDP = os.path.join(PATH_GRLNPT1, NAME_NPT1 + '_dump' + '.mdp')

        # mdrun npt 1
        PATH_NPT1_TRR = os.path.join(PATH_GRLNPT1, NAME_NPT1 + '.trr')
        PATH_NPT1_CONFOUT = os.path.join(PATH_GRLNPT1, NAME_NPT1 + '.gro')
        PATH_NPT1_EDR = os.path.join(PATH_GRLNPT1, NAME_NPT1 + '.edr')
        PATH_NPT1_LOG = os.path.join(PATH_GRLNPT1, NAME_NPT1 + '.log')
        PATH_NPT1_CPT = os.path.join(PATH_GRLNPT1, NAME_NPT1 + '.cpt')

        # data npt 1
        PATH_XVG_DAT = dP_LVL0['XVG_DAT']
        PATH_PLOT_DENS = dP_LVL0['PLOT_DENS']
        PATH_NPT1_DENS_XVG_DAT = os.path.join(PATH_XVG_DAT, 'dens_xvg_dat_' + NAME_CICLO + '.xvg')
        PATH_NPT1_DENS_PLOT = os.path.join(PATH_PLOT_DENS, 'dens_plot_' + NAME_CICLO + '.png')

        dic = {}

        dic['MIN1_MDP'] = PATH_MIN1_MDP 
        dic['MIN1_TPR'] = PATH_MIN1_TPR
        dic['MIN1_PTOPOL'] = PATH_MIN1_PTOPOL
        dic['MIN1_PMDP'] = PATH_MIN1_PMDP

        # mdrun min1
        dic['MIN1_TRR'] = PATH_MIN1_TRR 
        dic['MIN1_CONFOUT'] = PATH_MIN1_CONFOUT 
        dic['MIN1_EDR'] = PATH_MIN1_EDR 
        dic['MIN1_LOG'] = PATH_MIN1_LOG 

        # min 2
        dic['MIN2_MDP'] = PATH_MIN2_MDP  
        dic['MIN2_TPR'] = PATH_MIN2_TPR  
        dic['MIN2_PTOPOL'] = PATH_MIN2_PTOPOL 
        dic['MIN2_PMDP'] = PATH_MIN2_PMDP 

        # mdrun min 2
        dic['MIN2_TRR'] = PATH_MIN2_TRR 
        dic['MIN2_CONFOUT'] = PATH_MIN2_CONFOUT
        dic['MIN2_EDR'] = PATH_MIN2_EDR 
        dic['MIN2_LOG'] = PATH_MIN2_LOG 
        dic['MIN2_CPT'] = PATH_MIN2_CPT 

        # nvt 1
        dic['NVT1_MDP'] = PATH_NVT1_MDP 
        dic['NVT1_TPR'] = PATH_NVT1_TPR
        dic['NVT1_PTOPOL'] = PATH_NVT1_PTOPOL 
        dic['NVT1_PMDP'] = PATH_NVT1_PMDP

        # mdrun nvt 1
        dic['NVT1_TRR'] = PATH_NVT1_TRR 
        dic['NVT1_CONFOUT'] = PATH_NVT1_CONFOUT 
        dic['NVT1_EDR'] = PATH_NVT1_EDR 
        dic['NVT1_LOG'] = PATH_NVT1_LOG 
        dic['NVT1_CPT'] = PATH_NVT1_CPT

        # npt 1
        dic['NPT1_MDP'] = PATH_NPT1_MDP
        dic['NPT1_TPR'] = PATH_NPT1_TPR
        dic['NPT1_PTOPOL'] = PATH_NPT1_PTOPOL
        dic['NPT1_PMDP'] = PATH_NPT1_PMDP

        # mdrun npt 1
        dic['NPT1_TRR'] = PATH_NPT1_TRR
        dic['NPT1_CONFOUT'] = PATH_NPT1_CONFOUT
        dic['NPT1_EDR'] = PATH_NPT1_EDR
        dic['NPT1_LOG'] = PATH_NPT1_LOG
        dic['NPT1_CPT'] = PATH_NPT1_CPT

        # data npt 1
        dic['NPT1_DENS_XVG_DAT'] = PATH_NPT1_DENS_XVG_DAT
        dic['NPT1_DENS_PLOT'] = PATH_NPT1_DENS_PLOT
        
        dic['GRL1'] = PATH_GRL1
        dic['GRLMIN1'] = PATH_GRLMIN1 
        dic['GRLMIN2'] = PATH_GRLMIN2
        dic['GRLNVT1'] = PATH_GRLNVT1 
        dic['GRLNPT1'] = PATH_GRLNPT1 
        dic['TOPOL'] = PATH_TOPOL 
        
        PATH_NVT2_CONFIN = os.path.join(PATH_GRLNPT1, 'nvt2' + '_in' + '.gro')
        dic['NVT2_CONFIN'] = PATH_NVT2_CONFIN
        
        dic['XVG_DAT'] = PATH_XVG_DAT            
            

        return dic
    
    
    def wrapper_min1(self, **kwargs):
        
        PATH_TOPOL = kwargs.get("path_topol", "NULL")
        PATH_CELDA0 = kwargs.get("path_celda0", "NULL")
        NUM_PROC = kwargs.get("num_proc", 4)
        nsteps = kwargs.get("nsteps", 100)
        gmx = kwargs.get("gmx", "NULL")

        dP1 = kwargs.get("dP1", {})  
        dP_LVL1 = dP1
        
        df_min1 = call_grompp.call_estandar_min_001(nsteps=nsteps)
        herr.create_grompp(path_grompp=dP_LVL1['MIN1_MDP'],
                           df_grompp=df_min1)              

        cmd = [gmx, 'grompp',
               '-f', dP_LVL1['MIN1_MDP'],
               '-p', PATH_TOPOL, 
               '-c', PATH_CELDA0,
               '-o', dP_LVL1['MIN1_TPR'],
               '-pp', dP_LVL1['MIN1_PTOPOL'],
               '-po', dP_LVL1['MIN1_PMDP'],
               '-maxwarn', '10']

        cmd = [str(item) for item in cmd]
        process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)

        cmd = [gmx, 'mdrun',
               '-s', dP_LVL1['MIN1_TPR'],
               '-o', dP_LVL1['MIN1_TRR'],
               '-c', dP_LVL1['MIN1_CONFOUT'],
               '-e', dP_LVL1['MIN1_EDR'],
               '-g', dP_LVL1['MIN1_LOG'],
               '-nt', NUM_PROC]

        cmd = [str(item) for item in cmd]
        process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)

        return
            
    def wrapper_min2(self, **kwargs):
        
        PATH_TOPOL = kwargs.get("path_topol", "NULL")
        NUM_PROC = kwargs.get("num_proc", 4)
        nsteps = kwargs.get("nsteps", 100)
        gmx = kwargs.get("gmx", "NULL")

        dP1 = kwargs.get("dP1", {})  
        dP_LVL1 = dP1        
        
    
        df_min2 = call_grompp.call_estandar_min_002(nsteps=nsteps)
        herr.create_grompp(path_grompp=dP_LVL1['MIN2_MDP'],
                           df_grompp=df_min2)

        to = time.time()
        cmd = [gmx, 'grompp',
               '-f', dP_LVL1['MIN2_MDP'],          # input
               '-p', PATH_TOPOL,                   # input
               '-c', dP_LVL1['MIN1_CONFOUT'],      # input 
               '-o', dP_LVL1['MIN2_TPR'],          # output 
               '-pp', dP_LVL1['MIN2_PTOPOL'],      # output 
               '-po', dP_LVL1['MIN2_PMDP'],        # output 
               '-maxwarn', '10']

        cmd = [str(item) for item in cmd]
        process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)

        cmd = [gmx, 'mdrun',
               '-s', dP_LVL1['MIN2_TPR'],
               '-o', dP_LVL1['MIN2_TRR'],
               '-c', dP_LVL1['MIN2_CONFOUT'],
               '-e', dP_LVL1['MIN2_EDR'],
               '-g', dP_LVL1['MIN2_LOG'],
               '-nt', NUM_PROC]

        cmd = [str(item) for item in cmd]
        process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)
 
        
        
        return


    
    def wrapper_nvt1(self, **kwargs):

        PATH_TOPOL = kwargs.get("path_topol", "NULL")
        NUM_PROC = kwargs.get("num_proc", 4)
        nsteps = kwargs.get("nsteps", 100)
        gmx = kwargs.get("gmx", "NULL")
        dt = kwargs.get("dt", 0.002)
        rcoulomb = kwargs.get("rcoulomb", 1.5)
        rvdw = kwargs.get("rvdw", 1.5)

        dP1 = kwargs.get("dP1", {})  
        dP_LVL1 = dP1

        df_nvt1 = call_grompp.call_estandar_nvt_000(nsteps=nsteps,
                                                    dt=dt,
                                                    rcoulomb=rcoulomb,
                                                    rvdw=rvdw)

        herr.create_grompp(path_grompp=dP_LVL1['NVT1_MDP'], df_grompp=df_nvt1)

        to = time.time()
        cmd = [gmx, 'grompp',
               '-f', dP_LVL1['NVT1_MDP'],
               '-p', PATH_TOPOL,         
               '-c', dP_LVL1['MIN2_CONFOUT'],  
               '-o', dP_LVL1['NVT1_TPR'],
               '-pp', dP_LVL1['NVT1_PTOPOL'],
               '-po', dP_LVL1['NVT1_PMDP'],
               '-maxwarn', '10']

        cmd = [str(item) for item in cmd]
        process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)

        cmd = [gmx, 'mdrun',
               '-s', dP_LVL1['NVT1_TPR'], 
               '-o', dP_LVL1['NVT1_TRR'],
               '-c', dP_LVL1['NVT1_CONFOUT'], 
               '-e', dP_LVL1['NVT1_EDR'],
               '-g', dP_LVL1['NVT1_LOG'],
               '-cpo', dP_LVL1['NVT1_CPT'],
               '-nt', NUM_PROC]

        cmd = [str(item) for item in cmd]
        process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)


        return


    def wrapper_npt1(self, **kwargs):

        PATH_TOPOL = kwargs.get("path_topol", "NULL")
        NUM_PROC = kwargs.get("num_proc", 4)
        nsteps = kwargs.get("nsteps", 100)
        gmx = kwargs.get("gmx", "NULL")    
        dt = kwargs.get("dt", 0.001)
        rcoulomb = kwargs.get("rcoulomb", 1.5)
        rvdw = kwargs.get("rvdw", 1.5)

        dP1 = kwargs.get("dP1", {})  
        dP_LVL1 = dP1

        df_npt1 = call_grompp.call_estandar_npt_000(nsteps=nsteps,
                                                    dt=dt,
                                                    rcoulomb=rcoulomb,
                                                    rvdw=rvdw)

        herr.create_grompp(path_grompp=dP_LVL1['NPT1_MDP'], df_grompp=df_npt1) 

        to = time.time()
        cmd = [gmx, 'grompp',
               '-f', dP_LVL1['NPT1_MDP'], 
               '-p', PATH_TOPOL,        
               '-c', dP_LVL1['NVT1_CONFOUT'],
               '-o', dP_LVL1['NPT1_TPR'],      
               '-pp', dP_LVL1['NPT1_PTOPOL'],
               '-po', dP_LVL1['NPT1_PMDP'],
               '-maxwarn', '10']

        cmd = [str(item) for item in cmd]
        process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)

        cmd = [gmx, 'mdrun',
               '-s', dP_LVL1['NPT1_TPR'], 
               '-o', dP_LVL1['NPT1_TRR'],
               '-c', dP_LVL1['NPT1_CONFOUT'], 
               '-e', dP_LVL1['NPT1_EDR'],
               '-g', dP_LVL1['NPT1_LOG'],
               '-cpo', dP_LVL1['NPT1_CPT'],
               '-nt', NUM_PROC]
        cmd = [str(item) for item in cmd]
        process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)    


        f = open('tmpE.dat', 'w')
        f.write("Density\n0\n")
        f.close()

        cmd = [gmx, 'energy',
               '-f', dP_LVL1['NPT1_EDR'], 
               '-o', dP_LVL1['NPT1_DENS_XVG_DAT'], 
               '-xvg', 'none',
               '<', 'tmpE.dat']
        cmd = [str(item) for item in cmd]
        cmd = ' '.join(cmd)
        process = subprocess.run(cmd, check=True, shell=True, stdout=subprocess.PIPE, universal_newlines=True)   

        gro_npt1 = groFile(dP_LVL1['NPT1_CONFOUT'])
        dic = gro_npt1.get_general_info()
        xyz = gro_npt1.get_box_dims().loc[0].values


        cmd = [gmx, 'editconf',
               '-f', dP_LVL1['NPT1_CONFOUT'],
               '-o', dP_LVL1['NVT2_CONFIN'],
               '-c',
               '-box', xyz[0], xyz[1], 3*xyz[2]]
        cmd = [str(item) for item in cmd]
        process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)


        return
    
    def wrapper_nvt2s(self, **kwargs):

        PATH_TOPOL = kwargs.get("path_topol", "NULL")
        NAME_DIN = kwargs.get("name_din", "NULL")
        NUM_PROC = kwargs.get("num_proc", 4)
        df_nvt2 = kwargs.get("df_nvt2", "NULL")
        gmx = kwargs.get("gmx", "NULL")
        i = kwargs.get("i", "NULL")

        dP1 = kwargs.get("dP1", {})  
        dP_LVL1 = dP1    
        
        NAME_CICLO = NAME_DIN

        label = '_' + str(i)

        NAME_NVT2 = 'nvt2' + label
        surfT_name = 'surfT' + label
        
        PATH_NVT2_CONFIN = dP_LVL1['NVT2_CONFIN']

        PATH_GRLNVT2 = os.path.join(dP_LVL1['GRL1'], NAME_NVT2) 

        cmd = ['mkdir', '-p', PATH_GRLNVT2] # creando nvt2
        cmd = [str(item) for item in cmd]
        process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True) 

        # nvt 2
        PATH_NVT2_MDP = os.path.join(PATH_GRLNVT2, NAME_NVT2 + '.mdp') 
        PATH_NVT2_TPR = os.path.join(PATH_GRLNVT2, NAME_NVT2 + '.tpr') 
        PATH_NVT2_PTOPOL = os.path.join(PATH_GRLNVT2, NAME_NVT2 + '.top')
        PATH_NVT2_PMDP = os.path.join(PATH_GRLNVT2, NAME_NVT2 + '_dump' + '.mdp')

        # mdrun nvt 2
        PATH_NVT2_TRR = os.path.join(PATH_GRLNVT2, NAME_NVT2 + '.trr')
        PATH_NVT2_CONFOUT = os.path.join(PATH_GRLNVT2, NAME_NVT2 + '.gro')
        PATH_NVT2_EDR = os.path.join(PATH_GRLNVT2, NAME_NVT2 + '.edr')
        PATH_NVT2_LOG = os.path.join(PATH_GRLNVT2, NAME_NVT2 + '.log')
        PATH_NVT2_CPT = os.path.join(PATH_GRLNVT2, NAME_NVT2 + '.cpt')

        # data nvt 2
        PATH_NVT2_SURFT_XVG_DAT = os.path.join(dP_LVL1['XVG_DAT'], surfT_name +\
                                               '_xvg_dat_' + NAME_CICLO + '.xvg')

        herr.create_grompp(path_grompp=PATH_NVT2_MDP,
                           df_grompp=df_nvt2)

        to = time.time()
        cmd = [gmx, 'grompp',
               '-f', PATH_NVT2_MDP,      # input
               '-p', PATH_TOPOL,         # input
               '-c', PATH_NVT2_CONFIN,   # input
               '-o', PATH_NVT2_TPR,      # output
               '-pp', PATH_NVT2_PTOPOL,  # output
               '-po', PATH_NVT2_PMDP,    # output
               '-maxwarn', '10']

        cmd = [str(item) for item in cmd]
        process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)

        cmd = [gmx, 'mdrun',
               '-s', PATH_NVT2_TPR,
               '-o', PATH_NVT2_TRR,
               '-c', PATH_NVT2_CONFOUT,
               '-e', PATH_NVT2_EDR,
               '-g', PATH_NVT2_LOG,
               '-cpo', PATH_NVT2_CPT,
               '-nt', NUM_PROC]

        cmd = [str(item) for item in cmd]
        process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)

        f = open('tmpE.dat', 'w')
        f.write("#Surf*SurfTen\n0\n")
        f.close()

        cmd = [gmx, 'energy',
               '-f', PATH_NVT2_EDR,
               '-o', PATH_NVT2_SURFT_XVG_DAT,
               '-xvg', 'none',
               '<', 'tmpE.dat']
        cmd = [str(item) for item in cmd]
        cmd = ' '.join(cmd)
        process = subprocess.run(cmd, check=True, shell=True, stdout=subprocess.PIPE, universal_newlines=True)   

        tnvt2 = time.time() - to
        print("{}: {}".format(NAME_NVT2, tnvt2))    

        return    
        
        
    def extract_trr2xtc(self, **kwargs):

        gmx = "/usr/local/gromacs/bin/gmx"
        gmx = kwargs.get("gmx", gmx)

        PATH_CARPETS = kwargs.get("path_carpets", [])

        NAME_CARPET_TRRS = "trr_s"
        NAME_CARPET_TRRS = kwargs.get("name_carpet_trrs", NAME_CARPET_TRRS)
        PATH_TRRS = kwargs.get("path_trrs", "./")

        PATH_TRRS = os.path.join(PATH_TRRS, NAME_CARPET_TRRS)
        NAMES_TRRS_OUT = kwargs.get("names_trrs_out", [])

        NAME_CARPET_LEQ = kwargs.get("name_carpet_leq", "")

        tcarpets = kwargs.get("tcarpets", "NULL")

        if (not os.path.exists(PATH_TRRS)):
            os.makedirs(PATH_TRRS)

        for PATH_CARPET0, NAME_TRRS_OUT, tcarpet in zip(PATH_CARPETS, NAMES_TRRS_OUT, tcarpets):
        
            print(PATH_CARPET0)
            print(NAME_CARPET_LEQ)

            PATH_CARPET = os.path.join(PATH_CARPET0, NAME_CARPET_LEQ)
            print(PATH_CARPET)

            grompp_file = "grompp.mdp"
            conf_file = "conf.gro"
            topol_file = "topol.top"
            tpr_file = "topol.tpr"
            topol_out = "topolout.top"
            mdout_mdp = "mdout.mdp"
            traj_trr = "traj.trr"
            traj_xtc = "traj.xtc"
            
            # tcarpet = NAME_TRRS_OUT.split("_")[3:][0]
            print(f"{tcarpet} <================")
            
            grompp_file = f"{tcarpet}.mdp"
            conf_file = f"{tcarpet}.gro"
            topol_file = f"{tcarpet}.top"
            tpr_file = f"{tcarpet}.tpr"
            topol_out = f"topolout.top"
            mdout_mdp = f"mdout.mdp"
            traj_trr = f"{tcarpet}.trr"
            traj_xtc = f"{tcarpet}.xtc"
            
            PATH_GROMPP = os.path.join(PATH_CARPET, grompp_file)
            PATH_CONF = os.path.join(PATH_CARPET, conf_file)

            _ = os.path.normpath(PATH_CARPET)
            NAME_ESTRUCTURA = _.split(os.sep)[-1]

            PATH_TRR_OUT = os.path.join(PATH_TRRS, NAME_TRRS_OUT + ".trr")

            PATH_GROMPP = os.path.join(PATH_CARPET, grompp_file)     # input
            PATH_TOPOL = os.path.join(PATH_CARPET, topol_file)       # input
            PATH_CONF = os.path.join(PATH_CARPET, conf_file)         # input
            PATH_TPR = os.path.join(PATH_CARPET, tpr_file)           # output
            PATH_PTOPOL = os.path.join(PATH_CARPET, topol_out)       # output
            PATH_PMDP = os.path.join(PATH_CARPET, mdout_mdp)         # output

            PATH_TRR = os.path.join(PATH_CARPET, traj_trr)
            PATH_XTC = os.path.join(PATH_CARPET, traj_xtc)

            cmd = [gmx, 'grompp',
                   '-f', PATH_GROMPP,        # input
                   '-p', PATH_TOPOL,         # input
                   '-c', PATH_CONF,          # input
                   '-o', PATH_TPR,           # output
                   '-pp', PATH_PTOPOL,       # output
                   '-po', PATH_PMDP,         # output
                   '-maxwarn', '10']         
            cmd = [str(item) for item in cmd]
            process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)

            cmd = [gmx, 'trjconv',
                '-f', PATH_TRR,
                '-o', PATH_XTC]
            cmd = [str(item) for item in cmd]
            process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)

            cmd = ['mv', PATH_TRR, PATH_TRR_OUT]
            cmd = [str(item) for item in cmd]
            process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)
           
            print(PATH_TRR)
            print(PATH_TRR_OUT)


        return
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
