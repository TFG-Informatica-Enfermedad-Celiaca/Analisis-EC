# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 11:43:39 2021

@author: Carla
"""
from sklearn.experimental import enable_iterative_imputer 
from sklearn.impute import IterativeImputer
import pandas as pd
from sklearn.impute import KNNImputer
import operator

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

def imputation(df):
    # Before calling knn_imputation, calculate the mean of values that weren't 
    # missing and have DCG_ATG2_Negativo = 1 (do the same with DCG_ATG2_Positivo, 
    # DSG_ATG2_Negativo, DSG_ATG2_Positivo, DCG A-PDG_Negativo, DCG A-PDG_Positivo, 
    # DSG A-PDG_Negativo and DSG A-PDG_Positivo)
    categorical_columns = {
        "DCG_ATG2_Negativo": {"mean": 0,
                              "threshold": [operator.gt, 20],
                              "numerical": "DCG_ATG2_VALUE"},
        "DCG_ATG2_Positivo": {"mean": 0,
                              "threshold": [operator.lt, 20],
                              "numerical": "DCG_ATG2_VALUE"},
        "DSG ATG2_Negativo": {"mean": 0,
                              "threshold": [operator.gt, 20],
                              "numerical": "DSG ATG2 VALUE"}, 
        "DSG ATG2_Positivo": {"mean": 0,
                              "threshold": [operator.lt, 20],
                              "numerical": "DSG ATG2 VALUE"},
        "DCG A-PDG_Negativo": {"mean": 0,
                               "threshold": [operator.gt, 25],
                               "numerical": "DCG A-PDG_VALUE"},
        "DCG A-PDG_Positivo": {"mean": 0,
                               "threshold": [operator.lt, 25],
                               "numerical": "DCG A-PDG_VALUE"},
        "DSG A-PDG_Negativo": {"mean": 0,
                               "threshold": [operator.gt, 25],
                               "numerical": "DSG A-PDG VALUE"},
        "DSG A-PDG_Positivo": {"mean": 0,
                               "threshold": [operator.lt, 25],
                               "numerical": "DSG A-PDG VALUE"}
        }
    for column in categorical_columns.keys():
        categorical_columns[column]["mean"] = df.loc[df[column] == 1, 
                        categorical_columns[column]["numerical"]].mean(skipna=True)

    df = knn_imputation(df)
    
    # If the imputer has imputed a wrong value we change the imputation to the
    # mean of the non-missing values
    for item in categorical_columns.keys():
        df.loc[categorical_columns[item]["threshold"][0](
            df[categorical_columns[item]["numerical"]],
                categorical_columns[item]["threshold"][1]) 
               & df[item] ==1 , categorical_columns[item]["numerical"]
               ] = categorical_columns[item]["mean"]
       
    return df
        
        
        
        