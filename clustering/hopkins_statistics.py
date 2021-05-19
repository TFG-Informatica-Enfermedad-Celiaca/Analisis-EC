# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 13:00:19 2021

@author: Carla
"""

from pyclustertend import hopkins 
from sklearn.neighbors import BallTree
import numpy as np
import pandas as pd

def hopkins_test(df, name):
    X = df.drop(columns = ['Diagnóstico']).values
    aux = hopkins(X, X.shape[0])
    
    return aux
    