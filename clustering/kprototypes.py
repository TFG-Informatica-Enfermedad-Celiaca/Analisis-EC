# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 11:58:12 2021

@author: pablo
@author: Carla
"""

import pandas as pd
from kmodes.kprototypes import KPrototypes
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default='browser'
from tqdm import tqdm
import sys
sys.path.append(r'../')
from utils import categorical_columns
from reduceDimension import reduce_dimension_after_clustering
from scoreF1 import f1_score
from rater import rate

def kprototypes(df):
    data = df.drop(columns = ['Diagnóstico'])

    categories_numbers = [data.columns.get_loc(col) for col in 
                          categorical_columns]
    
    X = data.to_numpy()
    #y = train_numpy[:, 0]
    
    K_MAX = 10
    #Elbow plot: must find the value at wich the cost starts decreasing in 
    # a lineal way
    costs = []
    n_clusters = []
    clusters_assigned = []
    
    for i in tqdm(range(2, K_MAX)):
        try:
            # The model will select the i first different elements 
            # in the dataset as centroids
            kproto = KPrototypes(n_clusters=i, init='Huang', verbose=0, random_state = 0)
            clusters = kproto.fit_predict(X, categorical=categories_numbers)
            # Cost is defined as the sum of the distance from all the points 
            # to the centroid
            costs.append(kproto.cost_)
            n_clusters.append(i)
            clusters_assigned.append(clusters)
        except:
            print(f"Can't cluster with {i} clusters")
            
    fig = go.Figure(data=go.Scatter(x=n_clusters, y=costs))
    fig.update_layout(title='Elbow plot',
                   xaxis_title='Número clusters',
                   yaxis_title='Suma distancias de cada punto a su centro')
    fig.show()
    
    N_CLUSTER = 4
    # When we see the Elbow plot it is clear that the elbow is in 4
    # So we are going to use n_cluster = 4
    kproto = KPrototypes(n_clusters=N_CLUSTER, init='Huang', verbose=0, random_state = 0)
    clusters = kproto.fit_predict(X, categorical=categories_numbers)

    reduce_dimension_after_clustering(clusters, N_CLUSTER, 'K-Prototive')
    f1_score(clusters)
    
    
    rate(df, clusters, 'K-Prototive')
    
    
