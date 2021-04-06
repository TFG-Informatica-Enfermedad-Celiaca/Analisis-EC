# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 11:00:51 2021

@author: Carla
"""
import pandas as pd
from utils import categorical_columns

def transform_categorical_to_numerical(df):
    for column in categorical_columns:
        aux = pd.get_dummies(df[column], prefix=column)
        df = df.drop(columns= column)
        df = pd.concat([df, aux], axis = 1)
    return df

def fill_null_value_categorical(df):
    df[categorical_columns] = df[categorical_columns].fillna("Desconocido")
    return df