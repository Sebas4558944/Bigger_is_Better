# -*- coding: utf-8 -*-
"""
Created on Fri May 10 09:20:29 2019

@author: mathi
"""
import numpy as np
import math
import scipy as sp
import matplotlib.pyplot as plt

from control_curve import *
from stability import *
from loading_diagram import *
from seats import *

qcsweep    =  0.5515 #quarter chord sweep [rad]
hcsweepw    =  0.4869 #half chord sweep [rad]
A_w          =  8.67 #aspect ratio
S          =  427.8 #Wing surface
c          =  8.75 #mean aerodynamic chord
b          =  60.9 #wing span
c_r        =   12. #root chord
c_f        =   2.625 #flap chord
taper      =   0.149 #taper ratio
b_f0       =   15.6 #end of flap span
b_fi       =   4.1 #begin of flap span
l_f        =   56.4 #fuselage length
b_f        =   6.2 #fuselage diameter
h_f        =   6.2 #fuselage height
l_h        =   24.71 #tailarm
A_h        =   4.5 #aspect ratio horizontal tail
S_net      =   75. #area in fuselage

"""Coefficients"""
Cm_0       =   -0.1 #airfoil dependent moment coefficient 
CL_0       =   0.5 #CL of flapped wing at angle of attack of 0 deg 
CL_land    =   2.45 #CL during landing full flap configuration

"""Others"""
T0         =   293. #Temperature during landing  [K]
V_app      =   75.   #approach speed [m/s]
delta_flap =  0.5235 #flap deflection [rad]
alpha_land =   0.1745 #angle of attach during approach [rad]
M_app      =   0.22 #approach speed in Mach
eta        =  0.95# airfoil efficiency = 0.95

"""Retrieve from stability cruve program"""
x_ac       =  0.3   # aerodynamic centre location over the mac [n/m]
V_h_V      =  0.8    #(V_h/V) ratio  [m/s / m/s]
CL_alpha_AH =   4.788 # lif#t gradient of tailless aircraft [1/rad]
CL_AH       =  3.25 #lift coefficient A-H
CL_H        = -0.8 #liftcoefficient tail



#------------------------------VALUES GRAPHS--------------------------
mu_2       = 1. #2D to 3D correction factor from graph  
mu_3       = 0.025#  correction factor for sweep from graph
dc_c_f     =  0.5 # flap geometry ratio, see torenbeek book

M_h_cruise = 0.7395
hcsweeph= 0.525
A_h=4.5
M_w_cruise= 0.87
phi=0.3
h_wh = 3
s_wTEh= 24.71
b_n_1= 3.2
b_n_2= 3.2
b_n_3= 0
b_n_4= 0
l_n_1= -2
l_n_2= -2
l_n_3=0
l_n_4=0
x_ac_wing=0.4
l_fn= 20
c_g=c
SM=0.05

min_cg = potato(Safety_margin, xcg_fuel, W_fuel, W_fuse, W_nlg, W_vt, W_ht, W_fix, W_wing, W_nac, W_prop, W_mlg, cg_locations, xcg_nlg, xcg_mlg, X_LEMAC, W_payload, n_cargo, l_fuselage, MAC, n_pax, m_passenger, g, cargo_fwdfrac, xcg_seats, W_window, W_aisle, W_middle)[3] 
max_cg = potato(Safety_margin, xcg_fuel, W_fuel, W_fuse, W_nlg, W_vt, W_ht, W_fix, W_wing, W_nac, W_prop, W_mlg, cg_locations, xcg_nlg, xcg_mlg, X_LEMAC, W_payload, n_cargo, l_fuselage, MAC, n_pax, m_passenger, g, cargo_fwdfrac, xcg_seats, W_window, W_aisle, W_middle)[4]
X_LEMAC_range = potato(Safety_margin, xcg_fuel, W_fuel, W_fuse, W_nlg, W_vt, W_ht, W_fix, W_wing, W_nac, W_prop, W_mlg, cg_locations, xcg_nlg, xcg_mlg, X_LEMAC, W_payload, n_cargo, l_fuselage, MAC, n_pax, m_passenger, g, cargo_fwdfrac, xcg_seats, W_window, W_aisle, W_middle)[5]
S_control = Sh_S_control(CL_H,CL_AH,l_h,V_h_V,x_cg,Cm_0,A_w,qcsweep,delta_flap,b,b_f0,b_fi,taper,c,c_f,dc_c_f,mu_2,mu_3,x_ac,CL_land,b_f,h_f,l_f,S,S_net,hcsweepw,M_app,eta,CL_0)
S_stability = Sh_S_stability(x_cg, M_h_cruise, eta, hcsweeph, hcsweepw, A_w, A_h, M_w_cruise, b_f, b, S, l_h, qcsweep, phi, h_wh, s_wTEh, V_h_V, b_n_1, b_n_2, b_n_3, b_n_4, l_n_1, l_n_2, l_n_3, l_n_4, x_ac_wing, h_f, l_fn, c, c_r, c_g, taper, SM)

def control_stability_plot(min_cg, max_cg, X_LEMAC_range, S_control, S_stability):
    
    Sh_S = np.linspace(0,2,100)
    contr_trend = np.polyfit(x_cg, S_control, 1)
    stability_trend = np.polyfit(x_cg, S_stability, 1)
    a_control = contr_trend[0]
    b_control = contr_trend[1]
    a_stability = stability_trend[0]
    b_stability = stability_trend[1]

    Sh_opt = []
    LEMAC_opt = []
    for i in range(len(X_LEMAC_range)):
        
        for j in range(len(Sh_S)):
            x1 = (Sh_S[j] - b_control)/a_control
            x2 = (Sh_S[j] - b_stability)/a_stability
            
            if min_cg[i]>= x1 and max_cg[i]<x2:
                Sh_opt.append(Sh_S[j])
                LEMAC_opt.append(X_LEMAC_range[i])
                break

    print(len(Sh_opt))
    print(len(X_LEMAC_range))          
    print(LEMAC_opt)
    print(LEMAC_opt[Sh_opt.index(min(Sh_opt))])
    print(min(Sh_opt))
    print(min_cg[Sh_opt.index(min(Sh_opt))])
    print(max_cg[Sh_opt.index(min(Sh_opt))])
    
    X_LEMAC = list(np.array(X_LEMAC_range)+LEMAC_opt[Sh_opt.index(min(Sh_opt))])
    
    fig, ax1 = plt.subplots()

    ax2 = ax1.twinx()
    ax1.plot(x_cg, S_control, 'g-')
    ax1.plot(x_cg, S_stability, 'r')
    ax2.plot(min_cg, X_LEMAC, 'b-')
    ax2.plot(max_cg, X_LEMAC, 'b')
    
    plt.show()
    
    return

control_stability_plot(min_cg, max_cg, X_LEMAC_range, S_control, S_stability)


    
            

        
    