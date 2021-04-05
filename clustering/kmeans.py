# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 11:44:41 2021

@author: Carla
"""

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default='browser'
from tqdm import tqdm
#import sys
import numpy as np
#sys.path.append(r'../')
from reduceDimension import reduce_dimension_after_clustering
from scoreF1 import f1_score

def kmeans (df):
    data = df.drop(columns = ['Diagnóstico'])

    K_MAX = 20
    silhouette= []
    for i in tqdm(range(2, K_MAX)):
        kmeans = KMeans(n_clusters=i, init='random', n_init=1, random_state=0, max_iter=1000) 
        kmeans.fit(data)
        labels = kmeans.labels_
        silhouette.append(silhouette_score(data, labels))
    
    n_clusters = silhouette.index(max(silhouette)) + 2
    
    fig = go.Figure(data=go.Scatter(x=np.arange(2,K_MAX), y=silhouette))
    fig.update_layout(title='Coeficiente de Silhouette KMeans',
                   xaxis_title='Número de clusters',
                   yaxis_title='Coeficiente de Silhouette')
    fig.show()
    
    kmeans = KMeans(n_clusters=n_clusters, init='random', n_init=1, random_state=0, max_iter=1000) 
    kmeans.fit(data)
    
    reduce_dimension_after_clustering(kmeans.labels_, n_clusters)
    f1_score(kmeans.labels_)
