# -*- coding: utf-8 -*-
"""
Created on Wed May 15 14:56:07 2019

@author: nikki
"""

# -*- coding: utf-8 -*-
"""
Created on Tue May 14 08:55:23 2019

@author: nikki
"""

# -------------------------------MODULES---------------------------------------
import numpy as np
import matplotlib.pyplot as plt

# ------------------------------VERIFICATION DATA--------------------------------

"""Create reference line of B737 8 Max"""
# Obatined from old SAR code
SAR_ref = 1.84236002771
M_ref = 0.79
g = 9.80565


# -----------------------------DEFINITIONS-------------------------------------
# Standard air range (SAR) = distances travelled per mass fuel burned
# Fuel burn is related to speed, altitude, thrust (or drag in steady flight)
# unit of SAR (m/s)/(kg/s)

def ISA_density(h):  # enter height in m
    M = 0.0289644  # kg/mol molar mass of Earth's air
    R = 8.3144590  # universal gas constant Nm/MolK

    if h < 11000:
        rho0 = 1.225  # kg/m^3
        T = 288.15  # K
        h0 = 0.  # m
        a = -0.0065  # K/m
        rho = rho0 * (T / (T + a * (h - h0))) ** (1. + ((g * M) / (R * a)))

    if h >= 11000:
        rho0 = 0.36391  # kg/m^3
        T = 216.65  # K
        h0 = 11000.  # m
        rho = rho0 * np.e ** ((-g * M * (h - h0)) / (R * T))

    return rho


def ISA_temp(h):
    if h < 11000:
        T = 288.15 - 0.0065 * h  # in Kelvin
        return T
    if h >= 11000:
        return 216.65  # in Kelvin


def Mach(V, h):  # enter V in km/h
    gamma = 1.4  # enter h in m
    R = 287  # J/kg/K
    a = np.sqrt(gamma * R * ISA_temp(h))
    M = (V / 3.6) / a
    return M


def Velocity(M, h):
    gamma = 1.4
    R = 287
    a = np.sqrt(gamma * R * ISA_temp(h))
    V = M * a
    return V

#print Velocity(0.75,12000)

def SAR(V, h, A, S, e, CD0, Ct0, Wcr):  # enter h in m, V in m/s
    SAR = []
    for i in range(len(V)):
        Ct = (Ct0[i] / 233.083) * (V[i])  #
        k = 1. / (np.pi * A[i] * e[i])
        q = 0.5 * ISA_density(h[i]) * (V[i]) ** 2
        SAR_i = (1. / ((V[i]) / ((CD0[i] + k * (Wcr[i] / (q * S[i])) ** 2) * q * S[i] * Ct))) * 1000.  # in kg/km
        SAR.append(SAR_i / 450)

    # for i in range(len(V)):
    #     V[i] = Mach(V[i], h[i])  # here you change V to mach number (still called V tho)

    # plt.figure(1)
    # plt.plot(V[i], SAR[i], 'o', label='%s Design' % i)
    # plt.plot(M_ref, SAR_ref, 'mo', label="Ref. aircraft")
    # plt.hlines(0.9 * SAR_ref, .1, 1, "gray", "--")
    # plt.title('Fuel consumption w.r.t. Mach number')
    # plt.xlabel("Mach number")
    # plt.ylabel("Fuel consumption [kg/km]")
    # plt.legend()
    return h, SAR
