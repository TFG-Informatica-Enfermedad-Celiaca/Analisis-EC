# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 10:18:11 2021

@author: Carla
@author: pablo
"""
from tqdm import tqdm
from sklearn.metrics import silhouette_score
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default='browser'
import numpy as np

def silhouette(name, data, cluster_prod, **kwargs):
    
    K_MAX = 20
    silhouette= []
    for i in tqdm(range(2, K_MAX)):
        spec = cluster_prod(i, **kwargs) 
        spec.fit(data)
        labels = spec.labels_

        if (len(np.unique(labels)) > 1):
            silhouette.append(silhouette_score(data, labels))
        else: 
            silhouette.append(-1)
    
    n_clusters = silhouette.index(max(silhouette)) + 2
    
    fig = go.Figure(data=go.Scatter(x=np.arange(2,K_MAX), y=silhouette))
    fig.update_layout(title='Coeficiente de Silhouette ' + name,
                   xaxis_title='Número de clusters',
                   yaxis_title='Coeficiente de Silhouette')
    fig.show()
    
    return n_clusters