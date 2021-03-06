#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 15 16:49:52 2019

@author: Max
"""
import numpy as np
import matplotlib.pyplot as plt
import os
#define forces on fuselage and its location of applocation
#all the forces weights and locations need to be put in!!!!!!

from Load_data import load


inputs = load('aerodynamic_concept')

print (inputs)

l_fus = inputs[25]
print (l_fus)
#weights from class 2
w_fus_group = 900000
w_wing_group = 500000
w_emp = 30000

#x-locations
x_ac_wing = 45
x_ac_ht = 90
x_cg_wing_group = 47
x_cg_emp = 92

x_wing_force = 45
x_emp_force = 92

#forces
F_wing = 800000
F_emp = 100000
#lifts
#L_wing = 1350000
#L_h_tail = w_fus_group+w_wing_group+w_emp-L_wing

#distributed load


def fuselage_diagrams(l_fus, F_wing, F_emp, x_wing_force, x_emp_force):
    q_fus = w_fus_group/l_fus
    
    dx = 0.01
    x_range = np.arange(0,l_fus+dx,0.01)
    
    v_y = np.zeros(len(x_range))
    m_x = np.zeros(len(x_range))
    
    def step(x):
        return 1 * (x > 0)
    
    for i in range(len(x_range)):
        x = x_range[i]
        v_y[i] = -q_fus*x +step(x - x_wing_force)*F_wing + step(x - x_emp_force)*F_emp
        
        m_x[i] = (+0.5*q_fus*x**2 - step(x - x_wing_force)*F_wing*x - step(x - x_emp_force)*F_emp*x)
        
    #    if x_range[i] >= x_ac_wing and x_range[i] <= x_cg_wing_group:
    #        v_y[i] = v_y[i] - L_wing
    #        
    #    elif x_range[i] >= x_cg_wing_group and x_range[i] <= x_ac_ht:   
    #        v_y[i] = v_y[i] - L_wing + w_wing_group 
    #    
    #    elif x_range[i] >= x_ac_ht and x_range[i] <= x_cg_emp :
    #        v_y[i] = v_y[i] -L_wing + w_wing_group - L_h_tail
    #    
    #    elif x_range[i] >= x_cg_emp:
    #        v_y[i] = v_y[i] -L_wing + w_wing_group - L_h_tail + w_emp
    #    
    #
    m_ac = m_x[-1]    
    for i in range(len(x_range)):
        x = x_range[i]
        m_x[i] = m_x[i] - step(x - x_ac_wing)*m_ac    
        
    plt.subplot(121)
    plt.title("y shear force diagram of the fuselage")
    plt.grid()
    plt.plot(x_range,v_y)
    plt.xlabel('Fuselage length (m)')
    plt.ylabel('Shear Force (N)')
    plt.subplot(122)
    plt.plot(x_range,m_x)
    plt.grid()
    plt.title("x moment diagram of the fuselage")
    plt.xlabel('Fuselage length (m)')
    plt.ylabel('Moment (Nm)')
    plt.show()    
    

fuselage_diagrams(l_fus, F_wing, F_emp, x_wing_force, x_emp_force)


#def fuselage_stress(d_fus, cruise_height, cabin height, yield_strength)
