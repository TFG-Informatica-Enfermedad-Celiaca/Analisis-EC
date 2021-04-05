# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 11:58:12 2021

@author: pablo
@author: Carla
"""

import pandas as pd
import numpy as np
import plotly.io as pio
pio.renderers.default='browser'
import sys
sys.path.append(r'../')
from loadData import read_numerical_data_from_local
from reduceDimension import reduce_dimension_global_data_plotly, reduce_dimension_after_clustering
from scoreF1 import f1_score
from sklearn.cluster import DBSCAN
from sklearn.decomposition import PCA
from matplotlib import pyplot as plt
import sklearn as sklearn
from sklearn.neighbors import kneighbors_graph



def main ():
    
    reduce_dimension_global_data_plotly()
    full_data = read_numerical_data_from_local()
    data = full_data.drop(columns = ['Diagnóstico'])
    
    ## Parametrización de DBSCAN.
    estimator = PCA (n_components = 2)
    X_pca = estimator.fit_transform(data)
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
    plt.plot(seq)
    plt.show()
    

    db = DBSCAN(eps=0.7, min_samples=2, algorithm='auto').fit(data)
    clusters = db.fit_predict(data)
    aux = len(db.core_sample_indices_)
    
   
    
    reduce_dimension_after_clustering(clusters, aux)
                                
    f1_score(clusters)
    
    

    aux = pd.DataFrame()
    aux['Cluster']=clusters
    aux['Diagnóstico'] = full_data['Diagnóstico']
    print(aux)
    mostrar = pd.DataFrame()
    mostrar['result'] = aux.groupby(['Cluster', 'Diagnóstico']).size()
    print(mostrar)    
    
    
    
    
if __name__ == "__main__":
    main()
    