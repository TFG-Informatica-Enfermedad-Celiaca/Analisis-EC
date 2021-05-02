# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 11:58:12 2021

@author: pablo
@author: Carla
"""

import numpy as np
import plotly.io as pio
pio.renderers.default='browser'
import sys
sys.path.append(r'../')
from reduceDimension import reduce_dimension_global_data_plotly, reduce_dimension_after_clustering
from scoreF1 import f1_score
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram
from matplotlib import pyplot as plt
from rater import rate
from silhouette import silhouette
from sklearn import metrics
import b3

def plot_dendrogram(model, **kwargs):
    # Create linkage matrix and then plot the dendrogram

    # create the counts of samples under each node
    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1  # leaf node
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count

    linkage_matrix = np.column_stack([model.children_, model.distances_,
                                      counts]).astype(float)

    # Plot the corresponding dendrogram
    dendrogram(linkage_matrix, **kwargs)



def agglomerative(df, extended_information, name):
    data = df.drop(columns = ['Diagnóstico'])
    
    max_silh_dict = {}
    for metric in ['ward', 'complete', 'average', 'single']:
        [n_clusters,max_silhouette] = silhouette("Aglomerative " + metric + name, 
            data, None, None, None, AgglomerativeClustering, None, extended_information,
            affinity='euclidean', memory = None, connectivity = None,
            compute_full_tree='auto', linkage = metric, distance_threshold = None, 
            compute_distances=True)
        
        model = AgglomerativeClustering(
            n_clusters = n_clusters, affinity='euclidean', memory = None, connectivity = None,
            compute_full_tree='auto', linkage = metric, distance_threshold = None, 
            compute_distances=True)
            
        clusters = model.fit_predict(data)
        max_silh_dict["Agglomerative - " + metric + name]=[]
        max_silh_dict["Agglomerative - " + metric + name].append(max_silhouette)
        
        df['cluster'] = clusters
        df_con_diagnostico = df[df['Diagnóstico']!= "Sin diagnostico"]
        df_con_diagnostico = df[df['Diagnóstico']!= "Paciente perdido"]
        df_con_diagnostico = df[df['Diagnóstico']!= "Aún en estudio"]
        labels_true = df_con_diagnostico['Diagnóstico'].values
        labels_pred = df_con_diagnostico['cluster'].values
        
        max_silh_dict["Agglomerative - " + metric + name].append(b3.calc_b3(labels_true, labels_pred))
        if (extended_information):
            #reduce_dimension_after_clustering(clusters, n_clusters, 'Agglomerative ' + metric + name)
            #f1_score(clusters)
            #plot_dendrogram(model, truncate_mode='level', p=n_clusters)
            #plt.title(metric)
            #plt.xlabel("Number of points in node (or index of point if no parenthesis).")
            #plt.show()
            rate(df, clusters, 'Agglomerative '+metric + name, max_silhouette, b3.calc_b3(labels_true, labels_pred))  
        
    return max_silh_dict
        
        
        