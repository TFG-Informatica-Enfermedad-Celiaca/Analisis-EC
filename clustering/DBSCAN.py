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
from sklearn.cluster import DBSCAN
#from sklearn.decomposition import PCA
from matplotlib import pyplot as plt
import sklearn as sklearn
from sklearn.neighbors import kneighbors_graph
from rater import rate
from sklearn.metrics import silhouette_score
from sklearn import metrics
import b3
import numpy as np

def dbscan (df, extended_information, name):
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
    
    df['cluster'] = clusters
    df_con_diagnostico = df[df['Diagnóstico']!= "Sin diagnostico"]
    df_con_diagnostico = df[df['Diagnóstico']!= "Paciente perdido"]
    df_con_diagnostico = df[df['Diagnóstico']!= "Aún en estudio"]
                                                
    labels_true = df_con_diagnostico['Diagnóstico'].values
    labels_pred = df_con_diagnostico['cluster'].values
    
    if len(np.unique(db.labels_)) >= 2 :
            silhouette_s = silhouette_score(data, db.labels_)
    else:
            silhouette_s= -1
            
    if (extended_information):
        reduce_dimension_after_clustering('DBSCAN' + name, df)
        rate(df, clusters, 'DBSCAN' + name,silhouette_s ,
                   b3.calc_b3(labels_true, labels_pred))  
        
    
    return {"DBScan" + name: [silhouette_s ,
                       b3.calc_b3(labels_true, labels_pred)]}