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
import matplotlib.pyplot as plt

masa_molar_agua = 18
Na = 6.022*1e23

class herramientas(object):

    def molar_mass(self, path):
        
        df_xyz = self.xyz2df(path)
        
        symbols = list(df_xyz['symbol'].unique())

        masa_molar = 0
        for symbol in symbols:

            mm = self.atomicMass(symbol)
            n = df_xyz['symbol'][df_xyz['symbol']== symbol].count()
            masa_molar+= n*mm    
        
        return masa_molar
        

    def atomicMass(self, symbol):
        
        path = "../data/general/atomic-mass-list.csv"
        df = pd.read_csv(path, sep=" ", header=None)
        Id = self.symbol2Id(symbol)

        return df[1][df[0]== Id].iloc[0]


    def symbol2Id(self, symbol):

        # https://github.com/Bowserinator/Periodic-Table-JSON
        path = "../data/general/periodic-table.json"
        df = pd.read_json(path)

        return df['atomicNumber'][df['symbol']==symbol].iloc[0]

    def xyz2df(self, path):

        dic = {}
        dic['symbol'] = {}
        dic['x'] = {}
        dic['y'] = {}
        dic['z'] = {}
        
        F = open(path, 'r')
        line =  F.readline()
        atoms = float(line.split()[0])
        line = next(F)

        i = 1
        for line in F:
            
            symbol = line.split()[0]
            x = float(line.split()[1])
            y = float(line.split()[2])
            z = float(line.split()[3])
            
            dic['symbol'][i] = symbol
            dic['x'][i] = x
            dic['y'][i] = y
            dic['z'][i] = z
            
            if i >= atoms:
                break
            i+=1

        return pd.DataFrame(dic)


    def wrapper_create_dirs(self, paths):

        for path in paths:
            cmd = ['mkdir', '-p', path]
            cmd = [str(item) for item in cmd]
            process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)

        return


    def create_grompp(self, **kwargs):

        PATH_GROMPP = kwargs.get('path_grompp', 'NULL')
        df = kwargs.get('df_grompp', 'NULL')
        comment_opts = kwargs.get('comment_opts', [])

        f = open(PATH_GROMPP, 'w')
        for col in df.columns:
            
            if col == "gmx":
                continue
            
            if col == "user":
                continue
            
            value = str(df[col].iloc[0])

            if col in comment_opts:
                f.write(";{:<30} = {:<30}\n".format(col, value))
            else:
                f.write("{:<30} = {:<30}\n".format(col, value))
            
        f.close()

        return


    def copy_file_to(self, **kwargs):

        PATH_IN = kwargs.get("path_in", "NULL")
        PATH_OUT = kwargs.get("path_out", "NULL")

        cmd = ["cp", PATH_IN, PATH_OUT]

        cmd = [str(item) for item in cmd]
        process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)    

        return    

    def copy_folder_to(self, **kwargs):

        PATH_IN = kwargs.get("path_in", "NULL")
        PATH_OUT = kwargs.get("path_out", "NULL")

        cmd = ["cp", "-r", PATH_IN, PATH_OUT]

        cmd = [str(item) for item in cmd]
        process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True)    

        return       

    def vol_cube_length(self, path, dens, num):
        
        masa_molar = self.molar_mass(path)
        
        vol = (masa_molar*num)/(dens*6.022*10*10)
        
        return np.power(vol, 1/3)

