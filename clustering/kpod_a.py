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

def kpod(df):
    data = df.drop(columns = ['Diagnóstico'])
    
    X = data.to_numpy()
    N_CLUSTER = 2
    clustered_data = k_pod(X, N_CLUSTER)

    # save the cluster assignments and centers
    cluster_assignments = clustered_data[0]
    
    reduce_dimension_after_clustering(cluster_assignments, N_CLUSTER, 'K-POD')
    f1_score(cluster_assignments)

    rate(df, cluster_assignments, 'K-POD')
