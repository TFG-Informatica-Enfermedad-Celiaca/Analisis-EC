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
from sklearn.cluster import DBSCAN
#from sklearn.decomposition import PCA
from matplotlib import pyplot as plt
import sklearn as sklearn
from sklearn.neighbors import kneighbors_graph
from rater import rate
from sklearn.metrics import silhouette_score

def dbscan (df, extended_information):
    data = df.drop(columns = ['Diagnóstico'])
    
    ## Parametrización de DBSCAN.
    #estimator = PCA (n_components = 2)
    #X_pca = estimator.fit_transform(data)
    X_pca = data
    dist = sklearn.neighbors.DistanceMetric.get_metric('euclidean')
    matsim = dist.pairwise(X_pca)
    minPts  = 2 # Fijamos el parámetro minPts
    A = kneighbors_graph(X_pca, minPts, include_self=False)
    Ar = A.toarray()
    seq = []
    for i,s in enumerate(X_pca):
        for j in range(len(X_pca)):
            if Ar[i][j] != 0:
                seq.append(matsim[i][j])
    seq.sort()
    if (extended_information):
        plt.plot(seq)
        plt.show()
    

    db = DBSCAN(eps=0.7, min_samples=2, algorithm='auto').fit(data)
    clusters = db.fit_predict(data)
    aux = len(db.core_sample_indices_)
   
    if (extended_information):
        reduce_dimension_after_clustering(clusters, aux, 'DBSCAN')
        f1_score(clusters)
        rate(df, clusters, 'DBSCAN')  
    
    return {"DBScan": silhouette_score(data, db.labels_)}