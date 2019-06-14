# -*- coding: utf-8 -*-
"""
Created on Fri May 17 10:03:19 2019

@author: mathi
"""

import practised as prac
import Airfoil_inertia as ai
import centroid_wing as cw
import numpy as np
import math as m
#

def strut_area_req_F(sigma):
    
    F_strut = prac.results[0]
    A_req = np.zeros(len(prac.A_S_L))
    
    for i in range(len(prac.A_S_L)):

        A_req[i] = F_strut[i]/sigma

    return A_req

def strut_area_req_B():
    
    F_strut = prac.results[0]
    R_strut = prac.R_strut
    L_strut = prac.results[3]
    I_strut = 0.25*np.pi*R_strut**2
    P_cr = F_strut
    I_req = np.zeros(len(prac.A_S_L))
    req_area = np.zeros(len(prac.A_S_L))
    sigma_crit = np.zeros(len(prac.A_S_L))
    K = 1. 
    
    for i in range(len(prac.A_S_L)):
        I_req[i] = P_cr[i]*(K*L_strut[i])**2/(np.pi**2*prac.E_strut)
        while I_req[i]<I_strut:
            R_strut += 0.001
            I_req[i] = 0.25*np.pi*R_strut**2
            print(R_strut)

        req_area[i] = np.pi*R_strut**2
        sigma_crit[i] = P_cr[i]/req_area[i]
    
    return I_req, req_area, sigma_crit

def strut_cost(A_req_P, A_req_B, density, cost):
    Max_area = np.zeros(len(A_S_L))
    strut_volume = np.zeros(len(A_S_L))
    strut_mass = np.zeros(len(A_S_L))
    strut_cost = np.zeros(len(A_S_L))
    L_strut =  prac.L_strut_list
    
    for i in range(len(A_S_L)):
        Max_area[i] = max(A_req_P[i], A_req_B[i])

        strut_volume[i] = Max_area[i]*L_strut[i]
        strut_mass[i] = strut_volume[i]*density
        strut_cost[i] = strut_mass[i]*cost
    
    return Max_area, strut_volume, strut_mass, strut_cost


def wing_price_weight(A_req_P, A_req_B, density, cost, N, t_skin, b, qcsweep):
            
    Max_area, strut_volume, strut_mass, cost_strut = strut_cost(A_req_P, A_req_B, density, cost)
    airfoil_area, z_c_airfoil, y_c_airfoil = cw.get_skin_centroid(N, b, prac.calc_chord)
    spar_areas_verti = cw.wing_centroid(cw.boom_area, cw.spar_areas_hori, cw.t_spar_v, z_c_airfoil, y_c_airfoil, cw.n_stiff_up, cw.n_stiff_low, N, b, prac.calc_chord)
    spar_areas_hori = cw.spar_areas_hori
    boom_area = cw.boom_area
    nr_stiff  = cw.n_stiff_low + cw.n_stiff_up
    Sweep_LE = m.atan(m.tan(qcsweep) - 4 / prac.AR * (-0.25 * (1 - prac.taper) / (1 + prac.taper))) # rad
    
#    print(spar_areas_verti[0])
#    print(spar_areas_hori)
    
    
    total_spar_area = 0
    for i in range(len(spar_areas_hori)):
        for j in range(len(spar_areas_verti[0])):
            
            total_spar_area += spar_areas_verti[i][j] + spar_areas_hori[i]*2 
    
    total_boom_volume = (boom_area * nr_stiff)* (b/2)/np.cos(Sweep_LE)
    boom_mass = total_boom_volume * density
    boom_cost = boom_mass * cost
    
    skin_volume = np.zeros(len(X_root_plot))

    for i in range(len(X_root_plot)-1):
        
        skin_volume[i] = ai.s_airfoil(N,b, prac.calc_chord)[i]*prac.dx*t_skin
    
    skin_mass = sum(skin_volume) * density
    skin_price = skin_mass * cost
    
    spar_length = (b/2)/np.cos(Sweep_LE)
    spar_volume = total_spar_area*spar_length
    spar_mass = spar_volume * density
    spar_price = spar_mass * cost
    
    total_price = np.zeros(len(A_S_L))
    total_mass = np.zeros(len(A_S_L))
    
    for i in range(len(prac.A_S_L)):
        
        total_price[i] = (skin_price + spar_price)*2 + cost_strut[i]*2 + boom_cost*2
        total_mass[i] = (skin_mass + spar_mass)*2 + strut_mass[i]*2 + boom_mass*2
    
    return  skin_mass, spar_mass, boom_mass, total_mass, total_price

t_skin = 0.002
N = prac.N
b = prac.b
sigma = 100 * 10 ** 6
density = 2750
cost = 3.63 
qcsweep = (25/180) * np.pi

A_req_P = strut_area_req_F(sigma)
I_req, A_req_B, sigma_crit= strut_area_req_B()

max_strut_area, strut_volume, strut_mass, cost_strut = strut_cost(A_req_P, A_req_B, density, cost)
skin_mass, spar_mass, boom_mass, total_mass, total_price = wing_price_weight(A_req_P, A_req_B, density, cost, N, t_skin, b, qcsweep)

print("area due to force",A_req_P)
print()
print("area due to buckling",A_req_B)
print()
print("Ireq for buckling",I_req)
print()
print("critical stress", sigma_crit)
print()
print("skin mass", skin_mass)
print()
print("spar mass", spar_mass)
print()
print("boom mass", boom_mass)
print()
print("strut mass", strut_mass)
print()
print("total mass", total_mass)
print()
print("total cost", total_cost)


