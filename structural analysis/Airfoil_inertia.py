# -*- coding: utf-8 -*-
"""
Created on Wed May 15 16:01:47 2019

@author: floyd
"""
import numpy as np
import math as m
import scipy as sp
from stress_distribution_wing import load_airfoil
from loading_and_moment_diagrams import c
from airfoil_geometry import airfoil_geometry

N = 100 
b = 60.#47.83#39.56#41.76
HalfspanValues = np.linspace(0, b / 2 - 0.00001, N)


def inertia(N,b):
    #loading the airfoil data
#    data = load_airfoil("naca3414.txt")
#    dataz = np.asarray(data[1])
#    datay = np.asarray(data[2])
#    #ordering the data
    x_position = 0
    data_z_all_sec = airfoil_geometry(N,b)[0]
    data_y_upper_all_sec = airfoil_geometry(N,b)[1]
    data_y_lower_all_sec = airfoil_geometry(N,b)[2]
    #defining the integrated function
    Polyfit_airfoil_upper = sp.interpolate.interp1d(data_z_all_sec[x_position], data_y_upper_all_sec[x_position], kind="cubic", fill_value="extrapolate")
    Polyfit_airfoil_lower = sp.interpolate.interp1d(data_z_all_sec[x_position], data_y_lower_all_sec[x_position], kind="cubic", fill_value="extrapolate")
    #
    #def y_upper(z):    
    #    y_upper = Polyfit_airfoil_upper(z)  #put in right y function
    #    return(y_upper)
    #def y_lower(z):
    #    y_lower = Polyfit_airfoil_lower(z) #put in right y function
    #    return(y_lower)
    
    spar_loc_sec = []
    for i in range(len(HalfspanValues)):
        nr_spars = 4
        first_spar_location = 0.2*c(HalfspanValues[i])
        last_spar_location = 0.75*c(HalfspanValues[i])
        delta_spar = (last_spar_location-first_spar_location)/(nr_spars)
        spar_loc = np.arange(first_spar_location,last_spar_location+delta_spar,delta_spar)
        spar_loc_sec.append(spar_loc)
        
    #    print(c(HalfspanValues[i]))
    print(spar_loc_sec)        
    
    upper_y = np.zeros(len(spar_loc))
    lower_y = np.zeros(len(spar_loc))
    
    for i in range(len(spar_loc)):
        
        upper_y[i] = Polyfit_airfoil_upper(spar_loc_sec[x_position][i])
    
        lower_y[i] = Polyfit_airfoil_lower(spar_loc_sec[x_position][i])
        
    delta_z = []
    delta_y_upper = []
    delta_y_lower = []
    middle_y_upper = []
    middle_y_lower = []
    
    for i in range(len(spar_loc)-1):
        delta_y_upper.append(upper_y[i+1]-upper_y[i])
        delta_y_lower.append(lower_y[i+1] - lower_y[i])
        delta_z.append(spar_loc_sec[x_position][i+1]-spar_loc_sec[x_position][i])
        middle_y_upper.append(upper_y[i] + (upper_y[i+1]-upper_y[i])/2)
        middle_y_lower.append(lower_y[i] + (lower_y[i+1]-lower_y[i])/2)
    
    middle_z = spar_loc_sec[x_position] + delta_z[0]
    
    #Moment of inertia of flanges on its own centroid
    I_xx_upper = []    
    I_xx_lower = []
    I_yy_upper = []
    I_yy_lower = []
    I_xy_upper = []
    I_xy_lower = []
    
    upper_s = []
    lower_s = []
    
    t= 0.005
    centroid_y = 0.05
    centroid_z = 0.4*c(HalfspanValues[0])
    
    for i in range(len(delta_z)):
        s_upper = m.sqrt(delta_z[i]**2 + delta_y_upper[i]**2)
        s_lower = m.sqrt(delta_z[i]**2 + delta_y_lower[i]**2)
        upper_s.append(s_upper)
        lower_s.append(s_lower)
        beta = m.atan(delta_y_upper[i]/delta_z[i])
        area_upper = s_upper*t
        area_lower = s_lower*t
        dy_upper = middle_y_upper[i] - centroid_y
        dy_lower = middle_y_lower[i] - centroid_y
        dx_lower = middle_z[i] - centroid_z
        dx_upper = middle_z[i] - centroid_z
        I_xx_lower.append(s_lower**3*t*np.sin(beta)**2/12.+ area_lower*dy_lower**2)
        I_xx_upper.append(s_upper**3*t*np.sin(beta)**2/12.+ area_upper*dy_upper**2)
        I_yy_lower.append(s_lower**3*t*np.cos(beta)**2/12.+ area_lower*dx_lower**2)
        I_yy_upper.append(s_upper**3*t*np.cos(beta)**2/12. + area_upper*dx_upper**2)
        I_xy_lower.append(s_lower**3*t*np.sin(2*beta)/24.+ area_lower*dx_lower*dy_lower)
        I_xy_upper.append(s_upper**3*t*np.sin(2*beta)/24. + area_upper*dx_upper*dy_upper)
    
    return upper_y, lower_y, upper_s, lower_s

print(sum(inertia(N,b)[2]))
#sum_s_wingbox = sum(inertia(N,b)[2]) + sum(inertia(N,b)[3])
#print(sum_s_wingbox)
#print(sum(I_xx_lower)+sum(I_xx_lower) + sum(I_xx_upper) + sum(I_xx_upper))

