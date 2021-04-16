# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 14:11:27 2021

@author: Carla
@author: pablo
"""

from kPOD import k_pod
import sys
sys.path.append(r'../')
from reduceDimension import reduce_dimension_after_clustering
from scoreF1 import f1_score
from rater import rate

from tqdm import tqdm
from sklearn.metrics import silhouette_score
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default='browser'
import numpy as np
from silhouette import silhouette

def kpod(df_complete, df):
    data = df.drop(columns = ['Diagnóstico'])
    data_complete = df_complete.drop(columns =['Diagnóstico'])
    
    X = data.to_numpy()
    
    [n_clusters,max_silhouette] = silhouette("K-POD", data_complete, None, None, 
                                             X, k_pod, None)

    clustered_data = k_pod(X, n_clusters)    
    # save the cluster assignments and centers
    cluster_assignments = clustered_data[0]
    
    #reduce_dimension_after_clustering(cluster_assignments, n_clusters, 'K-POD')
    #f1_score(cluster_assignments)

    #rate(df, cluster_assignments, 'K-POD')
    
    return {"K-POD": max_silhouette}

    