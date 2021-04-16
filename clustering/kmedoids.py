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

def kmedoids (df, extended_information):
    data = df.drop(columns = ['Diagnóstico'])
    
    max_silh_dict = {}
    for metr in ['manhattan', 'euclidean', 'cosine']:
        [n_clusters,max_silhouette] = silhouette("K-Medoids "+ metr, data, 
                                None, None, None, KMedoids, None, extended_information, 
                                metric=metr, init='heuristic', random_state= 0, 
                                max_iter=1000)
        
        kmedoids = KMedoids(n_clusters=n_clusters,
                            metric=metr, init='heuristic', random_state= 0, 
                                max_iter=1000)
        
        kmedoids = kmedoids.fit(data)
        if (extended_information):
            reduce_dimension_after_clustering(kmedoids.labels_, n_clusters, 
                                              'K-Medoids '+metr)
            f1_score(kmedoids.labels_)
            
            rate(df, kmedoids.labels_, 'K-Medoids '+metr)

        max_silh_dict["K-Medoids - " + metr] = max_silhouette
   
    return max_silh_dict
