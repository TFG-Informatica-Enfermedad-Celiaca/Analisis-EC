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

def kmodes(df_numerical, df):
    data = df.drop(columns = ['Diagnóstico'])
    data_numerical = df_numerical.drop(columns = ['Diagnóstico'])
    
    X = data.to_numpy()

    n_clusters = silhouette(X, data_numerical, "K-Modes")

    kmodes = KModes(n_clusters=n_clusters, init='Huang', verbose=0, random_state = 0)
    clusters = kmodes.fit_predict(X)

    reduce_dimension_after_clustering(clusters, n_clusters, 'K-Modes')
    f1_score(clusters)
    
    
    rate(df, clusters, 'K-Modes')
    
def kprototypes(df_numerical, df):
    data = df.drop(columns = ['Diagnóstico'])
    data_numerical = df_numerical.drop(columns = ['Diagnóstico'])
    categories_numbers = [data.columns.get_loc(col) for col in 
                          categorical_columns]
    
    X = data.to_numpy()
    n_clusters = silhouette(X, data_numerical, "K-Prototypes")


    kproto = KPrototypes(n_clusters=n_clusters, init='Huang', verbose=0, random_state = 0)
    clusters = kproto.fit_predict(X, categorical=categories_numbers)

    reduce_dimension_after_clustering(clusters, n_clusters, 'K-Prototype')
    f1_score(clusters)
    
    
    rate(df, clusters, 'K-Prototype')
    
    
def silhouette(X, data_numerical, name):
    
    K_MAX = 20
    silhouette= []
    for i in tqdm(range(2, K_MAX)):
        kmodes = KModes(n_clusters=i, init='Huang', verbose=0, random_state = 0)
        labels = kmodes.fit_predict(X)

        if (len(np.unique(labels)) > 1):
            silhouette.append(silhouette_score(data_numerical, labels))
        else: 
            silhouette.append(-1)
    
    n_clusters = silhouette.index(max(silhouette)) + 2
    
    fig = go.Figure(data=go.Scatter(x=np.arange(2,K_MAX), y=silhouette))
    fig.update_layout(title='Coeficiente de Silhouette '+ name,
                   xaxis_title='Número de clusters',
                   yaxis_title='Coeficiente de Silhouette')
    fig.show()
    
    return n_clusters