# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 13:00:19 2021

@author: Carla
"""

from pyclustertend import hopkins 

def hopkins_test(df, name):
    X = df.drop(columns = ['Diagnóstico']).values
    print("El valor del estadístico de hopkins es para el dataset ", name)
    print(hopkins(X, X.shape[0]))