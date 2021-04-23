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
from kPOD import k_pod
from sklearn_extra.cluster import KMedoids

def silhouette(name, data, data_prototypes, data_modes, data_pod,
               cluster_prod,categories_numbers, extended_information,  **kwargs):
    
    K_MAX = 20
    silhouette= []
    for i in tqdm(range(2, K_MAX)):
        if (cluster_prod.__name__ == "KPrototypes"):
            kprot= cluster_prod(n_clusters=i, **kwargs)
            labels = kprot.fit_predict(data_prototypes, categorical=categories_numbers)
            
        elif (cluster_prod.__name__ == "KModes"):
            kmodes = cluster_prod(n_clusters=i, **kwargs)
            labels = kmodes.fit_predict(data_modes)
            
        elif(cluster_prod.__name__ == "k_pod"):
            spec = k_pod(data_pod,i) 
            labels = spec[0]
        elif(cluster_prod.__name__ == "k_medoids"):
            kmedoids = KMedoids(n_clusters=i, **kwargs).fit(data)
            labels = kmedoids.labels_
        else:
            algorithm = cluster_prod(i, **kwargs) 
            algorithm.fit(data)
            labels = algorithm.labels_

        if (len(np.unique(labels)) > 1):
            silhouette.append(silhouette_score(data, labels))
        else: 
            silhouette.append(-1)
    
    n_clusters = silhouette.index(max(silhouette)) + 2
    
    if (extended_information):
        fig = go.Figure(data=go.Scatter(x=np.arange(2,K_MAX), y=silhouette))
        fig.update_layout(title='Coeficiente de Silhouette ' + name,
                       xaxis_title='Número de clusters',
                       yaxis_title='Coeficiente de Silhouette')
        fig.show()
    
    return [n_clusters,max(silhouette)]
