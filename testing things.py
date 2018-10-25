# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 14:20:02 2018

@author: Otros
"""

a = {'activation': 'linear',
 'bias_initializer': 'randomNormal',
 'kernel_initilializer': 'randomNormal',
 'layer_type': 'Dense',
 'units': '1',
 'use_bias': True}

def testing(**kargs):
    print(kargs['use_bias'])
    
testing(**a)