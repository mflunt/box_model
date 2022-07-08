#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A module to setup box model for DARE Summer School practical

Created on Mon Jul  4 16:00:57 2022

@author: mlunt
"""

import numpy as np
import matplotlib.pyplot as plt

atm_convert = 2.767   # CH4 conversion Tg/ppb
#%%

def get_noaa_data():
    """Retrieve NOAA CH4 data from 2005-2022 
    Returns:
        ch4_obs: NOAA global mean CH4 data from January each year 2005-2022 inclusive.
        years: numpy array of integers 2005-2022
    """
    ch4_obs = np.asarray([1776. , 1779.5, 1779.2, 1786.8, 1795.1, 1797.1, 
                          1800.5, 1807.3, 1814.1, 1816.9, 1832.9, 1842.5, 
       1849.8, 1854.5, 1865. , 1874. , 1890.7, 1908.9])
    
    years = np.arange(2005, 2023)
    return ch4_obs, years

def model(years, m0, emis, k):
    """Run global box model of CH4 concentration
    Args:
        years: Array of integer years (numpy array)
        m0: Initial CH4 mole fraction in ppb (scalar)
        emis: CH4 emissions. Either np array of len(nyears) or a scalar
        k: Loss rate of methane. Either np array of len(nyears) or a scalar
    Returns:
        m_ppb: Array len(nyears) of CH4 concentration
    """
    
    ntime = len(years)
    m = np.zeros((ntime))
    m[0] = m0*atm_convert
    
    if isinstance(emis, np.ndarray) and isinstance(k, np.ndarray):
        for ti in range(ntime-1):
            m[ti+1] = m[ti]*np.exp(-1.*k[ti]) +emis[ti]/k[ti]*(1. - np.exp(-1.*k[ti]))
           
    elif isinstance(emis, np.ndarray) and type(k) in (float, int):
        for ti in range(ntime-1):
            m[ti+1] = m[ti]*np.exp(-1.*k) +emis[ti]/k*(1. - np.exp(-1.*k))
            
    elif type(emis) in (float,int) and isinstance(k, np.ndarray):
        for ti in range(ntime-1):
            m[ti+1] = m[ti]*np.exp(-1.*k[ti]) +emis/k[ti]*(1. - np.exp(-1.*k[ti]))
               
    else:
        for ti in range(ntime):
            m[ti] = m[0]*np.exp(-1.*k*ti) +emis/k*(1. - np.exp(-1.*k*ti))
        
    
    m_ppb = m/atm_convert
    return m_ppb

def plot_model(years,m):
    """Plot the CH4 concentration as a function of time
    Args:
        years: Array of integer years (numpy array)
        m: CH4 mole fraction in ppb (numpy array)
    """
    
    fig,ax=plt.subplots()

    ax.plot(years,m)
    ax.set_ylabel("CH$_4$ mole fraction (ppb)" )
    ax.set_xlabel("Year")
    plt.tight_layout()