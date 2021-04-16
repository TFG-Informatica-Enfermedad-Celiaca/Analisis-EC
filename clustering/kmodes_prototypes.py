# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 12:08:08 2021

@author: Carla
@author: pablo
"""

from kmodes.kmodes import KModes
from kmodes.kprototypes import KPrototypes
from tqdm import tqdm
from sklearn.metrics import silhouette_score
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default='browser'
import numpy as np
import sys
sys.path.append(r'../')
from reduceDimension import reduce_dimension_after_clustering
from scoreF1 import f1_score
from rater import rate
from utils import categorical_columns
from silhouette import silhouette

def kmodes(df_numerical, df, extended_information):
    data = df.drop(columns = ['Diagnóstico'])
    data_numerical = df_numerical.drop(columns = ['Diagnóstico'])
    
    X = data.to_numpy()

    [n_clusters,max_silhouette] = silhouette("K-Modes", data_numerical, None, X,None, 
                                    KModes,None,extended_information, init='Huang', verbose=0, random_state = 0)

    kmodes = KModes(n_clusters=n_clusters, init='Huang', verbose=0, random_state = 0)
    clusters = kmodes.fit_predict(X)
    
    if (extended_information):
        reduce_dimension_after_clustering(clusters, n_clusters, 'K-Modes')
        f1_score(clusters)
        rate(df, clusters, 'K-Modes')
        
    return {"K-Modes": max_silhouette}
    

def kprototypes(df_numerical, df, extended_information):
    data = df.drop(columns = ['Diagnóstico'])
    data_numerical = df_numerical.drop(columns = ['Diagnóstico'])
    categories_numbers = [data.columns.get_loc(col) for col in 
                          categorical_columns]
    
    X = data.to_numpy()
    [n_clusters,max_silhouette] = silhouette("K-Prototypes", data_numerical, X, None, 
                                            None, KPrototypes, categories_numbers, 
                                            extended_information,
                                             init='Huang', verbose=0, random_state = 0)

 
    kproto = KPrototypes(n_clusters=n_clusters, init='Huang', verbose=0, random_state = 0)
    clusters = kproto.fit_predict(X, categorical=categories_numbers)
    
    if(extended_information):
        reduce_dimension_after_clustering(clusters, n_clusters, 'K-Prototype')
        f1_score(clusters)
        
        rate(df, clusters, 'K-Prototype')
    return {"K-Prototypes": max_silhouette}
    