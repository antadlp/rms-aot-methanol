import pandas as pd
import numpy as np
import time
import datetime
import sys
import os
import subprocess 
from scipy.signal import savgol_filter
from scipy.signal import argrelextrema
from scipy.signal import find_peaks
import getpass
from call_grompp_conf import *
import os
from itertools import combinations 
from groFile import *
from herramientas import *


masa_molar_agua = 18
Na = 6.022*1e23


class topoles(object):
    
    PATH_AOT_RM = "../data/general/forcefields/63UD_GROMACS_G54A7FF_allatom_UDD.itp"
    PATH_HOH_RM = "../data/general/forcefields/spce_54a7_atb_hoh.itp"
    PATH_NA_RM  = "../data/general/forcefields/E0XM_GROMACS_G54A7FF_allatom_original.itp"
    PATH_ISO_RM = "../data/general/forcefields/G016_ffbonded_zero_charge.itp"
    PATH_GROMOS54A7_ATB = "../data/general/forcefields/ffnonbonded_gromos54a7_atb_original.itp"
    
    def fsigma(self, c6, c12):
        return np.power((c12/c6), 1/6)

    def feps(self, c6, c12):
        return c6*c6/(4*c12)

    def fc6(self, sigma, eps):
        return 4*eps*np.power(sigma, 6)

    def fc12(self, sigma, eps):
        return 4*eps*np.power(sigma, 12)



    def create_topol(self, **kwargs):

        user = kwargs.get('user', 'NULL')

        # dar celda 0
        gro_celda0 = kwargs.get('gro_celda0', 'NULL')
        dic_celda0 = gro_celda0.get_general_info()
        dfn_celda0 = gro_celda0.get_mols_info()

        # name ciclo
        NAME_CICLO = kwargs.get('name_ciclo', 'NULL')

        # dado, arbitrario
        path_ff = kwargs.get('path_ff', 'NULL')
        PATH_FF = path_ff

        # El path del topol debe estar libre donde estan las carpetas
        PATH_TOPOL = kwargs.get('path_topol', 'NULL')

        f = open(PATH_TOPOL, 'w')
        f.write("#include ")
        f.write('"' + PATH_FF + '"')
        f.write("\n\n")
        f.write("[ system ]\n")
        f.write(NAME_CICLO)
        f.write("\n\n")
        f.write("[ molecules ]\n")
        for idx in dfn_celda0.index:
            
            tipo_mol = dfn_celda0['tipo mol'].loc[idx]
            total_num = dfn_celda0['total num'].loc[idx]
            f.write("{:>5}{:>5}\n".format(tipo_mol, total_num))
            
            
        f.close()

        return 



    def gen_nonbonded_G016(self, **kwargs):
        
        PATH_ATYPES_G016 = '../data/general/forcefields/G016_atypes.pkl'
        PATH_ATYPES = kwargs.get('path_atypes', PATH_ATYPES_G016)
        
        PATH_ATOMS_G016 = '../data/general/forcefields/G016_atoms.pkl'
        PATH_ATOMS = kwargs.get('path_atoms', PATH_ATOMS_G016)
        
        PATH_GRL1 = kwargs.get('path_grl1', 'NULL')
        NAME_DIN = kwargs.get('name_din', 'NULL')
        
        PATH_FOLDER_FF = os.path.join(PATH_GRL1, 'forcefield')
        cmd = ['mkdir', '-p', PATH_FOLDER_FF]
        process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)
        
        PATH_OUTPUT = os.path.join(PATH_FOLDER_FF, 'ffnonbonded_G016_' + NAME_DIN + '.itp')
        
        NAME_ATYPES = 'atypes_base_' + NAME_DIN + '.pkl'
        CP_PATH_ATYPES = os.path.join(PATH_FOLDER_FF, NAME_ATYPES)
        
        NAME_ATOMS = 'atoms_base_' + NAME_DIN + '.pkl'
        CP_PATH_ATOMS = os.path.join(PATH_FOLDER_FF, NAME_ATOMS)

        sigma_factor = kwargs.get('sigma_factor', 1)
        eps_factor = kwargs.get('epsilon_factor', 1)

        df_atypes = pd.read_pickle(PATH_ATYPES)
        df_atoms = pd.read_pickle(PATH_ATOMS)
        
        df_atypes.to_pickle(CP_PATH_ATYPES)
        df_atoms.to_pickle(CP_PATH_ATOMS)

        df_a2 = df_atoms[['type', 'mass', 'charge']].drop_duplicates()
        df_a2 = df_a2.set_index('type')    

        param_flag = kwargs.get('param_flag', 'c6_c12')
        # otra: sigma_eps

        if (param_flag == 'c6_c12'):
            cA = 'c6'
            cB = 'c12'
        elif (param_flag == 'sigma_eps'):
            cA = 'sigma'
            cB = 'epsilon'
        else:
            cA = 'cA'
            cB = 'cB'

        f = open(PATH_OUTPUT, 'w')

        #####################################
        ####   ATYPES
        f.write('[ atomtypes ]\n')
        f.write('; name  at.num   mass      charge  ptype       {}         {}\n'.format(cA, cB))
        for idx in df_atypes.index:

            name = df_atypes['name'].loc[idx]
            atnum = df_atypes['at.num'].loc[idx]
            mass = df_a2['mass'].loc[name]
            charge = df_a2['charge'].loc[name]
            ptype = df_atypes['ptype'].loc[idx]

            # sigma cambia por c6 
            # epsilon cambia por c12, 393Pp 2019 V
            c6 = df_atypes['c6'].loc[idx]
            c12 = df_atypes['c12'].loc[idx]

            sigma = self.fsigma(c6, c12)
            eps = self.feps(c6, c12)

            sigma = sigma*sigma_factor
            eps = eps*eps_factor

            if (param_flag == 'c6_c12'):
                c6 = self.fc6(sigma, eps)
                c12 = self.fc12(sigma, eps)
                f.write("{:>5}{:>5d}{:>11.3f}{:>11.3f}{:>6}{:>14.10f}{:>15.7e}\n".format(name, atnum,
                                         0.0, 0.0, ptype, c6, c12))        
            elif (param_flag == 'sigma_eps'):
                f.write("{:>5}{:>5d}{:>11.3f}{:>11.3f}{:>6}{:>14.10f}{:>15.7e}\n".format(name, atnum,
                                         0.0, 0.0, ptype, sigma, eps))        
            else:
                c6 = self.fc6(sigma, eps)
                c12 = self.fc12(sigma, eps)
                f.write("{:>5}{:>5d}{:>11.3f}{:>11.3f}{:>6}{:>14.10f}{:>15.7e}\n".format(name, atnum,
                                         0.0, 0.0, ptype, c6, c12))        


        f.close()


        return PATH_OUTPUT
        
            
    def gen_nonbonded_G016_2(self, **kwargs):
        
        sigma_factor = kwargs.get('sigma_factor', 1)
        eps_factor = kwargs.get('epsilon_factor', 1)
        
        path_top_g016 = kwargs.get("path_top_g016", self.PATH_ISO_RM)
        DFB_ATOMS = self.get_binfo_g016()["[ atoms ]"]
        dfb_g016 = kwargs.get('dfb_atoms', DFB_ATOMS)
        atoms_g016 = dfb_g016['type'].unique()

        path_top_54a7 = kwargs.get("path_top_54a7", self.get_nbinfo_gromos54a7_atb)
        dic_54a7 = self.get_nbinfo_gromos54a7_atb(path_top=path_top_54a7) 
        DF_FFNB = dic_54a7['[ atomtypes ]']
        df_ffnb = kwargs.get("df_ffnb", DF_FFNB)

        decimals = kwargs.get("decimals", 9)

        dfNb_g016 = df_ffnb.loc[df_ffnb['name'].isin(atoms_g016)]

        new_values = {}
        new_values['c6'] = {}
        new_values['c12'] = {}
        for idx in dfNb_g016.index:

            c6 = float(dfNb_g016['c6'].loc[idx])
            c12 = float(dfNb_g016['c12'].loc[idx])

            sigma = self.fsigma(c6, c12)
            eps = self.feps(c6, c12)

            sigma = sigma*sigma_factor
            eps = eps*eps_factor
            
            c6  = self.fc6(sigma, eps)
            c12 = self.fc12(sigma, eps)
            
            new_values['c6'][idx] = str(np.round(c6, decimals=decimals))
            new_values['c12'][idx] = str(np.round(c12, decimals=decimals))
        
        df = pd.DataFrame(new_values)
        
        df1 = dfNb_g016.copy()
    #     df2 = df_ffnb.copy()

        df1.update(df)
    #     df2.update(df)
                    
        return df1


    def gen_bonded_G016(self, **kwargs):

        PATH_GRL1 = kwargs.get('path_grl1', 'NULL')
        NAME_DIN = kwargs.get('name_din', 'NULL')

        PATH_FOLDER_FF = os.path.join(PATH_GRL1, 'forcefield')

        PATH_OUTPUT = os.path.join(PATH_FOLDER_FF, 'ffbonded_G016_' + NAME_DIN + '.itp')
    
        PATH_B_G016 = '../data/general/forcefields/G016_ffbonded.itp'
        PATH_B_G016 = kwargs.get('path_b_g016', PATH_B_G016)

        cmd = ['mkdir', '-p', PATH_FOLDER_FF]
        process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)

        cmd = ['cp', PATH_B_G016, PATH_OUTPUT]
        process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)

        return PATH_OUTPUT



    def create_ff(self, **kwargs):
        
        nfunc = kwargs.get('nfunc', 1)
        comb_rule = kwargs.get('comb_rule', 1)
        gen_pairs = kwargs.get('gen_pairs', 'yes')
        fudgeLJ = kwargs.get('fudLJ', 1.0)
        fudgeQQ = kwargs.get('fudgeQQ', 1.0)
        
        PATHS_FFNB = kwargs.get('paths_ffnb', [])
        PATHS_FFB = kwargs.get('paths_ffb', [])
        
        PATH_FOLDER_FF = kwargs.get("path_folder_ff", "forcefield")
        NAME_DIN = kwargs.get('name_din', 'NULL')
        
        cmd = ['mkdir', '-p', PATH_FOLDER_FF]
        process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)
        
        PATH_OUTPUT = os.path.join(PATH_FOLDER_FF, 'forcefield_' + NAME_DIN + '.itp')
        
        f = open(PATH_OUTPUT, 'w')
        
        f.write('[ defaults ]\n')
        f.write('; nbfunc	comb-rule	gen-pairs	fudgeLJ	fudgeQQ\n')
        f.write('     {}              {}             {}             {}     {}\n'.format(nfunc,
                                                         comb_rule,
                                                         gen_pairs,
                                                         fudgeLJ,
                                                         fudgeQQ))
        f.write("\n\n")
        
        for ffnb in PATHS_FFNB:
            
            f.write("#include ")
            f.write('"' + ffnb + '"')
            f.write("\n")
        
        
        for ffb in PATHS_FFB:
            
            f.write("#include ")
            f.write('"' + ffb + '"')    
            f.write("\n")
        
        
        f.close()
        
        return PATH_OUTPUT
        
        
    def get_top_order_info(self, **kwargs):

        path_top = kwargs.get("path_top", "NULL")
        target_label = kwargs.get("target_label", "NULL")
        lines_to_data = kwargs.get("lines_to_data", "NULL")
        col_order = kwargs.get("col_order", "NULL")
        num_atoms = kwargs.get("num_atoms", "NULL")

        dic = {}
        for col in col_order:
            dic[col] = {}
        f = open(path_top, 'r')
        for line in f:
            if target_label in line:
                for i in range(lines_to_data):
                    next(f)
                idx = 0
                for i in range(num_atoms):
                    items = f.readline().split()
                    for col, item in zip(col_order, items):
                        dic[col][idx] = item
                    idx+=1

        f.close()
        df = pd.DataFrame(dic)

        return df
            

            
    def get_nbinfo_gromos54a7(self, **kwargs):
        
        dic = {}
        PATH_TOP = self.PATH_GROMOS54A7_ATB
        path_top = kwargs.get("path_top", PATH_TOP)

        # atomtypes
        target_label = "[ atomtypes ]"
        lines_to_data = 1
        col_order =   ["name",  "at.num",   "mass",    "charge",   "ptype",        "c6",          "c12"]
        num_atoms = 71 # numero de atomtypes en gromos54a7 atb, cuidado! solo con ese ff
        
        df = self.get_top_order_info(path_top=path_top,
                              target_label=target_label,
                              lines_to_data=lines_to_data,
                              col_order=col_order,
                              num_atoms=num_atoms)
        dic[target_label] = df
        
        # nonbond_params
        target_label = "[ nonbond_params ]"
        lines_to_data = 1
        col_order = ["i", "j", "func", "c6", "c12"]
        num_atoms = 2437 # numero de nonbond_params en gromos54a7 atb, cuidado! solo con ese ff
        
        df = self.get_top_order_info(path_top=path_top,
                              target_label=target_label,
                              lines_to_data=lines_to_data,
                              col_order=col_order,
                              num_atoms=num_atoms)
        dic[target_label] = df
        
        # pairtypes
        target_label = "[ pairtypes ]"
        lines_to_data = 1
        col_order = ["i", "j", "func", "c6", "c12"]
        num_atoms = 2506 # numero de pairtypes en gromos54a7 atb, cuidado! solo con ese ff
       
        df = self.get_top_order_info(path_top=path_top,
                              target_label=target_label,
                              lines_to_data=lines_to_data,
                              col_order=col_order,
                              num_atoms=num_atoms)
        dic[target_label] = df       
        
        # pendiente funcion automatica que calcule los
        # num_atoms
        
        return dic
            
            
    def get_nbinfo_gromos54a7_atb(self, **kwargs):
        
        dic = {}
        PATH_TOP = self.PATH_GROMOS54A7_ATB
        path_top = kwargs.get("path_top", PATH_TOP)

        # atomtypes
        target_label = "[ atomtypes ]"
        lines_to_data = 1
        col_order =   ["name",  "at.num",   "mass",    "charge",   "ptype",        "c6",          "c12"]
        num_atoms = 71
        
        df = self.get_top_order_info(path_top=path_top,
                              target_label=target_label,
                              lines_to_data=lines_to_data,
                              col_order=col_order,
                              num_atoms=num_atoms)
        dic[target_label] = df
        
        # nonbond_params
        target_label = "[ nonbond_params ]"
        lines_to_data = 1
        col_order = ["i", "j", "func", "c6", "c12"]
        num_atoms = 2437
        
        df = self.get_top_order_info(path_top=path_top,
                              target_label=target_label,
                              lines_to_data=lines_to_data,
                              col_order=col_order,
                              num_atoms=num_atoms)
        dic[target_label] = df
        
        # pairtypes
        target_label = "[ pairtypes ]"
        lines_to_data = 1
        col_order = ["i", "j", "func", "c6", "c12"]
        num_atoms = 2506
       
        df = self.get_top_order_info(path_top=path_top,
                              target_label=target_label,
                              lines_to_data=lines_to_data,
                              col_order=col_order,
                              num_atoms=num_atoms)
        dic[target_label] = df   
        
        # pendiente funcion automatica que calcule los
        # num_atoms        
        
        return dic
            
    
    def get_binfo_g016(self, **kwargs):
        # G016_ffbonded_zero_charge.itp
        PATH_TOP = self.PATH_ISO_RM
        path_top = kwargs.get("path_top", PATH_TOP)
                
        target_label = "[ atoms ]"
        lines_to_data = 1
        col_order =   ["nr", "type", "resnr", "resid", "atom", "cgnr", "charge", "mass"]
        num_atoms = 8    
        
        dic = {}
        tp = topoles()
        df = self.get_top_order_info(path_top=path_top,
                              target_label=target_label,
                              lines_to_data=lines_to_data,
                              col_order=col_order,
                              num_atoms=num_atoms)
        
        dic = {}
        dic[target_label] = df
        
        return dic
            
                        
    def get_binfo_spce(self, **kwargs):
        
        PATH_TOP = self.PATH_HOH_RM
        path_top = kwargs.get("path_top", PATH_TOP)
        
        
        target_label = "[ atoms ]"
        lines_to_data = 2
        col_order =   ["nr", "type", "resnr", "resid", "atom", "cgnr", "charge", "mass"]
        num_atoms = 3 
        
        dic = {}
        tp = topoles()
        df = self.get_top_order_info(path_top=path_top,
                              target_label=target_label,
                              lines_to_data=lines_to_data,
                              col_order=col_order,
                              num_atoms=num_atoms)
        
        dic = {}
        dic[target_label] = df
        
        return dic

    def get_binfo_spc_54a7(self, **kwargs):
        
        PATH_TOP = self.PATH_HOH_RM
        path_top = kwargs.get("path_top", PATH_TOP)
        
        
        target_label = "[ atoms ]"
        lines_to_data = 1
        col_order =   ["nr", "type", "resnr", "resid", "atom", "cgnr", "charge", "mass"]
        num_atoms = 3 
        
        dic = {}
        tp = topoles()
        df = self.get_top_order_info(path_top=path_top,
                              target_label=target_label,
                              lines_to_data=lines_to_data,
                              col_order=col_order,
                              num_atoms=num_atoms)
        
        dic = {}
        dic[target_label] = df
        
        return dic
 
    def get_binfo_conta(self, **kwargs):
        
        path_top = kwargs.get("path_top", "NULL")
        num_atoms = kwargs.get("num_atoms", 6)
        lines_to_data = kwargs.get("lines_to_data", 1)
        
        
        target_label = "[ atoms ]"
        lines_to_data = 1
        col_order =   ["nr", "type", "resnr", "resid", "atom", "cgnr", "charge", "mass"]
        
        dic = {}
        tp = topoles()
        df = self.get_top_order_info(path_top=path_top,
                              target_label=target_label,
                              lines_to_data=lines_to_data,
                              col_order=col_order,
                              num_atoms=num_atoms)
        
        dic = {}
        dic[target_label] = df
        
        return dic
 


                
    def get_binfo_na(self, **kwargs):
        
        PATH_TOP = self.PATH_NA_RM 
        path_top = kwargs.get("path_top", PATH_TOP)
        
        
        target_label = "[ atoms ]"
        lines_to_data = 1
        col_order =   ["nr", "type", "resnr", "resid", "atom", "cgnr", "charge", "mass"]
        num_atoms = 1
        
        dic = {}
        tp = topoles()
        df = self.get_top_order_info(path_top=path_top,
                              target_label=target_label,
                              lines_to_data=lines_to_data,
                              col_order=col_order,
                              num_atoms=num_atoms)
        
        dic = {}
        dic[target_label] = df
        
        return dic
    
    
    def get_binfo_aot(self, **kwargs):
        
        PATH_TOP = self.PATH_AOT_RM
        path_top = kwargs.get("path_top", PATH_TOP)

        target_label = "[ atoms ]"
        lines_to_data = 1
        col_order =   ["nr", "type", "resnr", "resid", "atom", "cgnr", "charge", "mass"]
        num_atoms = 65    
        
        dic = {}
        df = self.get_top_order_info(path_top=path_top,
                              target_label=target_label,
                              lines_to_data=lines_to_data,
                              col_order=col_order,
                              num_atoms=num_atoms)
        dic = {}
        dic[target_label] = df
        
        return dic        
        

    def get_ffnb_rm(self, **kwargs):
        
        USER = getpass.getuser()
        user = kwargs.get('user', USER) # <==

        NAME_DIN = kwargs.get("name_din", "PruebaX") # <==
        CARPET = kwargs.get("carpet", "carpeta")

        PATH_GRL0 = "/home/{}/Documents/rm_radios_varios".format(user)
        PATH_GRL0 = kwargs.get("path_grl0", PATH_GRL0) # <==
        
        PATH_GRL1 = os.path.join(PATH_GRL0, NAME_DIN)
        PATH_GRL2 = os.path.join(PATH_GRL1, CARPET)
        PATH_GRL2 = os.path.join(PATH_GRL2, "forcefield")

        NAME_FFNB = "ffnb_" + NAME_DIN + ".itp"
        PATH_FFNB_RM = os.path.join(PATH_GRL2, NAME_FFNB)
        PATH_FFNB_RM = kwargs.get("path_out", PATH_FFNB_RM)
        
        paths_to_create = [PATH_GRL0, PATH_GRL1, PATH_GRL2]
        for path in paths_to_create:
            cmd = ['mkdir', '-p', path]
            cmd = [str(item) for item in cmd]
            process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)
            
        path_ffb_in_g016 = kwargs.get("path_ffb_in_g016", self.PATH_ISO_RM)
        path_ffb_in_aot = kwargs.get("path_ffb_in_aot", self.PATH_AOT_RM)
        path_ffb_in_h2o = kwargs.get("path_ffb_in_hoh", self.PATH_HOH_RM)
        path_ffb_in_na = kwargs.get("path_ffb_in_na", self.PATH_NA_RM)            
        path_gromos54a7_atb = kwargs.get("path_gromos54a7_atb", self.PATH_GROMOS54A7_ATB)

        # atomtypes de aot
        df = self.get_binfo_aot(path_top=path_ffb_in_aot)["[ atoms ]"]
        at_aot = df["type"].unique()

        # atypes de g016
        df = self.get_binfo_g016(path_top=path_ffb_in_g016)["[ atoms ]"]
        at_g016 = df["type"].unique()
        comb = combinations(at_g016, 2)
        comb_g016 = [(i[0], i[1]) for i in list(comb)]

        # atypes de spce
#         df = self.get_binfo_spce(path_top=path_ffb_in_h2o)["[ atoms ]"]
        df = self.get_binfo_spc_54a7(path_top=path_ffb_in_h2o)["[ atoms ]"]
        at_spce = df["type"].unique()

        # atypes de na
        df = self.get_binfo_na(path_top=path_ffb_in_na)["[ atoms ]"]
        at_na = df["type"].unique()

        # juntando a todos
        rm_atypes = np.concatenate((at_aot, at_g016, at_spce, at_na)).astype(str)
        comb = combinations(rm_atypes, 2) 
        comb_atypes = [(i[0], i[1]) for i in list(comb)]

        self_comb = [(mol, mol) for mol in rm_atypes]
        all_comb_atypes = comb_atypes.copy()
        all_comb_atypes.extend(self_comb)

        # query de ffnbounded 54a7 atb
        df_54a7_at = self.get_nbinfo_gromos54a7_atb(path_top=path_gromos54a7_atb)['[ atomtypes ]']
        df_54a7_nb = self.get_nbinfo_gromos54a7_atb(path_top=path_gromos54a7_atb)['[ nonbond_params ]']
        df_54a7_pt = self.get_nbinfo_gromos54a7_atb(path_top=path_gromos54a7_atb)['[ pairtypes ]']


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
        epsilon_factor = kwargs.get("epsilon_factor", 1.0) # <==
        sigma_factor = kwargs.get("sigma_factor", 1.0)
        df_mod_g016 = self.gen_nonbonded_G016_2(epsilon_factor=epsilon_factor,
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
            mass = np.float(df_at_rm['mass'].loc[idx])
            charge = np.float(df_at_rm['charge'].loc[idx])
            ptype = df_at_rm['ptype'].loc[idx]
            c6 = np.float(df_at_rm['c6'].loc[idx])
            c12 = np.float(df_at_rm['c12'].loc[idx])

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
            df_nb_rm.to_excel("ver.xlsx")
            df_nb_rm.to_pickle("ver.pkl")
            func = np.int(df_nb_rm['func'].loc[idx])
            c6 = np.float(df_nb_rm['c6'].loc[idx])
            c12 = np.float(df_nb_rm['c12'].loc[idx])

            f.write("{:>9}{:>9}{:>6d}{:>14.10f}{:>15.7e}\n".format(i, j, func, c6, c12))

        # Escribiendo '[ pairtypes ]'
        # ;	i	j	func	c6	c12
        f.write("\n")
        f.write('[ pairtypes ]\n')
        f.write(';       i        j   func       c6           c12\n')

        for idx in df_pt_rm.index:

            i = df_pt_rm['i'].loc[idx]
            j = df_pt_rm['j'].loc[idx]
            func = np.int(df_pt_rm['func'].loc[idx])
            c6 = np.float(df_pt_rm['c6'].loc[idx])
            c12 = np.float(df_pt_rm['c12'].loc[idx])

            f.write("{:>9}{:>9}{:>6d}{:>14.10f}{:>15.7e}\n".format(i, j, func, c6, c12))

        f.close()
        
        return PATH_FFNB_RM


    def get_ffbonded_g016(self, **kwargs):
        
        PATH_FFB_IN = self.PATH_ISO_RM 
        PATH_FFB_IN = kwargs.get("path_ffb_in", PATH_FFB_IN)
        
        PATH_FFB_OUT = kwargs.get("path_ffb_out", "NULL")
        
        _ = os.path.split(PATH_FFB_OUT)   

        cmd = ['mkdir', '-p', _[0]]
        process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)

        cmd = ['cp', PATH_FFB_IN, PATH_FFB_OUT]
        process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)

        return
        
            
    def get_ffbonded_aot(self, **kwargs):
        
        PATH_FFB_IN = self.PATH_AOT_RM
        PATH_FFB_IN = kwargs.get("path_ffb_in", PATH_FFB_IN)
        
        PATH_FFB_OUT = kwargs.get("path_ffb_out", "NULL")
        
        _ = os.path.split(PATH_FFB_OUT)   

        cmd = ['mkdir', '-p', _[0]]
        process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)

        cmd = ['cp', PATH_FFB_IN, PATH_FFB_OUT]
        process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)

        return


    def get_ffbonded_h2o(self, **kwargs):
        
        PATH_FFB_IN = self.PATH_HOH_RM 
        PATH_FFB_IN = kwargs.get("path_ffb_in", PATH_FFB_IN)
        
        PATH_FFB_OUT = kwargs.get("path_ffb_out", "NULL")
        
        _ = os.path.split(PATH_FFB_OUT)   

        cmd = ['mkdir', '-p', _[0]]
        process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)

        cmd = ['cp', PATH_FFB_IN, PATH_FFB_OUT]
        process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)

        return

    def get_ffbonded_na(self, **kwargs):
        
        PATH_FFB_IN = self.PATH_NA_RM 
        PATH_FFB_IN = kwargs.get("path_ffb_in", PATH_FFB_IN)
        
        PATH_FFB_OUT = kwargs.get("path_ffb_out", "NULL")
        
        _ = os.path.split(PATH_FFB_OUT)   

        cmd = ['mkdir', '-p', _[0]]
        process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)

        cmd = ['cp', PATH_FFB_IN, PATH_FFB_OUT]
        process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)

        return        

    def get_ffbonded_conta(self, **kwargs):
        
        PATH_FFB_IN = kwargs.get("path_ffb_in", "NULL")
        
        PATH_FFB_OUT = kwargs.get("path_ffb_out", "NULL")
        
        _ = os.path.split(PATH_FFB_OUT)   

        cmd = ['mkdir', '-p', _[0]]
        process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)

        cmd = ['cp', PATH_FFB_IN, PATH_FFB_OUT]
        process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)

        return        




    def wrapper_create_topol_rm(self, **kwargs):

        PATH_GRL1 = kwargs.get("path_grl1", "NULL")
        CARPET = kwargs.get("carpet", "NULL")
        PATH_RMNOMEDC = kwargs.get("path_rmnomedc", "NULL")
        PATH_FFNB_RM = kwargs.get("path_ffnb_rm", "NULL")
        NAME_DIN = kwargs.get("name_din", "NULL")

        path_ffb_in_g016 = kwargs.get("path_ffb_in_g016", self.PATH_ISO_RM)
        path_ffb_in_aot = kwargs.get("path_ffb_in_aot", self.PATH_AOT_RM)
        path_ffb_in_h2o = kwargs.get("path_ffb_in_hoh", self.PATH_HOH_RM)
        path_ffb_in_na = kwargs.get("path_ffb_in_na", self.PATH_NA_RM)
        
        PATH_CARPET = os.path.join(PATH_GRL1, CARPET)
        PATH_FOLDER_FF = os.path.join(PATH_CARPET, "forcefield")

        path_b_g016 = os.path.join(PATH_FOLDER_FF, "ffbounded_g016.itp")
        path_b_aot = os.path.join(PATH_FOLDER_FF, "ffbounded_aot.itp")
        path_b_h2o = os.path.join(PATH_FOLDER_FF, "ffbounded_h2o.itp")
        path_b_na = os.path.join(PATH_FOLDER_FF, "ffbounded_na.itp")

        _ = [path_b_g016, path_b_aot, path_b_h2o, path_b_na]
        paths_ffb = [os.path.split(path)[1] for path in _]

        self.get_ffbonded_g016(path_ffb_in=path_ffb_in_g016, path_ffb_out=path_b_g016)
        self.get_ffbonded_aot(path_ffb_in=path_ffb_in_aot, path_ffb_out=path_b_aot)
        self.get_ffbonded_h2o(path_ffb_in=path_ffb_in_h2o, path_ffb_out=path_b_h2o)
        self.get_ffbonded_na(path_ffb_in=path_ffb_in_na, path_ffb_out=path_b_na)

        PATH_FF = self.create_ff(path_folder_ff=PATH_FOLDER_FF,
                            name_din=NAME_DIN,
                            paths_ffnb=[os.path.split(PATH_FFNB_RM)[1]],
                            paths_ffb=paths_ffb,
                            nfunc=1, comb_rule=1, gen_pairs='yes', fudLJ=1.0, fudgeQQ=1.0)

        PATH_FF = "./forcefield/" + os.path.split(PATH_FF)[-1]

        gro_celda0 = groFile(PATH_RMNOMEDC)
        PATH_TOPOL = os.path.join(PATH_CARPET, "topol.top")
        self.create_topol(gro_celda0 = gro_celda0,
                          name_ciclo=NAME_DIN,
                          path_ff=PATH_FF,
                          path_topol=PATH_TOPOL)


        return PATH_TOPOL

    def top_to_cop_rm(self, **kwargs):

        PATH_CARPET_IN = kwargs.get("path_carpet_in", "NULL")
        PATH_CARPET_OUT = kwargs.get("path_carpet_out", "NULL")
        NAME_DIN = kwargs.get("name_din", "NULL")
        
        PATH_CARPET_IN_FF = os.path.join(PATH_CARPET_IN, "forcefield")
        PATH_CARPET_OUT_FF = os.path.join(PATH_CARPET_OUT, "forcefield")

        cmd = ['mkdir', '-p', PATH_CARPET_OUT_FF]
        cmd = [str(item) for item in cmd]
        process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)

        NAME_FFF = "forcefield_" + NAME_DIN + ".itp"
        NAME_FF_NA = "ffbounded" + "_na.itp"
        NAME_FF_H2O = "ffbounded" + "_h2o.itp"
        NAME_FF_AOT = "ffbounded" + "_aot.itp"
        NAME_FF_G016 = "ffbounded" + "_g016.itp"
        NAME_FFNB = "ffnb_" + NAME_DIN + ".itp"
        NAME_TOPOL = "topol.top"

        NAME_TOPOL = kwargs.get("name_topol", NAME_TOPOL)
        NAME_FFF = kwargs.get("name_fff", NAME_FFF)
        NAME_FF_NA = kwargs.get("name_ff_na", NAME_FF_NA)
        NAME_FF_H2O = kwargs.get("name_ff_h2o", NAME_FF_H2O)
        NAME_FF_AOT = kwargs.get("name_ff_aot", NAME_FF_AOT)
        NAME_FF_G016 = kwargs.get("name_ff_g016", NAME_FF_G016)
        NAME_FFNB = kwargs.get("name_ffnb", NAME_FFNB)

        PATH_TOPOL_IN = os.path.join(PATH_CARPET_IN, NAME_TOPOL)
        PATH_TOPOL_OUT = os.path.join(PATH_CARPET_OUT, NAME_TOPOL)
        
        PATH_FFF_IN = os.path.join(PATH_CARPET_IN_FF, NAME_FFF)
        PATH_FF_NA_IN = os.path.join(PATH_CARPET_IN_FF, NAME_FF_NA)
        PATH_FF_H2O_IN = os.path.join(PATH_CARPET_IN_FF, NAME_FF_H2O)
        PATH_FF_AOT_IN = os.path.join(PATH_CARPET_IN_FF, NAME_FF_AOT)
        PATH_FF_G016_IN = os.path.join(PATH_CARPET_IN_FF, NAME_FF_G016)
        PATH_FFNB_IN = os.path.join(PATH_CARPET_IN_FF, NAME_FFNB)

        PATH_FFF_OUT = os.path.join(PATH_CARPET_OUT_FF, NAME_FFF)
        PATH_FF_NA_OUT = os.path.join(PATH_CARPET_OUT_FF, NAME_FF_NA)
        PATH_FF_H2O_OUT = os.path.join(PATH_CARPET_OUT_FF, NAME_FF_H2O)
        PATH_FF_AOT_OUT = os.path.join(PATH_CARPET_OUT_FF, NAME_FF_AOT)
        PATH_FF_G016_OUT = os.path.join(PATH_CARPET_OUT_FF, NAME_FF_G016)
        PATH_FFNB_OUT = os.path.join(PATH_CARPET_OUT_FF, NAME_FFNB)

        PATH_TOPOL_IN = kwargs.get("path_topol_in", PATH_TOPOL_IN)
        PATH_FFF_IN =  kwargs.get("path_fff_in", PATH_FFF_IN)
        PATH_FF_NA_IN = kwargs.get("path_ff_na_in", PATH_FF_NA_IN)
        PATH_FF_H2O_IN = kwargs.get("path_ff_h2o_in", PATH_FF_H2O_IN)
        PATH_FF_AOT_IN = kwargs.get("path_ff_aot_in", PATH_FF_AOT_IN)
        PATH_FF_G016_IN = kwargs.get("path_ff_g016_in", PATH_FF_G016_IN)
        PATH_FFNB_IN = kwargs.get("path_ffnb_in", PATH_FFNB_IN)
        
        PATH_TOPOL_OUT = kwargs.get("path_topol_out", PATH_TOPOL_OUT)
        PATH_FFF_OUT =  kwargs.get("path_fff_out", PATH_FFF_OUT)
        PATH_FF_NA_OUT = kwargs.get("path_ff_na_out", PATH_FF_NA_OUT)
        PATH_FF_H2O_OUT = kwargs.get("path_ff_h2o_out", PATH_FF_H2O_OUT)
        PATH_FF_AOT_OUT = kwargs.get("path_ff_aot_out", PATH_FF_AOT_OUT)
        PATH_FF_G016_OUT = kwargs.get("path_ff_g016_out", PATH_FF_G016_OUT)
        PATH_FFNB_OUT = kwargs.get("path_ffnb_out", PATH_FFNB_OUT)        
        
        PATHS_IN = [PATH_TOPOL_IN,
        PATH_FFF_IN,
        PATH_FF_NA_IN, 
        PATH_FF_H2O_IN, 
        PATH_FF_AOT_IN,
        PATH_FF_G016_IN, 
        PATH_FFNB_IN]

        PATHS_OUT = [PATH_TOPOL_OUT,
        PATH_FFF_OUT,
        PATH_FF_NA_OUT, 
        PATH_FF_H2O_OUT, 
        PATH_FF_AOT_OUT,
        PATH_FF_G016_OUT, 
        PATH_FFNB_OUT]

        for path_in, path_out in zip(PATHS_IN, PATHS_OUT):
            cmd = ['cp', path_in, path_out]
            cmd = [str(item) for item in cmd]
            process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)
            
        return PATH_TOPOL_OUT


    def get_ffnb_no_rm(self, **kwargs):
        
        USER = getpass.getuser()
        user = kwargs.get('user', USER) # <==

        NAME_DIN = kwargs.get("name_din", "PruebaX") # <==
        CARPET = kwargs.get("carpet", "carpeta")

        PATH_GRL0 = "/home/{}/Documents/rm_radios_varios".format(user)
        PATH_GRL0 = kwargs.get("path_grl0", PATH_GRL0) # <==
        
        PATH_GRL1 = os.path.join(PATH_GRL0, NAME_DIN)
        PATH_GRL2 = os.path.join(PATH_GRL1, CARPET)
        PATH_GRL2 = os.path.join(PATH_GRL2, "forcefield")

        NAME_FFNB = "ffnb_" + NAME_DIN + ".itp"
        PATH_FFNB_RM = os.path.join(PATH_GRL2, NAME_FFNB)
        PATH_FFNB_RM = kwargs.get("path_out", PATH_FFNB_RM)
        
        paths_to_create = [PATH_GRL0, PATH_GRL1, PATH_GRL2]
        for path in paths_to_create:
            cmd = ['mkdir', '-p', path]
            cmd = [str(item) for item in cmd]
            process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)
            
        path_ffb_in_g016 = kwargs.get("path_ffb_in_g016", self.PATH_ISO_RM)
        path_ffb_in_aot = kwargs.get("path_ffb_in_aot", self.PATH_AOT_RM)
        path_ffb_in_h2o = kwargs.get("path_ffb_in_hoh", self.PATH_HOH_RM)
        path_ffb_in_na = kwargs.get("path_ffb_in_na", self.PATH_NA_RM)            
        path_gromos54a7_atb = kwargs.get("path_gromos54a7_atb", self.PATH_GROMOS54A7_ATB)

        # atomtypes de aot
        df = self.get_binfo_aot(path_top=path_ffb_in_aot)["[ atoms ]"]
        at_aot = df["type"].unique()

        # atypes de g016
        df = self.get_binfo_g016(path_top=path_ffb_in_g016)["[ atoms ]"]
        at_g016 = df["type"].unique()
        comb = combinations(at_g016, 2)
        comb_g016 = [(i[0], i[1]) for i in list(comb)]

        # atypes de spce
#         df = self.get_binfo_spce(path_top=path_ffb_in_h2o)["[ atoms ]"]
        df = self.get_binfo_spc_54a7(path_top=path_ffb_in_h2o)["[ atoms ]"]
        at_spce = df["type"].unique()

        # atypes de na
        df = self.get_binfo_na(path_top=path_ffb_in_na)["[ atoms ]"]
        at_na = df["type"].unique()

        # juntando a todos
        rm_atypes = np.concatenate((at_aot, at_g016, at_spce, at_na)).astype(str)
        comb = combinations(rm_atypes, 2) 
        comb_atypes = [(i[0], i[1]) for i in list(comb)]

        self_comb = [(mol, mol) for mol in rm_atypes]
        all_comb_atypes = comb_atypes.copy()
        all_comb_atypes.extend(self_comb)

        # query de ffnbounded 54a7 atb
        df_54a7_at = self.get_nbinfo_gromos54a7_atb(path_top=path_gromos54a7_atb)['[ atomtypes ]']
        df_54a7_nb = self.get_nbinfo_gromos54a7_atb(path_top=path_gromos54a7_atb)['[ nonbond_params ]']
        df_54a7_pt = self.get_nbinfo_gromos54a7_atb(path_top=path_gromos54a7_atb)['[ pairtypes ]']


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
        epsilon_factor = kwargs.get("epsilon_factor", 1.0) # <==
        sigma_factor = kwargs.get("sigma_factor", 1.0)
        df_mod_g016 = self.gen_nonbonded_G016_2(epsilon_factor=epsilon_factor,
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
            mass = np.float(df_at_rm['mass'].loc[idx])
            charge = np.float(df_at_rm['charge'].loc[idx])
            ptype = df_at_rm['ptype'].loc[idx]
            c6 = np.float(df_at_rm['c6'].loc[idx])
            c12 = np.float(df_at_rm['c12'].loc[idx])

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
            df_nb_rm.to_excel("ver.xlsx")
            df_nb_rm.to_pickle("ver.pkl")
            func = np.int(df_nb_rm['func'].loc[idx])
            c6 = np.float(df_nb_rm['c6'].loc[idx])
            c12 = np.float(df_nb_rm['c12'].loc[idx])

            f.write("{:>9}{:>9}{:>6d}{:>14.10f}{:>15.7e}\n".format(i, j, func, c6, c12))

        # Escribiendo '[ pairtypes ]'
        # ;	i	j	func	c6	c12
        f.write("\n")
        f.write('[ pairtypes ]\n')
        f.write(';       i        j   func       c6           c12\n')

        for idx in df_pt_rm.index:

            i = df_pt_rm['i'].loc[idx]
            j = df_pt_rm['j'].loc[idx]
            func = np.int(df_pt_rm['func'].loc[idx])
            c6 = np.float(df_pt_rm['c6'].loc[idx])
            c12 = np.float(df_pt_rm['c12'].loc[idx])

            f.write("{:>9}{:>9}{:>6d}{:>14.10f}{:>15.7e}\n".format(i, j, func, c6, c12))

        f.close()
        
        return PATH_FFNB_RM



    def get_ffnb_g016(self, **kwargs):
        
        NAME_DIN = kwargs.get("name_din", "NULL")

        PATH_GRL1 = kwargs.get("path_grl1", "NULL")
        PATH_GRL2 = os.path.join(PATH_GRL1, "forcefield")
        

        NAME_FFNB = "ffnb_" + NAME_DIN + ".itp"
        PATH_FFNB_RM = os.path.join(PATH_GRL2, NAME_FFNB)
        PATH_FFNB_RM = kwargs.get("path_out", PATH_FFNB_RM)
        
        paths_to_create = [PATH_GRL1, PATH_GRL2]
        for path in paths_to_create:
            cmd = ['mkdir', '-p', path]
            cmd = [str(item) for item in cmd]
            process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)
            
        path_ffb_in_g016 = kwargs.get("path_ffb_in_g016", self.PATH_ISO_RM)
        path_gromos54a7_atb = kwargs.get("path_gromos54a7_atb", self.PATH_GROMOS54A7_ATB)

        # atypes de g016
        df = self.get_binfo_g016(path_top=path_ffb_in_g016)["[ atoms ]"]
        at_g016 = df["type"].unique()
        comb = combinations(at_g016, 2)
        comb_g016 = [(i[0], i[1]) for i in list(comb)]

        # juntando a todos
#         rm_atypes = np.concatenate((at_aot, at_g016, at_spce, at_na)).astype(str)
        rm_atypes = at_g016.astype(str)
        comb = combinations(rm_atypes, 2) 
        comb_atypes = [(i[0], i[1]) for i in list(comb)]

        self_comb = [(mol, mol) for mol in rm_atypes]
        all_comb_atypes = comb_atypes.copy()
        all_comb_atypes.extend(self_comb)

        # query de ffnbounded 54a7 atb
        df_54a7_at = self.get_nbinfo_gromos54a7_atb(path_top=path_gromos54a7_atb)['[ atomtypes ]']
        df_54a7_nb = self.get_nbinfo_gromos54a7_atb(path_top=path_gromos54a7_atb)['[ nonbond_params ]']
        df_54a7_pt = self.get_nbinfo_gromos54a7_atb(path_top=path_gromos54a7_atb)['[ pairtypes ]']

        ## EXTRAYENDO ATYPES
        df_at_rm = df_54a7_at.loc[df_54a7_at['name'].isin(rm_atypes)]

        ## EXTRAYENDO NON BOUNDED PARAMS
        
#        # cheka para cada par, si el par
#        # ti = (a, b) o (b, a) pertenece a
#        # comb_g016, si pertenece lo descarta,
#        # si no pertenece lo agrega a comb_atypes
#        #_nog016
#        # aqui de antemano ya no hay ningun self comb,
#        # por eso se hace tj sobre comb_g016
#        comb_atypes_nog016 = []
#        for ti in comb_atypes:
#            flag_array = []
#            for tj in comb_g016:
#                i = frozenset(ti)
#                j = frozenset(tj)
#                if i == j:
#                    flag_array.append(False)
#                else:
#                    flag_array.append(True)
#
#            if np.all(flag_array):
#                comb_atypes_nog016.append(ti)
#
        idxs_nb = []
        for idx in df_54a7_nb.index:
            flag_array = []

            t1 = df_54a7_nb['i'].loc[idx]
            t2 = df_54a7_nb['j'].loc[idx]
            ti = (t1, t2)

            if t1 == t2:
                print(ti)

#           for tj in comb_atypes_nog016:
            for tj in all_comb_atypes:
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
        epsilon_factor = kwargs.get("epsilon_factor", 1.0) # <==
        sigma_factor = kwargs.get("sigma_factor", 1.0)
        df_mod_g016 = self.gen_nonbonded_G016_2(epsilon_factor=epsilon_factor,
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
            mass = np.float(df_at_rm['mass'].loc[idx])
            charge = np.float(df_at_rm['charge'].loc[idx])
            ptype = df_at_rm['ptype'].loc[idx]
            c6 = np.float(df_at_rm['c6'].loc[idx])
            c12 = np.float(df_at_rm['c12'].loc[idx])

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
            df_nb_rm.to_excel("ver.xlsx")
            df_nb_rm.to_pickle("ver.pkl")
            func = np.int(df_nb_rm['func'].loc[idx])
            c6 = np.float(df_nb_rm['c6'].loc[idx])
            c12 = np.float(df_nb_rm['c12'].loc[idx])

            f.write("{:>9}{:>9}{:>6d}{:>14.10f}{:>15.7e}\n".format(i, j, func, c6, c12))

        # Escribiendo '[ pairtypes ]'
        # ;	i	j	func	c6	c12
        f.write("\n")
        f.write('[ pairtypes ]\n')
        f.write(';       i        j   func       c6           c12\n')

        for idx in df_pt_rm.index:

            i = df_pt_rm['i'].loc[idx]
            j = df_pt_rm['j'].loc[idx]
            func = np.int(df_pt_rm['func'].loc[idx])
            c6 = np.float(df_pt_rm['c6'].loc[idx])
            c12 = np.float(df_pt_rm['c12'].loc[idx])

            f.write("{:>9}{:>9}{:>6d}{:>14.10f}{:>15.7e}\n".format(i, j, func, c6, c12))

        f.close()
        
        return PATH_FFNB_RM
    
    
    def wrapper_create_topol_g016(self, **kwargs):

        PATH_GRL1 = kwargs.get("path_grl1", "NULL")
        CARPET = kwargs.get("carpet", "NULL")
        PATH_RMNOMEDC = kwargs.get("path_celda0", "NULL")
        PATH_FFNB_RM = kwargs.get("path_ffnb_g016", "NULL")
        NAME_DIN = kwargs.get("name_din", "NULL")

        path_ffb_in_g016 = kwargs.get("path_ffb_in_g016", self.PATH_ISO_RM)

#         PATH_CARPET = os.path.join(PATH_GRL1, CARPET)
        PATH_CARPET = PATH_GRL1
        PATH_FOLDER_FF = os.path.join(PATH_CARPET, "forcefield")

        path_b_g016 = os.path.join(PATH_FOLDER_FF, "ffbounded_g016.itp")

        _ = [path_b_g016]
        paths_ffb = [os.path.split(path)[1] for path in _]

        self.get_ffbonded_g016(path_ffb_in=path_ffb_in_g016, path_ffb_out=path_b_g016)

        PATH_FF = self.create_ff(path_folder_ff=PATH_FOLDER_FF,
                            name_din=NAME_DIN,
                            paths_ffnb=[os.path.split(PATH_FFNB_RM)[1]],
                            paths_ffb=paths_ffb,
                            nfunc=1, comb_rule=1, gen_pairs='yes', fudLJ=1.0, fudgeQQ=1.0)

        PATH_FF = "./forcefield/" + os.path.split(PATH_FF)[-1]

        gro_celda0 = groFile(PATH_RMNOMEDC)
        PATH_TOPOL = os.path.join(PATH_CARPET, "topol.top")
        self.create_topol(gro_celda0 = gro_celda0,
                          name_ciclo=NAME_DIN,
                          path_ff=PATH_FF,
                          path_topol=PATH_TOPOL)


        return PATH_TOPOL
    
    def get_top_bounded(self, **kwargs):

        herr = herramientas()

        user = getpass.getuser()
        PATH_GRL0 = '/home/{}/Documents'.format(user)
        PATH_GRL0 = kwargs.get("path_grl0", PATH_GRL0)
        NAME_CARPET = kwargs.get("name_carpet", "dfs")
        PATH_ITP = kwargs.get("path_itp", "NULL")
        
        PATH_DFS = os.path.join(PATH_GRL0, NAME_CARPET)
        herr.wrapper_create_dirs([PATH_DFS])
        
        PATH_DF_ATOMS = os.path.join(PATH_DFS, 'atoms.pkl')
        dic_atoms = {}
        dic_atoms['nr'] = {}
        dic_atoms['type'] = {}
        dic_atoms['resnr'] = {}
        dic_atoms['resid'] = {}
        dic_atoms['atom'] = {}
        dic_atoms['cgnr'] = {}
        dic_atoms['charge'] = {}
        dic_atoms['mass'] = {}

        PATH_DF_BONDS = os.path.join(PATH_DFS, 'bonds.pkl')
        dic_bonds = {}
        dic_bonds['ai'] = {}
        dic_bonds['aj'] = {}
        dic_bonds['funct'] = {}
        dic_bonds['c0'] = {}
        dic_bonds['c1'] = {}

        PATH_DF_PAIRS = os.path.join(PATH_DFS, 'pairs.pkl')
        dic_pairs = {}
        dic_pairs['ai'] = {}
        dic_pairs['aj'] = {}
        dic_pairs['funct'] = {}

        PATH_DF_ANGLES = os.path.join(PATH_DFS, 'angles.pkl')
        dic_angles = {}
        dic_angles['ai'] = {}
        dic_angles['aj'] = {}
        dic_angles['ak'] = {}
        dic_angles['funct'] = {}
        dic_angles['angle'] = {}
        dic_angles['fc'] = {}

        PATH_DF_DIHEDRALS = os.path.join(PATH_DFS, 'dihedrals.pkl')
        dic_dihedrals = {}
        dic_dihedrals['ai'] = {}
        dic_dihedrals['aj'] = {}
        dic_dihedrals['ak'] = {}
        dic_dihedrals['al'] = {}
        dic_dihedrals['funct'] = {}
        dic_dihedrals['ph0'] = {}
        dic_dihedrals['cp'] = {}
        dic_dihedrals['mult'] = {}

        PATH_DF_DIHEDRALS_IMP = os.path.join(PATH_DFS, 'dihedrals_imp.pkl')
        dic_dihedrals_imp = {}
        dic_dihedrals_imp['ai'] = {}
        dic_dihedrals_imp['aj'] = {}
        dic_dihedrals_imp['ak'] = {}
        dic_dihedrals_imp['al'] = {}
        dic_dihedrals_imp['funct'] = {}
        dic_dihedrals_imp['angle'] = {}
        dic_dihedrals_imp['fc'] = {}

        f = open(PATH_ITP, 'r')
        flag_next_line = True
        while(flag_next_line):

            line = f.readline()

            if not line:
                flag_next_line = False
                break

            atom_counter = 0
            if '[ atoms ]' in line:
                for line2 in f:
                    sf = line2.split()
                    if sf[0] == ';':
                        continue
                    if (len(sf) != 8) or ('[' in sf):
                        line = line2
                        break

                    dic_atoms['nr'][atom_counter] = int(sf[0]) # 1, 2, ..
                    dic_atoms['type'][atom_counter] = str(sf[1]) # 'CH0', 'CH1'
                    dic_atoms['resnr'][atom_counter] = int(sf[2]) # 1, 2, ..
                    dic_atoms['resid'][atom_counter] = str(sf[3]) # G006
                    dic_atoms['atom'][atom_counter] = str(sf[4]) # C1, C2, ...
                    dic_atoms['cgnr'][atom_counter] = int(sf[5]) # 1, 2, ...
                    dic_atoms['charge'][atom_counter] = float(sf[6]) # -0.014, 0.016
                    dic_atoms['mass'][atom_counter] = float(sf[7]) # 15.0350, 14.0270

                    atom_counter+=1

            bond_counter = 0
            if '[ bonds ]' in line:
                for line2 in f:
                    sf = line2.split()
                    if sf[0] == ';':
                        continue
                    if (len(sf) != 5) or ('[' in sf):
                        line = line2
                        break

                    dic_bonds['ai'][bond_counter] = int(sf[0])
                    dic_bonds['aj'][bond_counter] = int(sf[1])
                    dic_bonds['funct'][bond_counter] = int(sf[2])
                    dic_bonds['c0'][bond_counter] = float(sf[3])
                    dic_bonds['c1'][bond_counter] = float(sf[4])

                    bond_counter+=1


            pair_counter = 0
            if '[ pairs ]' in line:
                for line2 in f:
                    sf = line2.split()
                    if sf[0] == ';':
                        continue
                    if (len(sf) != 3) or ('[' in sf):
                        line = line2
                        break

                    dic_pairs['ai'][pair_counter] = int(sf[0])
                    dic_pairs['aj'][pair_counter] = int(sf[1])
                    dic_pairs['funct'][pair_counter] = int(sf[2])
                    pair_counter+=1                     


            angle_counter = 0
            if '[ angles ]' in line:
                for line2 in f:
                    sf = line2.split()
                    if sf[0] == ';':
                        continue
                    if (len(sf) != 6) or ('[' in sf):
                        line = line2
                        break

                    dic_angles['ai'][angle_counter] = int(sf[0])
                    dic_angles['aj'][angle_counter] = int(sf[1])
                    dic_angles['ak'][angle_counter] = int(sf[2])
                    dic_angles['funct'][angle_counter] = int(sf[3])
                    dic_angles['angle'][angle_counter] = float(sf[4])
                    dic_angles['fc'][angle_counter] = float(sf[5])

                    angle_counter+=1           


            dihedral_counter = 0
            if '[ dihedrals ]' in line:
                for line2 in f:
                    sf = line2.split()
                    if sf[0] == ';':
                        continue
                    if (len(sf) != 7) or ('[' in sf):
                        line = line2
                        break

                    # ;  ai   aj   ak   al  funct   angle     fc                
                    dic_dihedrals_imp['ai'][dihedral_counter] = int(sf[0])
                    dic_dihedrals_imp['aj'][dihedral_counter] = int(sf[1])
                    dic_dihedrals_imp['ak'][dihedral_counter] = int(sf[2])
                    dic_dihedrals_imp['al'][dihedral_counter] = int(sf[3])
                    dic_dihedrals_imp['funct'][dihedral_counter] = int(sf[4])
                    dic_dihedrals_imp['angle'][dihedral_counter] = float(sf[5])
                    dic_dihedrals_imp['fc'][dihedral_counter] = float(sf[6])

                    dihedral_counter+=1      

            dihedral_counter = 0
            if '[ dihedrals ]' in line:
                for line2 in f:
                    sf = line2.split()
                    if sf[0] == ';':
                        continue
                    if (len(sf) != 8) or ('[' in sf):
                        line = line2
                        break

                    dic_dihedrals['ai'][dihedral_counter] = int(sf[0])
                    dic_dihedrals['aj'][dihedral_counter] = int(sf[1])
                    dic_dihedrals['ak'][dihedral_counter] = int(sf[2])
                    dic_dihedrals['al'][dihedral_counter] = int(sf[3])
                    dic_dihedrals['funct'][dihedral_counter] = int(sf[4])
                    dic_dihedrals['ph0'][dihedral_counter] = float(sf[5])
                    dic_dihedrals['cp'][dihedral_counter] = float(sf[6])
                    dic_dihedrals['mult'][dihedral_counter] = int(sf[7])

                    dihedral_counter+=1   


        PATH_DF_ATOMS = os.path.join(PATH_DFS, 'atoms.pkl')
        pd.DataFrame(dic_atoms).to_pickle(PATH_DF_ATOMS)

        PATH_DF_BONDS = os.path.join(PATH_DFS, 'bonds.pkl')
        pd.DataFrame(dic_bonds).to_pickle(PATH_DF_BONDS)

        PATH_DF_PAIRS = os.path.join(PATH_DFS, 'pairs.pkl')
        pd.DataFrame(dic_pairs).to_pickle(PATH_DF_PAIRS)

        PATH_DF_ANGLES = os.path.join(PATH_DFS, 'angles.pkl')
        pd.DataFrame(dic_angles).to_pickle(PATH_DF_ANGLES)

        PATH_DF_DIHEDRALS = os.path.join(PATH_DFS, 'dihedrals.pkl')
        pd.DataFrame(dic_dihedrals).to_pickle(PATH_DF_DIHEDRALS)

        PATH_DF_DIHEDRALS_IMP = os.path.join(PATH_DFS, 'dihedrals_imp.pkl')
        pd.DataFrame(dic_dihedrals_imp).to_pickle(PATH_DF_DIHEDRALS_IMP)

        f.close()
        
        dic = {}
        dic['PATH_DF_ATOMS'] = PATH_DF_ATOMS
        dic['PATH_DF_BONDS'] = PATH_DF_BONDS
        dic['PATH_DF_PAIRS'] = PATH_DF_PAIRS
        dic['PATH_DF_ANGLES'] = PATH_DF_ANGLES
        dic['PATH_DF_DIHEDRALS'] = PATH_DF_DIHEDRALS
        dic['PATH_DF_DIHEDRALS_IMP'] = PATH_DF_DIHEDRALS_IMP
        dic['PATH_DFS'] = PATH_DFS
        
        return dic
        
        
    def gen_itp_from_dfs(self, **kwargs):
        
        n_merge = kwargs.get("n_merge", "NULL")
        
        PATH_DF_ATOMS = kwargs.get('path_df_atoms', 'NULL')
        PATH_DF_BONDS = kwargs.get('path_df_bonds', 'NULL')
        PATH_DF_FBONDS = kwargs.get('path_df_fbonds', 'NULL')
        PATH_DF_PAIRS = kwargs.get('path_df_pairs', 'NULL')
        PATH_DF_ANGLES = kwargs.get('path_df_angles', 'NULL')
        PATH_DF_DIHEDRALS = kwargs.get('path_df_dihedrals', 'NULL')
        PATH_DF_DIHEDRALS_IMP = kwargs.get('path_df_dihedrals_imp', 'NULL')
        PATH_OUTPUT = kwargs.get('path_output', 'NULL')
        LABEL = kwargs.get('label', 'NULL')
        
        df_atoms = pd.read_pickle(PATH_DF_ATOMS)
        df_bonds = pd.read_pickle(PATH_DF_BONDS)
        df_fbonds = pd.read_pickle(PATH_DF_FBONDS)
        df_pairs = pd.read_pickle(PATH_DF_PAIRS)
        df_angles = pd.read_pickle(PATH_DF_ANGLES)
        df_dihedrals = pd.read_pickle(PATH_DF_DIHEDRALS)
        df_dihedrals_imp = pd.read_pickle(PATH_DF_DIHEDRALS_IMP)
        label = LABEL
        
        df_map = df_atoms.copy()
        df_map = df_map.set_index('nr')
        f = open(PATH_OUTPUT, 'w')
        
        #####################################
        ####   HEADER 1
        f.write('[ moleculetype ]\n')
        f.write('; Name   nrexcl\n')
        f.write('    {}     3\n\n'.format(label))
        
        #####################################
        ####   ATOMS
        
        f.write(' [ atoms ]\n')
        # ['nr', 'type', 'resnr', 'resid', 'atom', 'cgnr', 'charge', 'mass']    
        #     1    HC    1    UDD    H65    1    0.078   1.0080
        f.write(';      nr      type     resnr   resid    atom       cgnr  charge    mass\n')
        
        for i in range(n_merge):
            
            for idx in df_atoms.index:

                nr = df_atoms['nr'].loc[idx]
                typ = df_atoms['type'].loc[idx]
                resnr = df_atoms['resnr'].loc[idx]
                resid = df_atoms['resid'].loc[idx]
                atom = df_atoms['atom'].loc[idx]
                cgnr = df_atoms['cgnr'].loc[idx]
                charge = df_atoms['charge'].loc[idx]
                mass = df_atoms['mass'].loc[idx]
                
                nr = int(nr) + i*65
                cgnr = cgnr + i*65
                
                #           1    HC    1   UDD H65    1    0.078   1.0080        
                f.write("{:>9d}{:>9}{:>9d}{:>9}{:>9}{:>9d}{:>9.4f}{:>9.4f}\n".format(nr, typ, resnr, resid,
                                                                               atom, cgnr, charge, mass))
                                                        
            
            
           
        #####################################
        ####   BONDS
        f.write('[ bonds ]\n')
        f.write(';    ai     aj  funct   c0         c1\n')
                #      C5     C4    2   0.1530   7.1500e+06
            
        for i in range(n_merge):
            for idx in df_bonds.index:

                ai = df_bonds['ai'].loc[idx]
                aj = df_bonds['aj'].loc[idx]
                
                ai = ai + i*65
                aj = aj + i*65

                funct = df_bonds['funct'].loc[idx]

                c0 = df_bonds['c0'].loc[idx]
                c1 = df_bonds['c1'].loc[idx]

                f.write("{:>7}{:>7}{:>5d}{:>9.4f}{:13.4e}\n".format(ai, aj, funct, c0, c1))
                
                
        #####################################
        ####  fusion BONDS

        for idx in df_fbonds.index:

            ai = df_fbonds['ai'].loc[idx]
            aj = df_fbonds['aj'].loc[idx]

            ai = ai  
            aj = aj 
            
            funct = df_fbonds['funct'].loc[idx]

            c0 = df_fbonds['c0'].loc[idx]
            c1 = df_fbonds['c1'].loc[idx]

            f.write("{:>7}{:>7}{:>5d}{:>9.4f}{:13.4e}\n".format(ai, aj, funct, c0, c1))                
                
        
            
        #####################################
        ####   PAIRS
        f.write('[ pairs ]\n')
        f.write(';    ai     aj  funct\n')
                #     C5     C2    1
        for i in range(n_merge):
            for idx in df_pairs.index:

                ai = df_pairs['ai'].loc[idx]
                ai = ai + i*65

                aj = df_pairs['aj'].loc[idx]
                aj = aj + i*65

                funct = df_pairs['funct'].loc[idx]

                f.write("{:>7}{:>7}{:>5d}\n".format(ai, aj, funct))

            
        #####################################
        ####   ANGLES
        f.write('[ angles ]\n')
        f.write(';    ai     aj     ak  funct   angle     fc\n')
                #     C5     C4     C3    2    111.00   530.00
            
        for i in range(n_merge):
            for idx in df_angles.index:

                ai = df_angles['ai'].loc[idx]
                aj = df_angles['aj'].loc[idx]
                ak = df_angles['ak'].loc[idx]

                ai = ai + i*65
                aj = aj + i*65
                ak = ak + i*65


                funct = df_angles['funct'].loc[idx]
                angle = df_angles['angle'].loc[idx]
                fc = df_angles['fc'].loc[idx]

                f.write("{:>7}{:>7}{:>7}{:>5d}{:>10.2f}{:>9.2f}\n".format(ai, aj, ak, funct,
                                                                angle, fc))     
            
            
        #####################################
        ####    DIHEDRALS
        f.write('[ dihedrals ]\n')
        # ;  ai   aj   ak   al  funct   angle     fc                
        f.write(';  ai   aj   ak   al  funct   angle     fc\n')
        for i in range(n_merge):
            for idx in df_dihedrals_imp.index:

                ai = df_dihedrals_imp['ai'].loc[idx]
                aj = df_dihedrals_imp['aj'].loc[idx]
                ak = df_dihedrals_imp['ak'].loc[idx]
                al = df_dihedrals_imp['al'].loc[idx]

                ai = ai + i*65
                aj = aj + i*65
                ak = ak + i*65  
                al = al + i*65  

                funct = df_dihedrals_imp['funct'].loc[idx]
                angle = df_dihedrals_imp['angle'].loc[idx]
                fc = df_dihedrals_imp['fc'].loc[idx]

                f.write("{:>7}{:>7}{:>7}{:>7}{:>5d}{:>12.4f}{:>11.4f}\n".format(ai, aj, ak, al,
                                                                funct, angle, fc))     

        
        f.write('[ dihedrals ]\n')
        f.write(';    ai     aj     ak     al  funct    ph0      cp     mult\n')
                #     C5     C4     C3     C2    1      0.00     5.92    3
            
        for i in range(n_merge):
            for idx in df_dihedrals.index:

                ai = df_dihedrals['ai'].loc[idx]
                aj = df_dihedrals['aj'].loc[idx]
                ak = df_dihedrals['ak'].loc[idx]
                al = df_dihedrals['al'].loc[idx]

                ai = ai + i*65
                aj = aj + i*65
                ak = ak + i*65  
                al = al + i*65  

                funct = df_dihedrals['funct'].loc[idx]
                ph0 = df_dihedrals['ph0'].loc[idx]
                cp = df_dihedrals['cp'].loc[idx]
                mult = df_dihedrals['mult'].loc[idx]

                f.write("{:>7}{:>7}{:>7}{:>7}{:>5d}{:>10.2f}{:>9.2f}{:>5d}\n".format(ai, aj, ak, al,
                                                                funct, ph0, cp, mult))     

    
        f.write("\n")        
        f.close()
        
        return


    def get_ffnonbonded_agua(self, **kwargs):

#         PATH_GROMOS54A7_ATB = "../data/general/forcefields/ffnonbonded_gromos54a7_atb_original.itp"
        # PATH_HOH_RM = kwargs.get("path_agua_itp", "NULL")
        path_agua_itp = kwargs.get("path_agua_itp", "NULL")

        USER = getpass.getuser()
        user = kwargs.get('user', USER) # <==

        NAME_DIN = kwargs.get("name_din", "PruebaX") # <==
        CARPET = kwargs.get("carpet", "carpeta")

        PATH_GRL0 = "/home/{}/Documents/aguas_xxx".format(user)
        PATH_GRL0 = kwargs.get("path_grl0", PATH_GRL0) # <==

        PATH_GRL1 = os.path.join(PATH_GRL0, NAME_DIN)
        PATH_GRL2 = os.path.join(PATH_GRL1, CARPET)
        PATH_GRL2 = os.path.join(PATH_GRL2, "forcefield")

        NAME_FFNB = "ffnonbonded_" + NAME_DIN + ".itp"
        PATH_FFNB_RM = os.path.join(PATH_GRL2, NAME_FFNB)
        PATH_FFNB_RM = kwargs.get("path_out", PATH_FFNB_RM)

        paths_to_create = [PATH_GRL0, PATH_GRL1, PATH_GRL2]
        for path in paths_to_create:
            cmd = ['mkdir', '-p', path]
            cmd = [str(item) for item in cmd]
            process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)

        path_gromos54a7_atb = kwargs.get("path_gromos54a7_atb", self.PATH_GROMOS54A7_ATB)

        # atypes de spce

        df = self.get_binfo_spc_54a7(path_top=path_agua_itp)["[ atoms ]"]
        at_spce = df["type"].unique()

        # juntando a todos
    #     rm_atypes = np.concatenate((at_aot, at_g016, at_spce, at_na)).astype(str)
        rm_atypes = np.array(at_spce).astype(str)
        comb = combinations(rm_atypes, 2) 
        comb_atypes = [(i[0], i[1]) for i in list(comb)]

        self_comb = [(mol, mol) for mol in rm_atypes]
        all_comb_atypes = comb_atypes.copy()
        all_comb_atypes.extend(self_comb)

        # query de. ffnbounded 54a7 atb
        df_54a7_at = self.get_nbinfo_gromos54a7_atb(path_top=path_gromos54a7_atb)['[ atomtypes ]']
        df_54a7_nb = self.get_nbinfo_gromos54a7_atb(path_top=path_gromos54a7_atb)['[ nonbond_params ]']
        df_54a7_pt = self.get_nbinfo_gromos54a7_atb(path_top=path_gromos54a7_atb)['[ pairtypes ]']


        ## EXTRAYENDO ATYPES

        df_at_rm = df_54a7_at.loc[df_54a7_at['name'].isin(rm_atypes)]

        ## EXTRAYENDO NON BOUNDED PARAMS

    # el anteriro era para no_rm
    # no tomaba en cuenta los non bounded de isooctano
    # A + B

    #                  A
    #     comb_atypes_nog016 = []
    #     for ti in comb_atypes:
    #         flag_array = []
    #         for tj in comb_g016:
    #             i = frozenset(ti)
    #             j = frozenset(tj)
    #             if i == j:
    #                 flag_array.append(False)
    #             else:
    #                 flag_array.append(True)

    #         if np.all(flag_array):
    #             comb_atypes_nog016.append(ti)

    #                   B
        idxs_nb = []
        for idx in df_54a7_nb.index:
            flag_array = []

            t1 = df_54a7_nb['i'].loc[idx]
            t2 = df_54a7_nb['j'].loc[idx]
            ti = (t1, t2)

            for tj in comb_atypes:
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

        # ESCRIBIENDO ARCHIVO FFNONBOUNDED
        f = open(PATH_FFNB_RM, 'w')

        # Escribiendo '[ atomtypes ]'
        f.write('[ atomtypes ]\n')
        f.write('; name  at.num   mass      charge  ptype                c6                      c12\n')

        for idx in df_at_rm.index:

            name = df_at_rm['name'].loc[idx]
            atnum = int(df_at_rm['at.num'].loc[idx])
            mass = np.float(df_at_rm['mass'].loc[idx])
            charge = np.float(df_at_rm['charge'].loc[idx])
            ptype = df_at_rm['ptype'].loc[idx]
            c6 = np.float(df_at_rm['c6'].loc[idx])
            c12 = np.float(df_at_rm['c12'].loc[idx])

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
            func = np.int(df_nb_rm['func'].loc[idx])
            c6 = np.float(df_nb_rm['c6'].loc[idx])
            c12 = np.float(df_nb_rm['c12'].loc[idx])

            f.write("{:>9}{:>9}{:>6d}{:>14.10f}{:>15.7e}\n".format(i, j, func, c6, c12))

        # Escribiendo '[ pairtypes ]'
        # ;	i	j	func	c6	c12
        f.write("\n")
        f.write('[ pairtypes ]\n')
        f.write(';       i        j   func       c6           c12\n')

        for idx in df_pt_rm.index:

            i = df_pt_rm['i'].loc[idx]
            j = df_pt_rm['j'].loc[idx]
            func = np.int(df_pt_rm['func'].loc[idx])
            c6 = np.float(df_pt_rm['c6'].loc[idx])
            c12 = np.float(df_pt_rm['c12'].loc[idx])

            f.write("{:>9}{:>9}{:>6d}{:>14.10f}{:>15.7e}\n".format(i, j, func, c6, c12))

        f.close()

        return PATH_FFNB_RM


    def wrapper_create_topol_agua(self, **kwargs):

        PATH_GRL1 = kwargs.get("path_grl1", "NULL") 
        CARPET = kwargs.get("carpet", "NULL")

        # PATH_RMNOMEDC = kwargs.get("path_rmnomedc", "NULL")
        PATH_CELDA0 = kwargs.get("path_celda0", "NULL")

        # PATH_FFNB_RM = kwargs.get("path_ffnb_rm", "NULL")
        PATH_FFNB = kwargs.get("path_ffnb", "NULL")

        NAME_DIN = kwargs.get("name_din", "NULL")

        # path_ffb_in_h2o = kwargs.get("path_ffb_in_hoh", self.PATH_HOH_RM)
        path_agua_itp = kwargs.get("path_agua_itp", "NULL")
        
        PATH_CARPET = os.path.join(PATH_GRL1, CARPET)
        PATH_FOLDER_FF = os.path.join(PATH_CARPET, "forcefield")

        name_b_h2o = "ffbounded_" + NAME_DIN + ".itp"

        path_b_h2o = os.path.join(PATH_FOLDER_FF, name_b_h2o)

        # _ = [path_b_g016, path_b_aot, path_b_h2o, path_b_na]
        _ = [path_b_h2o]
        paths_ffb = [os.path.split(path)[1] for path in _]

        self.get_ffbonded_h2o(path_ffb_in=path_agua_itp, path_ffb_out=path_b_h2o)

        PATH_FF = self.create_ff(path_folder_ff=PATH_FOLDER_FF,
                            name_din=NAME_DIN,
                            paths_ffnb=[os.path.split(PATH_FFNB)[1]],
                            paths_ffb=paths_ffb,
                            nfunc=1, comb_rule=1, gen_pairs='yes', fudLJ=1.0, fudgeQQ=1.0)

        PATH_FF = "./forcefield/" + os.path.split(PATH_FF)[-1]

        gro_celda0 = groFile(PATH_CELDA0)
        PATH_TOPOL = os.path.join(PATH_CARPET, "topol.top")
        self.create_topol(gro_celda0 = gro_celda0,
                          name_ciclo=NAME_DIN,
                          path_ff=PATH_FF,
                          path_topol=PATH_TOPOL)


        return PATH_TOPOL


    def top_to_cop_agua(self, **kwargs):

        PATH_CARPET_IN = kwargs.get("path_carpet_in", "NULL")
        PATH_CARPET_OUT = kwargs.get("path_carpet_out", "NULL")
        NAME_DIN = kwargs.get("name_din", "NULL")
        
        PATH_CARPET_IN_FF = os.path.join(PATH_CARPET_IN, "forcefield")
        PATH_CARPET_OUT_FF = os.path.join(PATH_CARPET_OUT, "forcefield")

        cmd = ['mkdir', '-p', PATH_CARPET_OUT_FF]
        cmd = [str(item) for item in cmd]
        process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)

        NAME_FFF = "forcefield_" + NAME_DIN + ".itp"
        NAME_FF_H2O = "ffbounded_" + NAME_DIN + ".itp"
        NAME_FFNB = "ffnonbonded_" + NAME_DIN + ".itp"
        NAME_TOPOL = "topol.top"

        NAME_TOPOL = kwargs.get("name_topol", NAME_TOPOL)
        NAME_FFF = kwargs.get("name_fff", NAME_FFF)
        NAME_FF_H2O = kwargs.get("name_ff_h2o", NAME_FF_H2O)
        NAME_FFNB = kwargs.get("name_ffnb", NAME_FFNB)

        PATH_TOPOL_IN = os.path.join(PATH_CARPET_IN, NAME_TOPOL)
        PATH_TOPOL_OUT = os.path.join(PATH_CARPET_OUT, NAME_TOPOL)
        
        PATH_FFF_IN = os.path.join(PATH_CARPET_IN_FF, NAME_FFF)
        PATH_FF_H2O_IN = os.path.join(PATH_CARPET_IN_FF, NAME_FF_H2O)
        PATH_FFNB_IN = os.path.join(PATH_CARPET_IN_FF, NAME_FFNB)

        PATH_FFF_OUT = os.path.join(PATH_CARPET_OUT_FF, NAME_FFF)
        PATH_FF_H2O_OUT = os.path.join(PATH_CARPET_OUT_FF, NAME_FF_H2O)
        PATH_FFNB_OUT = os.path.join(PATH_CARPET_OUT_FF, NAME_FFNB)

        PATH_TOPOL_IN = kwargs.get("path_topol_in", PATH_TOPOL_IN)
        PATH_FFF_IN =  kwargs.get("path_fff_in", PATH_FFF_IN)
        PATH_FF_H2O_IN = kwargs.get("path_ff_h2o_in", PATH_FF_H2O_IN)
        
        PATH_TOPOL_OUT = kwargs.get("path_topol_out", PATH_TOPOL_OUT)
        PATH_FFF_OUT =  kwargs.get("path_fff_out", PATH_FFF_OUT)
        PATH_FF_H2O_OUT = kwargs.get("path_ff_h2o_out", PATH_FF_H2O_OUT)
        
        PATHS_IN = [PATH_TOPOL_IN,
        PATH_FFF_IN,
        PATH_FF_H2O_IN, 
        PATH_FFNB_IN]

        PATHS_OUT = [PATH_TOPOL_OUT,
        PATH_FFF_OUT,
        PATH_FF_H2O_OUT, 
        PATH_FFNB_OUT]

        for path_in, path_out in zip(PATHS_IN, PATHS_OUT):
            cmd = ['cp', path_in, path_out]
            cmd = [str(item) for item in cmd]
            process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)
            
        return PATH_TOPOL_OUT



    def get_ffnb_contaminantes(self, **kwargs):
        
        USER = getpass.getuser()
        user = kwargs.get('user', USER) # <==

        NAME_DIN = kwargs.get("name_din", "PruebaX") # <==
        CARPET = kwargs.get("carpet", "carpeta")

        PATH_GRL0 = "/home/{}/Documents/rm_radios_varios".format(user)
        PATH_GRL0 = kwargs.get("path_grl0", PATH_GRL0) # <==
        
        PATH_GRL1 = os.path.join(PATH_GRL0, NAME_DIN)
        PATH_GRL2 = os.path.join(PATH_GRL1, CARPET)
        PATH_GRL2 = os.path.join(PATH_GRL2, "forcefield")

        NAME_FFNB = "ffnb_" + NAME_DIN + ".itp"
        PATH_FFNB_RM = os.path.join(PATH_GRL2, NAME_FFNB)
        PATH_FFNB_RM = kwargs.get("path_out", PATH_FFNB_RM)
        
        paths_to_create = [PATH_GRL0, PATH_GRL1, PATH_GRL2]
        for path in paths_to_create:
            cmd = ['mkdir', '-p', path]
            cmd = [str(item) for item in cmd]
            process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)
            
        path_ffb_in_g016 = kwargs.get("path_ffb_in_g016", self.PATH_ISO_RM)
        path_ffb_in_aot = kwargs.get("path_ffb_in_aot", self.PATH_AOT_RM)
        path_ffb_in_h2o = kwargs.get("path_ffb_in_h2o", "NULL")
        path_ffb_in_na = kwargs.get("path_ffb_in_na", self.PATH_NA_RM)            
        path_ffb_in_conta = kwargs.get("path_ffb_in_conta", "NULL")            
        path_gromos54a7_atb = kwargs.get("path_gromos54a7_atb", self.PATH_GROMOS54A7_ATB)

        lines_to_data_conta = kwargs.get("lines_to_data_conta", 1)
        num_atoms_conta = kwargs.get("num_atoms_conta", 6)

        # atomtypes de aot
        df = self.get_binfo_aot(path_top=path_ffb_in_aot)["[ atoms ]"]
        at_aot = df["type"].unique()

        # atypes de g016
        df = self.get_binfo_g016(path_top=path_ffb_in_g016)["[ atoms ]"]
        at_g016 = df["type"].unique()
        comb = combinations(at_g016, 2)
        comb_g016 = [(i[0], i[1]) for i in list(comb)]

        # atypes de spce
#         df = self.get_binfo_spce(path_top=path_ffb_in_h2o)["[ atoms ]"]
        df = self.get_binfo_spc_54a7(path_top=path_ffb_in_h2o)["[ atoms ]"]
        at_spce = df["type"].unique()

        # atypes de na
        df = self.get_binfo_na(path_top=path_ffb_in_na)["[ atoms ]"]
        at_na = df["type"].unique()

        # atypes de contaminante
        df = self.get_binfo_conta(path_top=path_ffb_in_conta,
                                  num_atoms=num_atoms_conta,
                                  lines_to_data=lines_to_data_conta)["[ atoms ]"]
        at_conta = df["type"].unique()

        # juntando a todos
        rm_atypes = np.concatenate((at_aot, at_g016, at_spce, at_na, at_conta)).astype(str)
        comb = combinations(rm_atypes, 2) 
        comb_atypes = [(i[0], i[1]) for i in list(comb)]

        self_comb = [(mol, mol) for mol in rm_atypes]
        all_comb_atypes = comb_atypes.copy()
        all_comb_atypes.extend(self_comb)

        # query de ffnbounded 54a7 atb
        df_54a7_at = self.get_nbinfo_gromos54a7_atb(path_top=path_gromos54a7_atb)['[ atomtypes ]']
        df_54a7_nb = self.get_nbinfo_gromos54a7_atb(path_top=path_gromos54a7_atb)['[ nonbond_params ]']
        df_54a7_pt = self.get_nbinfo_gromos54a7_atb(path_top=path_gromos54a7_atb)['[ pairtypes ]']


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
        df_54a7_nb.to_pickle("verA.pkl")
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

        pd.DataFrame(idxs_nb).to_pickle("verB.pkl")
        idxs_nb = list(set(idxs_nb))
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

        idxs_pt = list(set(idxs_pt))
        df_pt_rm = df_54a7_pt.loc[idxs_pt]

        # Modificando g016 atypes parametros
        epsilon_factor = kwargs.get("epsilon_factor", 1.0) # <==
        sigma_factor = kwargs.get("sigma_factor", 1.0)
        df_mod_g016 = self.gen_nonbonded_G016_2(epsilon_factor=epsilon_factor,
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
            mass = np.float(df_at_rm['mass'].loc[idx])
            charge = np.float(df_at_rm['charge'].loc[idx])
            ptype = df_at_rm['ptype'].loc[idx]
            c6 = np.float(df_at_rm['c6'].loc[idx])
            c12 = np.float(df_at_rm['c12'].loc[idx])

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
            df_nb_rm.to_excel("ver.xlsx")
            df_nb_rm.to_pickle("ver.pkl")
            func = np.int(df_nb_rm['func'].loc[idx])
            c6 = np.float(df_nb_rm['c6'].loc[idx])
            c12 = np.float(df_nb_rm['c12'].loc[idx])

            f.write("{:>9}{:>9}{:>6d}{:>14.10f}{:>15.7e}\n".format(i, j, func, c6, c12))

        # Escribiendo '[ pairtypes ]'
        # ;	i	j	func	c6	c12
        f.write("\n")
        f.write('[ pairtypes ]\n')
        f.write(';       i        j   func       c6           c12\n')

        for idx in df_pt_rm.index:

            i = df_pt_rm['i'].loc[idx]
            j = df_pt_rm['j'].loc[idx]
            func = np.int(df_pt_rm['func'].loc[idx])
            c6 = np.float(df_pt_rm['c6'].loc[idx])
            c12 = np.float(df_pt_rm['c12'].loc[idx])

            f.write("{:>9}{:>9}{:>6d}{:>14.10f}{:>15.7e}\n".format(i, j, func, c6, c12))

        f.close()
        
        return PATH_FFNB_RM



    def wrapper_create_topol_contaminantes(self, **kwargs):

        PATH_GRL1 = kwargs.get("path_grl1", "NULL")
        CARPET = kwargs.get("carpet", "NULL")
        PATH_RMNOMEDC = kwargs.get("path_rmnomedc", "NULL")
        PATH_FFNB_RM = kwargs.get("path_ffnb_rm", "NULL")
        NAME_DIN = kwargs.get("name_din", "NULL")

        path_ffb_in_g016 = kwargs.get("path_ffb_in_g016", self.PATH_ISO_RM)
        path_ffb_in_aot = kwargs.get("path_ffb_in_aot", self.PATH_AOT_RM)
        path_ffb_in_h2o = kwargs.get("path_ffb_in_hoh", self.PATH_HOH_RM)
        path_ffb_in_na = kwargs.get("path_ffb_in_na", self.PATH_NA_RM)
        path_ffb_in_conta = kwargs.get("path_ffb_in_conta", "NULL")
        
        PATH_CARPET = os.path.join(PATH_GRL1, CARPET)
        PATH_FOLDER_FF = os.path.join(PATH_CARPET, "forcefield")

        path_b_g016 = os.path.join(PATH_FOLDER_FF, "ffbounded_g016.itp")
        path_b_aot = os.path.join(PATH_FOLDER_FF, "ffbounded_aot.itp")
        path_b_h2o = os.path.join(PATH_FOLDER_FF, "ffbounded_h2o.itp")
        path_b_na = os.path.join(PATH_FOLDER_FF, "ffbounded_na.itp")
        path_b_conta = os.path.join(PATH_FOLDER_FF, "ffbounded_conta.itp")

        _ = [path_b_g016, path_b_aot, path_b_h2o, path_b_na, path_b_conta]
        paths_ffb = [os.path.split(path)[1] for path in _]

        self.get_ffbonded_g016(path_ffb_in=path_ffb_in_g016, path_ffb_out=path_b_g016)
        self.get_ffbonded_aot(path_ffb_in=path_ffb_in_aot, path_ffb_out=path_b_aot)
        self.get_ffbonded_h2o(path_ffb_in=path_ffb_in_h2o, path_ffb_out=path_b_h2o)
        self.get_ffbonded_na(path_ffb_in=path_ffb_in_na, path_ffb_out=path_b_na)
        self.get_ffbonded_conta(path_ffb_in=path_ffb_in_conta, path_ffb_out=path_b_conta)

        PATH_FF = self.create_ff(path_folder_ff=PATH_FOLDER_FF,
                            name_din=NAME_DIN,
                            paths_ffnb=[os.path.split(PATH_FFNB_RM)[1]],
                            paths_ffb=paths_ffb,
                            nfunc=1, comb_rule=1, gen_pairs='yes', fudLJ=1.0, fudgeQQ=1.0)

        PATH_FF = "./forcefield/" + os.path.split(PATH_FF)[-1]

        gro_celda0 = groFile(PATH_RMNOMEDC)
        PATH_TOPOL = os.path.join(PATH_CARPET, "topol.top")
        self.create_topol(gro_celda0 = gro_celda0,
                          name_ciclo=NAME_DIN,
                          path_ff=PATH_FF,
                          path_topol=PATH_TOPOL)


        return PATH_TOPOL

 
    def get_ffnb_g016_atypes(self, **kwargs):

        NAME_DIN = kwargs.get("name_din", "NULL")

        PATH_GRL1 = kwargs.get("path_grl1", "NULL")
        PATH_GRL2 = os.path.join(PATH_GRL1, "forcefield")
        

        NAME_FFNB = "ffnb_" + NAME_DIN + ".itp"
        PATH_FFNB_RM = os.path.join(PATH_GRL2, NAME_FFNB)
        PATH_FFNB_RM = kwargs.get("path_out", PATH_FFNB_RM)
        
        paths_to_create = [PATH_GRL1, PATH_GRL2]
        for path in paths_to_create:
            cmd = ['mkdir', '-p', path]
            cmd = [str(item) for item in cmd]
            process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)
            
        path_ffb_in_g016 = kwargs.get("path_ffb_in_g016", self.PATH_ISO_RM)
        path_gromos54a7_atb = kwargs.get("path_gromos54a7_atb", self.PATH_GROMOS54A7_ATB)

        # atypes de g016
        df = self.get_binfo_g016(path_top=path_ffb_in_g016)["[ atoms ]"]
        at_g016 = df["type"].unique()
        comb = combinations(at_g016, 2)
        comb_g016 = [(i[0], i[1]) for i in list(comb)]

        # juntando a todos
#         rm_atypes = np.concatenate((at_aot, at_g016, at_spce, at_na)).astype(str)
        rm_atypes = at_g016.astype(str)
        comb = combinations(rm_atypes, 2) 
        comb_atypes = [(i[0], i[1]) for i in list(comb)]

        self_comb = [(mol, mol) for mol in rm_atypes]
        all_comb_atypes = comb_atypes.copy()
        all_comb_atypes.extend(self_comb)

        # query de ffnbounded 54a7 atb
        df_54a7_at = self.get_nbinfo_gromos54a7_atb(path_top=path_gromos54a7_atb)['[ atomtypes ]']
        df_54a7_nb = self.get_nbinfo_gromos54a7_atb(path_top=path_gromos54a7_atb)['[ nonbond_params ]']
        df_54a7_pt = self.get_nbinfo_gromos54a7_atb(path_top=path_gromos54a7_atb)['[ pairtypes ]']

        ## EXTRAYENDO ATYPES
        df_at_rm = df_54a7_at.loc[df_54a7_at['name'].isin(rm_atypes)]

        ## EXTRAYENDO NON BOUNDED PARAMS
        
#        # cheka para cada par, si el par
#        # ti = (a, b) o (b, a) pertenece a
#        # comb_g016, si pertenece lo descarta,
#        # si no pertenece lo agrega a comb_atypes
#        #_nog016
#        # aqui de antemano ya no hay ningun self comb,
#        # por eso se hace tj sobre comb_g016
#        comb_atypes_nog016 = []
#        for ti in comb_atypes:
#            flag_array = []
#            for tj in comb_g016:
#                i = frozenset(ti)
#                j = frozenset(tj)
#                if i == j:
#                    flag_array.append(False)
#                else:
#                    flag_array.append(True)
#
#            if np.all(flag_array):
#                comb_atypes_nog016.append(ti)
#
        idxs_nb = []
        for idx in df_54a7_nb.index:
            flag_array = []

            t1 = df_54a7_nb['i'].loc[idx]
            t2 = df_54a7_nb['j'].loc[idx]
            ti = (t1, t2)

            if t1 == t2:
                print(ti)

#           for tj in comb_atypes_nog016:
            for tj in all_comb_atypes:
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
        epsilon_factor = kwargs.get("epsilon_factor", 1.0) # <==
        sigma_factor = kwargs.get("sigma_factor", 1.0)
        df_mod_g016 = self.gen_nonbonded_G016_2(epsilon_factor=epsilon_factor,
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


        f.close()
        
        return PATH_FFNB_RM
 


