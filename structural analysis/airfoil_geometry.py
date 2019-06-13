# -*- coding: utf-8 -*-
"""
Created on Thu May 16 09:55:34 2019

@author: Mathilde
"""

import numpy as np  ### Never use * to import stuff, as it makes it difficult to retrace where functions come from
import scipy as sp
import math as m
from scipy import interpolate ### Useful to interpolate stuff
from scipy import integrate
from matplotlib import pyplot as plt
#from stress_distribution_wing import load_airfoil
from loading_and_moment_diagrams import c
import loading_and_moment_diagrams as lm

N = 100
b = lm.b#39.56 #41.76

def load_airfoil(filename):
    f = open(filename,'r')
    lines = f.readlines()
    data = []
    data_z = []
    data_y = []
    for line in lines:
        x = line.split()
        data.append(x)
    for i in range(len(data)):
        for j in range(len(data[i])):
            data[i][j] = float(data[i][j])
    for i in range(len(data)):
        data_z.append(data[i][0])
        data_y.append(data[i][1])

#    plt.plot(data_z,data_y)
#    plt.axis('equal')
#    plt.show()
    return data,data_z,data_y
#
#filename = 'SC(2)-0616.txt'
#print(load_airfoil(filename))

def airfoil_geometry(N,b):

    HalfspanValues = np.linspace(0, b / 2 - 0.00001, N)
#    print(HalfspanValues[0])
    
    data_z_all_sec = []
    data_y_lower_all_sec = []
    data_y_upper_all_sec = []
    
    for i in range(len(HalfspanValues)):
        
        data_z, data_y = load_airfoil('SC(2)-0616.txt')[1], load_airfoil('SC(2)-0616.txt')[2] 
        data_z_order =  np.array(data_z[0:int((len(data_y)/2))])*c(HalfspanValues[i])
        data_z_all_sec.append(data_z_order)
        data_y_lower = np.array(data_y[(int((len(data_y)/2))):])*c(HalfspanValues[i])
        data_y_lower_all_sec.append(data_y_lower)
        data_y_upper = np.array(data_y[0:int((len(data_y)/2))])*c(HalfspanValues[i])
        data_y_upper_all_sec.append(data_y_upper)
    
    data_z_all_sec = np.asarray(data_z_all_sec)
    data_z_all_sec = np.reshape(data_z_all_sec, (len(HalfspanValues),len(data_z_order)))
    data_y_upper_all_sec = np.asarray(data_y_upper_all_sec)
    data_y_upper_all_sec = np.reshape(data_y_upper_all_sec, (len(HalfspanValues),len(data_z_order)))
    data_y_lower_all_sec = np.asarray(data_y_lower_all_sec)
    data_y_lower_all_sec = np.reshape(data_y_lower_all_sec,(len(HalfspanValues),len(data_z_order)))
    
#    print(data_y_upper_all_sec[0])
#    print(data_y_lower_all_sec[10])
    return data_z_all_sec, data_y_upper_all_sec, data_y_lower_all_sec


#data = load_airfoil('NACA3414.txt')
data_z_all_sec, data_y_upper_all_sec, data_y_lower_all_sec = airfoil_geometry(N,b)
#plt.scatter(data_z_all_sec[0], data_y_upper_all_sec[0])
#plt.scatter(data_z_all_sec[0], data_y_lower_all_sec[0])
#plt.show()
##print(data_z_all_sec[0])
#print(data_y_upper_all_sec[0])
##print(data_y_lower_all_sec[0])
#print(np.shape(data_z_all_sec))