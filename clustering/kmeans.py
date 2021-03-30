# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 11:44:41 2021

@author: Carla
"""

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default='browser'
from tqdm import tqdm
import sys
import numpy as np
sys.path.append(r'../')
from loadData import read_numerical_data_from_local
from utils import final_columns_to_numeric, final_column_to_one_hot
from reduceDimension import reduce_dimension_global_data_plotly, reduce_dimension_after_clustering
from scoreF1 import f1_score

def main ():
    #reduce_dimension_global_data_plotly()
    full_data = read_numerical_data_from_local()
    data = full_data.drop(columns = ['Diagnóstico'])
    
    # As we know kmeans sufers from curse of dimensionality so before we run 
    # kmeans algorithm we are going to execute dimensionality reduction algorithm
    # PCA
    pca = PCA(n_components="mle", random_state=42)
    data = pca.fit_transform(data)
    K_MAX = 10
    silhouette= []
    for i in tqdm(range(2, K_MAX)):
        kmeans = KMeans(n_clusters=i, init='random', n_init=1, random_state=0, max_iter=1000) 
        kmeans.fit(data)
        labels = kmeans.labels_
        silhouette.append(silhouette_score(data, labels))
    
    n_clusters = silhouette.index(max(silhouette)) + 2
    
    fig = go.Figure(data=go.Scatter(x=np.arange(2,K_MAX), y=silhouette))
    fig.update_layout(title='Coeficiente de Silhouette KMeans',
                   xaxis_title='Número de clusters',
                   yaxis_title='Coeficiente de Silhouette')
    fig.show()
    
    kmeans = KMeans(n_clusters=n_clusters, init='random', n_init=1, random_state=0, max_iter=1000) 
    kmeans.fit(data)
    
    reduce_dimension_after_clustering(kmeans.labels_, n_clusters)
    f1_score(kmeans.labels_)
    
if __name__ == "__main__":
    main()
    