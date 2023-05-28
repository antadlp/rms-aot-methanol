import numpy as np
import pandas as pd


class rms_meoh(object):

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
    
    
    
    