import sys
import getpass
from herramientas import *
from groFile import *
from topoles import *


herr = herramientas()
call_grompp = call_grompp_conf()
tp = topoles()


class norm(object):

    PATH_ISO_RM = "../data/general/forcefields/G016_ffbonded_zero_charge.itp"
    PATH_GROMOS54A7_ATB = "../data/general/forcefields/ffnonbonded_gromos54a7_atb_original.itp"
    
    def set_paths_lvl0(self, **kwargs):

        user = getpass.getuser()
        PATH_GRL_0_0 = kwargs.get("path_grl_0_0", "/home/{}/Documents".format(user))
        NAME_CARPET0 = kwargs.get("name_carpet0", "aguas_tests_00x")

        PATH_GRL0 = os.path.join(PATH_GRL_0_0, NAME_CARPET0)

        PATH_DATA = os.path.join(PATH_GRL0, 'data')
        PATH_PLOTS = os.path.join(PATH_DATA, 'plots')
        PATH_PLOT_DENS = os.path.join(PATH_PLOTS, 'densities')
        PATH_PLOT_SURFT = os.path.join(PATH_PLOTS, 'surfT')
        PATH_TABLES = os.path.join(PATH_DATA, 'tables')
        PATH_XVG_GRACE = os.path.join(PATH_DATA, 'xvg_grace')
        PATH_XVG_DAT = os.path.join(PATH_DATA, 'xvg_dat')
        
        PATH_GRO_NA = "../data/inputs/reverce_micelles/gros/na.gro"
        PATH_GRO_AOT  = "../data/inputs/reverce_micelles/gros/udd.gro"
        PATH_GRO_ISO = "../data/inputs/reverce_micelles/gros/isooctano_united.gro"
        PATH_GRO_H2O = "../data/inputs/reverce_micelles/gros/spc216.gro"
        PATH_GRO_MET = "../data/inputs/rms_contaminantes/gros/jqkk.gro"
        
        PATH_FF_AOT = "../data/general/forcefields/63UD_GROMACS_G54A7FF_allatom_UDD.itp"
        PATH_FF_H20 = "../data/inputs/reverce_micelles/forcefields/aguas/spc_54a7.itp"
        PATH_FF_NA  = "../data/general/forcefields/E0XM_GROMACS_G54A7FF_allatom_original.itp"
        PATH_FF_ISO = "../data/general/forcefields/G016_ffbonded_zero_charge.itp"
        PATH_FF_MET = "../data/inputs/rms_contaminantes/itps/JQKK_GROMACS_G54A7FF_allatom.itp"
        PATH_FF_GROMOS54A7_ATB = "../data/general/forcefields/ffnonbonded_gromos54a7_atb_original.itp"
        
        PATH_GRO_NA = kwargs.get("path_gro_na", PATH_GRO_NA)
        PATH_GRO_AOT  = kwargs.get("path_gro_aot", PATH_GRO_AOT)
        PATH_GRO_ISO = kwargs.get("path_gro_iso", PATH_GRO_ISO)
        PATH_GRO_H2O = kwargs.get("path_gro_h2o", PATH_GRO_H2O)

        PATH_FF_AOT = kwargs.get("path_ff_aot", PATH_FF_AOT)
        PATH_FF_H20 = kwargs.get("path_ff_h2o", PATH_FF_H20)
        PATH_FF_NA  = kwargs.get("path_ff_na", PATH_FF_NA)
        PATH_FF_ISO = kwargs.get("path_ff_iso", PATH_FF_ISO)
        PATH_FF_GROMOS54A7_ATB = kwargs.get("path_ff_54a7", PATH_FF_GROMOS54A7_ATB)        

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
        
        
        # GEMETRIES AND FORCEFIELDS
        dic['PATH_GRO_NA'] = PATH_GRO_NA
        dic['PATH_GRO_AOT'] = PATH_GRO_AOT
        dic['PATH_GRO_ISO'] = PATH_GRO_ISO
        dic['PATH_GRO_H2O'] = PATH_GRO_H2O
        dic['PATH_GRO_CONTA'] = PATH_GRO_MET

        dic['PATH_FF_AOT'] = PATH_FF_AOT
        dic['PATH_FF_H20'] = PATH_FF_H20
        dic['PATH_FF_NA'] = PATH_FF_NA
        dic['PATH_FF_ISO'] = PATH_FF_ISO
        dic['PATH_FF_CONTA'] = PATH_FF_MET
        dic['PATH_FF_GROMOS54A7_ATB'] = PATH_FF_GROMOS54A7_ATB
        

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
        NAME_FOLDER_CELDA0 = "celda0"
        
        GROMPP = "grompp.mdp"
        TOPOLTPR = "topol.tpr"
        TOPOLOUT = "topolout.top"
        MDPOUT = "mdout.mdp"
        TRAJ = "traj.trr"
        CONFOUT = "confout.gro"
        ENER = "ener.edr"
        CONF = "conf.gro"
        LOG = "md.log"
        CPT = "state.cpt"
        
        PATH_GRL0 = dP_LVL0['GRL0']

        PATH_GRL1 = os.path.join(PATH_GRL0, NAME_DIN)
        PATH_FOLDER_CELDA0 = os.path.join(PATH_GRL1, NAME_FOLDER_CELDA0)
        PATH_GRLMIN1 = os.path.join(PATH_GRL1, NAME_MIN1)
        PATH_GRLMIN2 = os.path.join(PATH_GRL1, NAME_MIN2)
        PATH_GRLNVT1 = os.path.join(PATH_GRL1, NAME_NVT1)
        PATH_GRLNPT1 = os.path.join(PATH_GRL1, NAME_NPT1)
        PATH_TOPOL = os.path.join(PATH_GRL1, NAME_TOPOL)

        herr.wrapper_create_dirs([PATH_GRLMIN1, PATH_GRLMIN2, PATH_GRLNVT1, PATH_GRLNPT1])
        

        # min 1
        PATH_MIN1_MDP = os.path.join(PATH_GRLMIN1, GROMPP) 
        PATH_MIN1_TPR = os.path.join(PATH_GRLMIN1, TOPOLTPR) 
        PATH_MIN1_PTOPOL = os.path.join(PATH_GRLMIN1, TOPOLOUT)
        PATH_MIN1_PMDP = os.path.join(PATH_GRLMIN1, MDPOUT)
        PATH_MIN1_CONF = os.path.join(PATH_GRLMIN1, CONF)
        

        # mdrun min1
        PATH_MIN1_TRR = os.path.join(PATH_GRLMIN1, TRAJ)
        PATH_MIN1_CONFOUT = os.path.join(PATH_GRLMIN1, CONFOUT)
        PATH_MIN1_EDR = os.path.join(PATH_GRLMIN1, ENER)
        PATH_MIN1_LOG = os.path.join(PATH_GRLMIN1, LOG)
        PATH_MIN1_CPT = os.path.join(PATH_GRLMIN1, CPT)
        
        
        
        # min 2
        PATH_MIN2_MDP = os.path.join(PATH_GRLMIN2, GROMPP) 
        PATH_MIN2_TPR = os.path.join(PATH_GRLMIN2, TOPOLTPR) 
        PATH_MIN2_PTOPOL = os.path.join(PATH_GRLMIN2, TOPOLOUT)
        PATH_MIN2_PMDP = os.path.join(PATH_GRLMIN2, MDPOUT)
        PATH_MIN2_CONF = os.path.join(PATH_GRLMIN2, CONF)
        PATH_MIN2_TOPOL = os.path.join(PATH_GRLMIN2, NAME_TOPOL)

        # mdrun MIN2
        PATH_MIN2_TRR = os.path.join(PATH_GRLMIN2, TRAJ)
        PATH_MIN2_CONFOUT = os.path.join(PATH_GRLMIN2, CONFOUT)
        PATH_MIN2_EDR = os.path.join(PATH_GRLMIN2, ENER)
        PATH_MIN2_LOG = os.path.join(PATH_GRLMIN2, LOG)
        PATH_MIN2_CPT = os.path.join(PATH_GRLMIN2, CPT)
        
        
        
        # NVT1
        PATH_NVT1_MDP = os.path.join(PATH_GRLNVT1, GROMPP) 
        PATH_NVT1_TPR = os.path.join(PATH_GRLNVT1, TOPOLTPR) 
        PATH_NVT1_PTOPOL = os.path.join(PATH_GRLNVT1, TOPOLOUT)
        PATH_NVT1_PMDP = os.path.join(PATH_GRLNVT1, MDPOUT)
        PATH_NVT1_CONF = os.path.join(PATH_GRLNVT1, CONF)
        PATH_NVT1_TOPOL = os.path.join(PATH_GRLNVT1, NAME_TOPOL)


        # mdrun NVT1
        PATH_NVT1_TRR = os.path.join(PATH_GRLNVT1, TRAJ)
        PATH_NVT1_CONFOUT = os.path.join(PATH_GRLNVT1, CONFOUT)
        PATH_NVT1_EDR = os.path.join(PATH_GRLNVT1, ENER)
        PATH_NVT1_LOG = os.path.join(PATH_GRLNVT1, LOG)
        PATH_NVT1_CPT = os.path.join(PATH_GRLNVT1, CPT)
        
        
        
        # NPT1
        PATH_NPT1_MDP = os.path.join(PATH_GRLNPT1, GROMPP) 
        PATH_NPT1_TPR = os.path.join(PATH_GRLNPT1, TOPOLTPR) 
        PATH_NPT1_PTOPOL = os.path.join(PATH_GRLNPT1, TOPOLOUT)
        PATH_NPT1_PMDP = os.path.join(PATH_GRLNPT1, MDPOUT)
        PATH_NPT1_CONF = os.path.join(PATH_GRLNPT1, CONF)

        # mdrun NPT1
        PATH_NPT1_TRR = os.path.join(PATH_GRLNPT1, TRAJ)
        PATH_NPT1_CONFOUT = os.path.join(PATH_GRLNPT1, CONFOUT)
        PATH_NPT1_EDR = os.path.join(PATH_GRLNPT1, ENER)
        PATH_NPT1_LOG = os.path.join(PATH_GRLNPT1, LOG)
        PATH_NPT1_CPT = os.path.join(PATH_GRLNPT1, CPT)
        
        

        # data npt 1
        PATH_XVG_DAT = dP_LVL0['XVG_DAT']
        PATH_PLOT_DENS = dP_LVL0['PLOT_DENS']
        PATH_NPT1_DENS_XVG_DAT = os.path.join(PATH_XVG_DAT, 'dens_xvg_dat_' + NAME_CICLO + '.xvg')
        PATH_NPT1_DENS_PLOT = os.path.join(PATH_PLOT_DENS, 'dens_plot_' + NAME_CICLO + '.png')

        dic = {}
        
        # celda0
        dic['FOLDER_CELDA0'] = PATH_FOLDER_CELDA0 
    
        # MIN1
        dic['MIN1_MDP'] = PATH_MIN1_MDP 
        dic['MIN1_TPR'] = PATH_MIN1_TPR
        dic['MIN1_PTOPOL'] = PATH_MIN1_PTOPOL
        dic['MIN1_PMDP'] = PATH_MIN1_PMDP
        dic['MIN1_CONF'] = PATH_MIN1_CONF

        dic['MIN1_TRR'] = PATH_MIN1_TRR 
        dic['MIN1_CONFOUT'] = PATH_MIN1_CONFOUT 
        dic['MIN1_EDR'] = PATH_MIN1_EDR 
        dic['MIN1_LOG'] = PATH_MIN1_LOG
        dic['MIN1_CPT'] = PATH_MIN1_CPT
        
        

        # min 2
        dic['MIN2_MDP'] = PATH_MIN2_MDP  
        dic['MIN2_TPR'] = PATH_MIN2_TPR  
        dic['MIN2_PTOPOL'] = PATH_MIN2_PTOPOL 
        dic['MIN2_PMDP'] = PATH_MIN2_PMDP
        dic['MIN2_CONF'] = PATH_MIN2_CONF
        dic['MIN2_TOPOL'] = PATH_MIN2_TOPOL
        

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
        dic['NVT1_CONF'] = PATH_NVT1_CONF
        dic['NVT1_TOPOL'] = PATH_NVT1_TOPOL

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
        dic['NPT1_CONF'] = PATH_NPT1_CONF

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
        
        dic['NAME_DIN'] = NAME_DIN
            

        return dic
    

    def create_no_rm(self, **kwargs):

        dP_LVL0 = kwargs.get("dP_LVL0", {})
        dP_LVL1 = kwargs.get("dP_LVL1", {})

        PATH_PDB_AOT = dP_LVL0['PATH_GRO_AOT']
        PATH_PDB_NA = dP_LVL0['PATH_GRO_NA']
        PATH_PDB_H2O = dP_LVL0['PATH_GRO_H2O']
        PATH_GRO_ISO = dP_LVL0['PATH_GRO_ISO']

        gmx = kwargs.get("gmx", "NULL")

        PATH_FOLDER_CELDA0 = dP_LVL1['FOLDER_CELDA0']
        PATH_CELDA0 = os.path.join(PATH_FOLDER_CELDA0, "celda0.gro")
        dP_LVL1['CELDA0'] = PATH_CELDA0

        cmd = ['mkdir', '-p', PATH_FOLDER_CELDA0]
        cmd = [str(item) for item in cmd]
        process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)    

        num_aot = kwargs.get("num_aot", 97)
        num_h2o = kwargs.get("num_h2o", 970)
        num_iso = kwargs.get("num_iso", 0)
        L = kwargs.get("L", 11)
        d = kwargs.get("d", 2)

        ### crear caja 
        PATHS = [PATH_PDB_AOT, PATH_PDB_NA, PATH_PDB_H2O, PATH_GRO_ISO]
        NUMS = [num_aot, num_aot, num_h2o, num_iso]

        cmd = [gmx, 'insert-molecules',
               '-ci', PATHS[0],   
               '-nmol', NUMS[0],   
               '-box', L, L, L,         
               '-o', PATH_CELDA0]       
        cmd = [str(item) for item in cmd]
        process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)

        for i in range(1, 4):
            
            if NUMS[i] < 1:
                continue
            else:
                
                cmd = [gmx, 'insert-molecules',
                       '-f', PATH_CELDA0,       # input 
                       '-ci', PATHS[i],         # input
                       '-nmol', NUMS[i],        # input
                       '-box', L, L, L,         # input
                       '-o', PATH_CELDA0]       # output
                cmd = [str(item) for item in cmd]
                process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)

            
        cmd = [gmx, 'editconf',
               '-f', PATH_CELDA0,                   # input 
               '-box', L + d, L + d, L + d,         # input
               '-o', PATH_CELDA0]                   # output
        cmd = [str(item) for item in cmd]
        process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)        


        return PATH_CELDA0

    
    def eskici_naot(self, **kwargs):

        # default values in paper, constants
        no_aot = kwargs.get("no_aot", 13.6) # adimensional
        a_aot = kwargs.get("a_aot", 59) # (angstroms)^2
        vbar = kwargs.get("vbar", 33) # (angstroms)^3

        w0 = kwargs.get("w0", 7.5) # independent value

        A = np.divide(np.power(vbar, 2), np.power(a_aot, 3))
        B = 36*np.pi*np.power((w0 + 1.5), 2)

        n_aot = A*B + no_aot

        return n_aot
    

    def waters4Wos(self, **kwargs):

        w0 = kwargs.get("w0", 7.5)
        aots = kwargs.get("aots", 62)

        return np.multiply(w0, aots)    


    
    def get_ffnb_no_rm(self, **kwargs):
        
        CARPET = kwargs.get("carpet", "carpeta")

        epsilon_factor = kwargs.get("epsilon_factor", 0.925)
        sigma_factor = kwargs.get("sigma_factor", 1.0)
        
        dP_LVL0 = kwargs.get("dP_LVL0", {})
        dP_LVL1 = kwargs.get("dP_LVL1", {})
        
        NAME_DIN = dP_LVL1['NAME_DIN']

        PATH_GRL0 = dP_LVL0['GRL0']
        PATH_GRL1 = os.path.join(PATH_GRL0, NAME_DIN)
        PATH_GRL2 = os.path.join(PATH_GRL1, CARPET)
        PATH_GRL2 = os.path.join(PATH_GRL2, "forcefield")

        NAME_FFNB = "ffnb_" + NAME_DIN + ".itp"
        PATH_FFNB_RM = os.path.join(PATH_GRL2, NAME_FFNB)
        PATH_FFNB_RM = kwargs.get("path_out", PATH_FFNB_RM)
        
        paths_to_create = [PATH_GRL0, PATH_GRL1, PATH_GRL2]
        herr.wrapper_create_dirs(paths_to_create)
            
        path_ffb_in_g016 = dP_LVL0['PATH_FF_ISO']
        path_ffb_in_aot = dP_LVL0['PATH_FF_AOT']
        path_ffb_in_h2o = dP_LVL0['PATH_FF_H20']
        path_ffb_in_na = dP_LVL0['PATH_FF_NA']            
        path_gromos54a7_atb = dP_LVL0['PATH_FF_GROMOS54A7_ATB'] 

        # atomtypes de aot
        df = tp.get_binfo_aot(path_top=path_ffb_in_aot)["[ atoms ]"]
        at_aot = df["type"].unique()

        # atypes de g016
        df = tp.get_binfo_g016(path_top=path_ffb_in_g016)["[ atoms ]"]
        at_g016 = df["type"].unique()
        comb = combinations(at_g016, 2)
        comb_g016 = [(i[0], i[1]) for i in list(comb)]

        # atypes de spce
        df = tp.get_binfo_spc_54a7(path_top=path_ffb_in_h2o)["[ atoms ]"]
        at_spce = df["type"].unique()

        # atypes de na
        df = tp.get_binfo_na(path_top=path_ffb_in_na)["[ atoms ]"]
        at_na = df["type"].unique()

        # juntando a todos
        rm_atypes = np.concatenate((at_aot, at_g016, at_spce, at_na)).astype(str)
        comb = combinations(rm_atypes, 2) 
        comb_atypes = [(i[0], i[1]) for i in list(comb)]

        self_comb = [(mol, mol) for mol in rm_atypes]
        all_comb_atypes = comb_atypes.copy()
        all_comb_atypes.extend(self_comb)

        # query de ffnbounded 54a7 atb
        df_54a7_at = tp.get_nbinfo_gromos54a7_atb(path_top=path_gromos54a7_atb)['[ atomtypes ]']
        df_54a7_nb = tp.get_nbinfo_gromos54a7_atb(path_top=path_gromos54a7_atb)['[ nonbond_params ]']
        df_54a7_pt = tp.get_nbinfo_gromos54a7_atb(path_top=path_gromos54a7_atb)['[ pairtypes ]']


        ## EXTRAYENDO ATYPES

        df_at_rm = df_54a7_at.loc[df_54a7_at['name'].isin(rm_atypes)]

        ## EXTRAYENDO NON BOUNDED PARAMS

        comb_atypes_nog016 = []
        for ti in comb_atypes:
            flag_array = []
            for tj in comb_g016:
                i = frozenset(ti)
                j = frozenset(tj)
                if i == j:
                    flag_array.append(False)
                else:
                    flag_array.append(True)

            if np.all(flag_array):
                comb_atypes_nog016.append(ti)

        idxs_nb = []
        for idx in df_54a7_nb.index:
            flag_array = []

            t1 = df_54a7_nb['i'].loc[idx]
            t2 = df_54a7_nb['j'].loc[idx]
            ti = (t1, t2)

            if t1 == t2:
                print(ti)

            for tj in comb_atypes_nog016:
                i = frozenset(ti)
                j = frozenset(tj)
                if i == j:
                    idxs_nb.append(idx)

        df_nb_rm = df_54a7_nb.loc[idxs_nb]

        ## EXTRAYENDO PAIR TYPES

        idxs_pt = []
        for idx in df_54a7_pt.index:
            flag_array = []

            t1 = df_54a7_pt['i'].loc[idx]
            t2 = df_54a7_pt['j'].loc[idx]
            ti = (t1, t2)

            for tj in all_comb_atypes:
                i = frozenset(ti)
                j = frozenset(tj)
                if i == j:
                    idxs_pt.append(idx)

        df_pt_rm = df_54a7_pt.loc[idxs_pt]

        # Modificando g016 atypes parametros
        df_mod_g016 = tp.gen_nonbonded_G016_2(epsilon_factor=epsilon_factor,
                                                sigma_factor=sigma_factor,
                                                path_top_54a7=path_gromos54a7_atb,
                                                path_top_g016=path_ffb_in_g016)
        
        df_at_rm = df_at_rm.copy()
        df_at_rm.update(df_mod_g016)

        # ESCRIBIENDO ARCHIVO FFNONBOUNDED
        f = open(PATH_FFNB_RM, 'w')

        # Escribiendo '[ atomtypes ]'
        f.write('[ atomtypes ]\n')
        f.write('; name  at.num   mass      charge  ptype                c6                      c12\n')

        for idx in df_at_rm.index:

            name = df_at_rm['name'].loc[idx]
            atnum = int(df_at_rm['at.num'].loc[idx])
            mass = float(df_at_rm['mass'].loc[idx])
            charge = float(df_at_rm['charge'].loc[idx])
            ptype = df_at_rm['ptype'].loc[idx]
            c6 = float(df_at_rm['c6'].loc[idx])
            c12 = float(df_at_rm['c12'].loc[idx])

            f.write("{:>5}{:>5d}{:>11.3f}{:>11.3f}{:>6}{:>25.10f}{:>25.7e}\n".format(name,
                        atnum, mass, charge, ptype, c6, c12))

        # Escribiendo '[ nonbond_params ]'
        # ;	i	j	func	c6	c12
        f.write("\n")
        f.write('[ nonbond_params ]\n')
        f.write(';       i        j   func       c6           c12\n')

        for idx in df_nb_rm.index:

            i = df_nb_rm['i'].loc[idx]
            j = df_nb_rm['j'].loc[idx]
            func = int(df_nb_rm['func'].loc[idx])
            c6 = float(df_nb_rm['c6'].loc[idx])
            c12 = float(df_nb_rm['c12'].loc[idx])

            f.write("{:>9}{:>9}{:>6d}{:>14.10f}{:>15.7e}\n".format(i, j, func, c6, c12))

        # Escribiendo '[ pairtypes ]'
        # ;	i	j	func	c6	c12
        f.write("\n")
        f.write('[ pairtypes ]\n')
        f.write(';       i        j   func       c6           c12\n')

        for idx in df_pt_rm.index:

            i = df_pt_rm['i'].loc[idx]
            j = df_pt_rm['j'].loc[idx]
            func = int(df_pt_rm['func'].loc[idx])
            c6 = float(df_pt_rm['c6'].loc[idx])
            c12 = float(df_pt_rm['c12'].loc[idx])

            f.write("{:>9}{:>9}{:>6d}{:>14.10f}{:>15.7e}\n".format(i, j, func, c6, c12))

        f.close()
        
        dP_LVL1['FFNB_RM'] = PATH_FFNB_RM
        
        return 
    

    def create_topol(self, **kwargs):
        
        CARPET = kwargs.get("carpet", "carpeta")
        
        dP_LVL0 = kwargs.get("dP_LVL0", {})
        dP_LVL1 = kwargs.get("dP_LVL1", {})
        
        NAME_DIN = dP_LVL1['NAME_DIN']        

        PATH_GRL1 = dP_LVL1['GRL1']
        PATH_CELDA0 = dP_LVL1['CELDA0']
        PATH_FFNB_RM = dP_LVL1['FFNB_RM']

        path_ffb_in_g016 = dP_LVL0['PATH_FF_ISO']
        path_ffb_in_aot = dP_LVL0['PATH_FF_AOT']
        path_ffb_in_h2o = dP_LVL0['PATH_FF_H20']
        path_ffb_in_na = dP_LVL0['PATH_FF_NA']
        # path_ffb_in_conta = dP_LVL0['PATH_FF_CONTA']
        path_gromos54a7_atb = dP_LVL0['PATH_FF_GROMOS54A7_ATB']         
        
        PATH_CARPET = os.path.join(PATH_GRL1, CARPET)
        PATH_FOLDER_FF = os.path.join(PATH_CARPET, "forcefield")

        path_b_g016 = os.path.join(PATH_FOLDER_FF, "ffbounded_g016.itp")
        path_b_aot = os.path.join(PATH_FOLDER_FF, "ffbounded_aot.itp")
        path_b_h2o = os.path.join(PATH_FOLDER_FF, "ffbounded_h2o.itp")
        path_b_na = os.path.join(PATH_FOLDER_FF, "ffbounded_na.itp")
        # path_b_conta = os.path.join(PATH_FOLDER_FF, "ffbounded_conta.itp")

        _ = [path_b_g016, path_b_aot, path_b_h2o, path_b_na]
         # _ = [path_b_g016, path_b_aot, path_b_h2o, path_b_na, path_b_conta]
        paths_ffb = [os.path.split(path)[1] for path in _]

        tp.get_ffbonded_g016(path_ffb_in=path_ffb_in_g016, path_ffb_out=path_b_g016)
        tp.get_ffbonded_aot(path_ffb_in=path_ffb_in_aot, path_ffb_out=path_b_aot)
        tp.get_ffbonded_h2o(path_ffb_in=path_ffb_in_h2o, path_ffb_out=path_b_h2o)
        tp.get_ffbonded_na(path_ffb_in=path_ffb_in_na, path_ffb_out=path_b_na)
        # tp.get_ffbonded_conta(path_ffb_in=path_ffb_in_conta, path_ffb_out=path_b_conta)

        PATH_FF = tp.create_ff(path_folder_ff=PATH_FOLDER_FF,
                            name_din=NAME_DIN,
                            paths_ffnb=[os.path.split(PATH_FFNB_RM)[1]],
                            paths_ffb=paths_ffb,
                            nfunc=1, comb_rule=1, gen_pairs='yes', fudLJ=1.0, fudgeQQ=1.0)

        PATH_FF = "./forcefield/" + os.path.split(PATH_FF)[-1]

        gro_celda0 = groFile(PATH_CELDA0)
        PATH_TOPOL = os.path.join(PATH_CARPET, "topol.top")
        tp.create_topol(gro_celda0 = gro_celda0,
                          name_ciclo=NAME_DIN,
                          path_ff=PATH_FF,
                          path_topol=PATH_TOPOL)

        dP_LVL1['TOPOL'] = PATH_TOPOL
        
        return    
   
    def do_min1(self, **kwargs):
        
        dP_LVL1 = kwargs.get("dP_LVL1", {})
        
        PATH_TOPOL = dP_LVL1['TOPOL']
        PATH_CELDA0 = dP_LVL1['CELDA0']
        
        NUM_PROC = kwargs.get("num_proc", 4)
        nsteps = kwargs.get("nsteps", 100)
        gmx = kwargs.get("gmx", "NULL")

        df_min1 = call_grompp.call_estandar_min_001(nsteps=nsteps)
        herr.create_grompp(path_grompp=dP_LVL1['MIN1_MDP'],
                           df_grompp=df_min1)  
        
        herr.copy_file_to(path_in=PATH_CELDA0, path_out=dP_LVL1['MIN1_CONF'])

        cmd = [gmx, 'grompp',
               '-f', dP_LVL1['MIN1_MDP'],
               '-p', PATH_TOPOL, 
               '-c', dP_LVL1['MIN1_CONF'],
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
    
    
    
    def do_min2(self, **kwargs):
        
        NUM_PROC = kwargs.get("num_proc", 4)
        nsteps = kwargs.get("nsteps", 100)
        gmx = kwargs.get("gmx", "NULL")

        dP_LVL1 = kwargs.get("dP_LVL1", {}) 
        name_din = dP_LVL1['NAME_DIN']        
    
        df_min2 = call_grompp.call_estandar_min_002(nsteps=nsteps)
        herr.create_grompp(path_grompp=dP_LVL1['MIN2_MDP'],
                           df_grompp=df_min2)
        
        self.top_to_cop(path_carpet_in=dP_LVL1['GRLMIN1'],
                        path_carpet_out=dP_LVL1['GRLMIN2'])
        
       
        herr.copy_file_to(path_in=dP_LVL1['MIN1_CONFOUT'], path_out=dP_LVL1['MIN2_CONF'])

        to = time.time()
        cmd = [gmx, 'grompp',
               '-f', dP_LVL1['MIN2_MDP'],          # input
               '-p', dP_LVL1['MIN2_TOPOL'],                   # input
               '-c', dP_LVL1['MIN2_CONF'],      # input 
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
    
    
    

    def top_to_cop(self, **kwargs):

        PATH_CARPET_IN = kwargs.get("path_carpet_in", "NULL")
        PATH_CARPET_OUT = kwargs.get("path_carpet_out", "NULL")
        
        PATH_CARPET_FF_IN = os.path.join(PATH_CARPET_IN, "forcefield")
        PATH_CARPET_FF_OUT = os.path.join(PATH_CARPET_OUT, "forcefield")
        herr.copy_folder_to(path_in=PATH_CARPET_FF_IN, path_out=PATH_CARPET_FF_OUT)
        
        PATH_TOPOL_IN = os.path.join(PATH_CARPET_IN, "topol.top")
        PATH_TOPOL_OUT = os.path.join(PATH_CARPET_OUT, "topol.top")
        herr.copy_file_to(path_in=PATH_TOPOL_IN, path_out=PATH_TOPOL_OUT)
 
        return 
    
    
    
    
    
    
    def wrapper_nvt1(self, **kwargs):
        
        NUM_PROC = kwargs.get("num_proc", 4)
        nsteps = kwargs.get("nsteps", 100)
        gmx = kwargs.get("gmx", "NULL")

        dP_LVL1 = kwargs.get("dP_LVL1", {}) 
        name_din = dP_LVL1['NAME_DIN']     
        
        dt = kwargs.get("dt", 0.002)
        
        temp=kwargs.get("temp", "300.0")
        rcoulomb = kwargs.get('rcoulomb', 1.5)
        rvdw = kwargs.get('rvdw', 1.5)
        tc_grps = kwargs.get('tc_grps', 'system')
        pbc = kwargs.get('pbc', 'xyz')
        
        nstout=kwargs.get('nstout', 1)
        nstlog=kwargs.get('nstlog', 1)
        
        df_nvt1 = call_grompp.call_estandar_nvt_000(nsteps=nsteps,
                                                    dt=dt,
                                                    rcoulomb=rcoulomb,
                                                    rvdw=rvdw,
                                                    tc_grps=tc_grps,
                                                    nstxout=nstout,
                                                    nstvout=nstout,
                                                    nstenergy=nstout,
                                                    nstlog=nstlog,
                                                    pbc=pbc,
                                                    temp=temp)

        herr.create_grompp(path_grompp=dP_LVL1['NVT1_MDP'], df_grompp=df_nvt1)
        
        self.top_to_cop(path_carpet_in=dP_LVL1['GRLMIN2'],
                        path_carpet_out=dP_LVL1['GRLNVT1'])          

        herr.copy_file_to(path_in=dP_LVL1['MIN2_CONFOUT'], path_out=dP_LVL1['NVT1_CONF'])
        
        
        to = time.time()
        cmd = [gmx, 'grompp',
               '-f', dP_LVL1['NVT1_MDP'],
               '-p', dP_LVL1['NVT1_TOPOL'],         
               '-c', dP_LVL1['NVT1_CONF'],  
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
        
    
    
    
    
