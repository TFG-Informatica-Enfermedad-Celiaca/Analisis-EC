# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 21:37:46 2021

@author: Carla
@author: pablo
"""
import sys
sys.path.append(r'./preprocessing')
sys.path.append(r'./clustering')
from preprocess import preprocess
from kmeans import kmeans
from kmodes_prototypes import kmodes, kprototypes
from kpod_a import kpod
from agglomerative import agglomerative
from DBSCAN import dbscan
from kmedoids import kmedoids
from optics import optics
from spectral import spectral
from reduceDimension import reduce_dimension_global_data_plotly
from hopkins_statistics import hopkins_test
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default='browser'
import numpy as np

def main():
    [df_numerical, df_numerical_short,df_missing, df_mix, df_categorical] = preprocess()
    
    for df in [df_numerical, df_numerical_short] :
        hopkins_test(df)
    
    #reduce_dimension_global_data_plotly()
    silhouette = {}
    c_kmeans = kmeans(df_numerical, False)
    for key in c_kmeans.keys():
        silhouette[key] = c_kmeans[key]
    
    c_kmeans2 = kmeans(df_numerical_short, False)
    for key in c_kmeans2.keys():
        silhouette[key + " 2"] = c_kmeans2[key]
    
    c_pod = kpod(df_numerical, df_missing, False)
    for key in c_pod.keys():
        silhouette[key] = c_pod[key]
        
    c_prototypes= kprototypes(df_numerical, df_mix, False)
    for key in c_prototypes.keys():
        silhouette[key] = c_prototypes[key]
        
    c_modes = kmodes(df_numerical, df_categorical, False)
    for key in c_modes.keys():
        silhouette[key] = c_modes[key]
    
    c_spec = spectral(df_numerical, False)
    for key in c_spec.keys():
        silhouette[key] = c_spec[key]
    
    c_aggl = agglomerative(df_numerical, False)
    for key in c_aggl.keys():
        silhouette[key] = c_aggl[key]
    
    c_dbscan = dbscan(df_numerical, False)
    for key in c_dbscan.keys():
        silhouette[key] = c_dbscan[key]
    
    c_optics = optics(df_numerical, False)
    for key in c_optics.keys():
        silhouette[key] = c_optics[key]
    
    c_kmedoids = kmedoids(df_numerical, False)
    for key in c_kmedoids.keys():
        silhouette[key] = c_kmedoids[key]
    
    
    silhouette = dict(sorted(silhouette.items(), key=lambda item: item[1], reverse=True))

    fig = go.Figure(data=[go.Table(header=dict(values=[['<b>Algoritmo</b>'],
                  ['<b>Coeficiente de Silhouette</b>']],),
                     cells=dict(values=[np.array(list(silhouette.keys())), np.array(list(silhouette.values()))]))
                         ])
    fig.show()

if __name__ == "__main__":
    main()