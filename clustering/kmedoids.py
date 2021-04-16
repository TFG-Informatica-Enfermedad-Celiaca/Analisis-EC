# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 11:58:12 2021

@author: pablo
@author: Carla
"""

import plotly.io as pio
pio.renderers.default='browser'
import sys
sys.path.append(r'../')
from reduceDimension import reduce_dimension_after_clustering
from scoreF1 import f1_score
from sklearn_extra.cluster import KMedoids
from rater import rate
from silhouette import silhouette

def kmedoids (df):
    data = df.drop(columns = ['Diagnóstico'])
    
    for metr in ['manhattan', 'euclidean', 'cosine']:
        n_clusters = silhouette("K-Medoids "+ metr, data, KMedoids, 
                                metric=metr, init='heuristic', random_state= 0, 
                                max_iter=1000)
        
        kmedoids = KMedoids(n_clusters=n_clusters,
                            metric=metr, init='heuristic', random_state= 0, 
                                max_iter=1000)
        
        kmedoids = kmedoids.fit(data)
        
        reduce_dimension_after_clustering(kmedoids.labels_, n_clusters, 
                                          'K-Medoids '+metr)
        f1_score(kmedoids.labels_)
        
        rate(df, kmedoids.labels_, 'K-Medoids '+metr)
   
    