# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 14:36:26 2019

@author: mathi
"""
from spar_locations import spar_loc
import numpy as np 
import scipy as sp
from scipy import interpolate
from airfoil_geometry import airfoil_geometry
from loading_and_moment_diagrams import c
import loading_and_moment_diagrams as lm


N= 100
b = lm.b
HalfspanValues = np.linspace(0, b / 2 - 0.00001, N)

airfoil_area = []
z_c_airfoil = []
y_c_airfoil = []
for i in range(len(HalfspanValues)):
    z_c_airfoil.append(0.42*c(HalfspanValues[i]))
    y_c_airfoil.append(0.0231*c(HalfspanValues[i]))
    airfoil_area.append(9.59*10**(-2)*c(HalfspanValues[i]))
    
data_z_all_sec = airfoil_geometry(N,b)[0]
data_y_upper_all_sec = airfoil_geometry(N,b)[1]
data_y_lower_all_sec = airfoil_geometry(N,b)[2]


n_stiff_up = 6
n_stiff_low = 4
l_spar_h = 0.2
t_spar_h = 0.01
t_spar_v = 0.01
nr_spars = 2
first_spar = 0.2 
last_spar = 0.6
delta_spar = spar_loc(HalfspanValues, nr_spars, first_spar, last_spar)[1] 
spar_loc_sec = spar_loc(HalfspanValues, nr_spars, first_spar, last_spar)[0]
spar_areas_hori = l_spar_h*t_spar_h*np.ones(nr_spars)
boom_area = 0.0007
#print(spar_loc_sec[0][0])

def wing_centroid(boom_area, spar_areas_hori, t_spar_v, z_c_airfoil, y_c_airfoil, n_stiff_up, n_stiff_low, HalfspanValues):
    
    n_total = n_stiff_up+n_stiff_low
    
    z_loc_stiff_up = []
    z_loc_stiff_low = []
    y_loc_spar_up = np.zeros((len(HalfspanValues), len(spar_loc_sec[0])))
    y_loc_spar_low = np.zeros((len(HalfspanValues), len(spar_loc_sec[0])))
    y_vertical_spar = np.zeros((len(HalfspanValues), len(spar_loc_sec[0])))
    spar_areas_verti = np.zeros((len(HalfspanValues), nr_spars))

#    print(np.shape(spar_loc_sec))
#    print(spar_loc_sec[1][-1])
    
    for i in range(len(HalfspanValues)):
        stepsize_up = (spar_loc_sec[i][-1]-spar_loc_sec[i][0])/(n_stiff_up+1)
        stepsize_low = (spar_loc_sec[i][-1]-spar_loc_sec[i][0])/(n_stiff_low+1)
        z_loc_up = np.arange(spar_loc_sec[i][0] + stepsize_up, spar_loc_sec[i][-1]-0.001, stepsize_up)
#        print(z_loc_up)
        z_loc_stiff_up.append(z_loc_up)
        z_loc_low = np.arange(spar_loc_sec[i][0] + stepsize_low , spar_loc_sec[i][-1] -0.001, stepsize_low)
        z_loc_stiff_low.append(z_loc_low)
        
    y_loc_stiff_up = np.zeros((len(HalfspanValues), len(z_loc_up)))
    y_loc_stiff_low = np.zeros((len(HalfspanValues), len(z_loc_low)))    
    
    for i in range(len(HalfspanValues)):
        Polyfit_airfoil_upper = sp.interpolate.interp1d(data_z_all_sec[i], data_y_upper_all_sec[i], kind="cubic", fill_value="extrapolate")
        Polyfit_airfoil_lower = sp.interpolate.interp1d(data_z_all_sec[i], data_y_lower_all_sec[i], kind="cubic", fill_value="extrapolate")

        for j in range(len(z_loc_up)):
            y_loc_up = Polyfit_airfoil_upper(z_loc_up[j])
            y_loc_stiff_up[i][j] = y_loc_up 

        for d in range(len(z_loc_low)):
            y_loc_low = Polyfit_airfoil_lower(z_loc_low[d])
            y_loc_stiff_low[i][d] = y_loc_low
        
        for k in range(len(spar_loc_sec[0])):
            y_loc_up_spar = Polyfit_airfoil_upper(spar_loc_sec[i][k])
            y_loc_spar_up[i][k] = y_loc_up_spar
            y_loc_low_spar = Polyfit_airfoil_lower(spar_loc_sec[i][k])
            y_loc_spar_low[i][k]= y_loc_low_spar
            l_spar_v = y_loc_up_spar - y_loc_low_spar
            y_vertical_spar[i][k] = (y_loc_up_spar - y_loc_low_spar)/2
            spar_areas_verti[i][k] = l_spar_v*t_spar_v
    

    z_centroid_all_sec = [] 
    y_centroid_all_sec = []      
    for i in range(len(HalfspanValues)):
        z_A = 0
        y_A = 0
        
        for j in range(len(z_loc_stiff_up[0])):
            z_A += z_loc_stiff_up[i][j]*boom_area
            y_A += y_loc_stiff_up[i][j]*boom_area
        for m in range(len(z_loc_stiff_low[0])):
            z_A += z_loc_stiff_low[i][m]*boom_area
            y_A += y_loc_stiff_low[i][m]*boom_area
        for l in range(len(spar_loc_sec[0])):
            z_A += spar_loc_sec[i][l]*spar_areas_hori[l]
            y_A += y_loc_spar_low[i][l]*spar_areas_hori[l]
        for n in range(len(spar_loc_sec[0])):
            z_A += spar_loc_sec[i][k]*spar_areas_hori[k]
            y_A += y_loc_spar_low[i][k]*spar_areas_hori[k]
        for t in range(len(spar_loc_sec[0])):
            z_A += spar_loc_sec[i][t]*spar_areas_verti[i][t]
            y_A += y_vertical_spar[i][t]*spar_areas_verti[i][t]
        
#        print(spar_areas_verti)
        z_A += z_c_airfoil[i]*airfoil_area[i]
        y_A += y_c_airfoil[i]*airfoil_area[i]
        

        total_area = boom_area*n_total+sum(spar_areas_hori)*2 + sum(spar_areas_verti[i]) + airfoil_area[i]
#        print(total_area)
#        print("hoi",y_A/total_area)
        
        z_centroid_all_sec.append(z_A/total_area)
        y_centroid_all_sec.append(y_A/total_area)
    
#    print(c(HalfspanValues[0]))
#    print(z_loc_stiff_low)    
#    print(z_centroid_all_sec[0])
#    print(y_centroid_all_sec[0])

    return z_centroid_all_sec, y_centroid_all_sec, y_loc_spar_up, y_loc_spar_low, y_loc_stiff_up, y_loc_stiff_low, y_vertical_spar, z_loc_stiff_up, spar_loc_sec, z_loc_stiff_low

#print(wing_centroid(boom_area, spar_areas_hori, t_spar_v, z_c_airfoil, y_c_airfoil, n_stiff_up, n_stiff_low, HalfspanValues)[1])
#print(wing_centroid(boom_area, spar_areas_hori, spar_areas_verti, z_c_airfoil, y_c_airfoil, n_stiff_up, n_stiff_low, HalfspanValues)[1])
#print(wing_centroid(boom_area, spar_areas, z_c_airfoil, y_c_airfoil, n_stiff_up, n_stiff_low, HalfspanValues)[7])