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



def agglomerative(df):
    data = df.drop(columns = ['Diagnóstico'])
    
    number_clusters = 6;

    for metric in ['ward', 'complete', 'average', 'single']:
        model = AgglomerativeClustering(
            n_clusters = number_clusters, affinity='euclidean', memory = None, connectivity = None,
            compute_full_tree='auto', linkage = metric, distance_threshold = None, 
            compute_distances=True)
            
        clusters = model.fit_predict(data)
        reduce_dimension_after_clustering(clusters, number_clusters, 'Agglomerative ' + metric)
        f1_score(clusters)
        plot_dendrogram(model, truncate_mode='level', p=number_clusters)
        plt.title(metric)
        plt.xlabel("Number of points in node (or index of point if no parenthesis).")
        plt.show()
        
        rate(df, clusters, 'Agglomerative '+metric)
        
        
        
        
        