# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 13:00:19 2021

@author: Carla
"""

from pyclustertend import hopkins 

def hopkins_test(df):
    X = df.drop(columns = ['Diagnóstico']).values
    print(hopkins(X, X.shape[0]))