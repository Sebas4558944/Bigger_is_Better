# -*- coding: utf-8 -*-
"""
Created on Tue May 28 09:19:12 2019

@author: mathi
"""

import loading_and_moment_diagrams as lm
from loading_and_moment_diagrams import load_diagrams

def required_Izz(Cr):
    M_max = max(load_diagrams(100)[0])
    y_max = 0.07 * Cr
    # print(y_max)
    sigma_ult = 502 * 10 ** 6
    I_zz = M_max * y_max / sigma_ult
    return 'I_zz=', I_zz

 #8.54#7.11#6.63#6.06
print(required_Izz(lm.Cr))
