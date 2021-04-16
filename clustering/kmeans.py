# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 11:44:41 2021

@author: Carla
"""
from sklearn.cluster import KMeans
#import sys
#sys.path.append(r'../')
from reduceDimension import reduce_dimension_after_clustering
from scoreF1 import f1_score
from rater import rate
from silhouette import silhouette

def kmeans (df, extended_information):
    data = df.drop(columns = ['Diagnóstico'])

    [n_clusters,max_silhouette]= silhouette("K-Means", data, None, None, None, 
                            KMeans, None, extended_information, init='random', n_init=1, 
                            random_state=0, max_iter=1000)
    
    kmeans = KMeans(n_clusters=n_clusters, init='random', n_init=1, random_state=0, max_iter=1000) 
    clusters = kmeans.fit_predict(data)
    
    if (extended_information):
        reduce_dimension_after_clustering(clusters, n_clusters, 'K-Means')
        f1_score(kmeans.labels_)
        rate(df, clusters, 'K-Means')

    return {"K-Means": max_silhouette}

