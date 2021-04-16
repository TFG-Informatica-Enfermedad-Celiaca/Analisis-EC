# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 17:19:35 2021

@author: Carla
@auhor: pablo
"""

from sklearn.cluster import SpectralClustering
import sys
sys.path.append(r'../')
from reduceDimension import reduce_dimension_after_clustering, reduce_dimension_global_data_plotly
from scoreF1 import f1_score
from rater import rate
from tqdm import tqdm
from sklearn.metrics import silhouette_score
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default='browser'
import numpy as np

def spectral(df):
    data = df.drop(columns = ['Diagnóstico'])
    
    K_MAX = 20
    silhouette= []
    for i in tqdm(range(2, K_MAX)):
        spec = SpectralClustering(n_clusters=i, random_state=42, affinity="nearest_neighbors", n_neighbors=10) 
        spec.fit(data)
        labels = spec.labels_
        silhouette.append(silhouette_score(data, labels))
    
    n_clusters = silhouette.index(max(silhouette)) + 2
    
    fig = go.Figure(data=go.Scatter(x=np.arange(2,K_MAX), y=silhouette))
    fig.update_layout(title='Coeficiente de Silhouette Spectral',
                   xaxis_title='Número de clusters',
                   yaxis_title='Coeficiente de Silhouette')
    fig.show()
    
    
    X = data.to_numpy()
    N_CLUSTER = 2
    spectral = SpectralClustering(n_clusters= n_clusters, 
        random_state=42, affinity="nearest_neighbors", n_neighbors=10)
    clusters = spectral.fit_predict(X)

    
    reduce_dimension_after_clustering(clusters, N_CLUSTER, 'Spectral')
    f1_score(clusters)

    rate(df, clusters, 'Spectral')
