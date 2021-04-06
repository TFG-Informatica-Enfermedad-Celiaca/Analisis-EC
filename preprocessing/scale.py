# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 21:04:55 2021

@author: Carla
@author: pablo
"""

import plotly.express as px
import plotly.io as pio
pio.renderers.default='browser'
import pandas as pd
from sklearn.preprocessing import RobustScaler, PowerTransformer,MinMaxScaler, QuantileTransformer

def plot_distribution(df, columns):
    for column in columns:
        print(df[column].dropna())
        fig = px.histogram(df, x=column,
                           title= "Distribución de "+ column)
        fig.show()

def print_scatter_plot(df, columns):
    fig = px.scatter_matrix(df, dimensions=columns)
    fig.update_traces(marker=dict(size=5))
    fig.update_layout(font=dict(
        size=5
    ))
    fig.show()

def robust_scaler(df):
    aux = df[["Diagnóstico"]]
    df = df.drop(columns=["Diagnóstico"])
    columns = df.columns
    
    transformer = RobustScaler()
    df = transformer.fit_transform(df)
    
    df = pd.DataFrame(df, columns = columns)
    df = pd.concat([df, aux], axis = 1)
    return df

def minmax_scaler(df):
    aux = df[["Diagnóstico"]]
    df = df.drop(columns=["Diagnóstico"])
    columns = df.columns
    
    transformer = MinMaxScaler()
    df = transformer.fit_transform(df)
    
    df = pd.DataFrame(df, columns = columns)
    df = pd.concat([df, aux], axis = 1)
    return df

def power_transformer(df):
    aux = df[["Diagnóstico"]]
    df = df.drop(columns=["Diagnóstico"])
    columns = df.columns
    
    transformer = PowerTransformer()
    df = transformer.fit_transform(df)
    
    df = pd.DataFrame(df, columns = columns)
    df = pd.concat([df, aux], axis = 1)
    return df

def quantile_transformer(df):
    aux = df[["Diagnóstico"]]
    df = df.drop(columns=["Diagnóstico"])
    columns = df.columns
    
    transformer = QuantileTransformer(n_quantiles=6, random_state=0)
    df = transformer.fit_transform(df)
    
    df = pd.DataFrame(df, columns = columns)
    df = pd.concat([df, aux], axis = 1)
    return df
