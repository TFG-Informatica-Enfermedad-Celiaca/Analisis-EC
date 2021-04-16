# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 17:19:35 2021

@author: Carla
@auhor: pablo
"""

from sklearn.cluster import SpectralClustering
import sys
sys.path.append(r'../')
from reduceDimension import reduce_dimension_after_clustering
from scoreF1 import f1_score
from rater import rate

from silhouette import silhouette
from sklearn import metrics

def spectral(df, extended_information):
    data = df.drop(columns = ['Diagnóstico'])
    
    [n_clusters,max_silhouette] = silhouette("Spectral", data, None, None, None, 
                            SpectralClustering, None, extended_information, random_state=42,
                            affinity="nearest_neighbors", n_neighbors=10)
    X = data.to_numpy()
    spectral = SpectralClustering(n_clusters= n_clusters, 
        random_state=42, affinity="nearest_neighbors", n_neighbors=10)
    clusters = spectral.fit_predict(X)

    if (extended_information):
        reduce_dimension_after_clustering(clusters, n_clusters, 'Spectral')
        f1_score(clusters)
    
        rate(df, clusters, 'Spectral')
    
    df['cluster'] = clusters
    df_con_diagnostico = df[df['Diagnóstico']!= "Sin diagnóstico"]
    labels_true = df_con_diagnostico['Diagnóstico'].values
    labels_pred = df_con_diagnostico['cluster'].values
    
    return {"Spectral": [max_silhouette, metrics.homogeneity_completeness_v_measure(labels_true, labels_pred)]}
