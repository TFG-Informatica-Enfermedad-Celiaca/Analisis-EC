# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 11:43:39 2021

@author: Carla
"""
from sklearn.experimental import enable_iterative_imputer 
from sklearn.impute import IterativeImputer
import pandas as pd
from sklearn.impute import KNNImputer

# Suffers from Convergence Warming:
# Early stopping criterion not reached
def multivariate_imputation(df):
     imp = IterativeImputer(max_iter=100, random_state=0)
     df = df.drop(columns=["Diagnóstico"])
     columns = df.columns
     df = imp.fit_transform(df.to_numpy())
     df = pd.DataFrame(df, columns = columns)
     return df
     
def knn_imputation(df):
    aux = df[["Diagnóstico"]]
    df = df.drop(columns=["Diagnóstico"])
    columns = df.columns
    
    imputer = KNNImputer(n_neighbors=4)
    df = imputer.fit_transform(df.to_numpy())
    
    df = pd.DataFrame(df, columns = columns)
    df = pd.concat([df, aux], axis = 1)
    return df
    