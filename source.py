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
from plotly.subplots import make_subplots

def fill_dict(clustering, silhouette, f_measure, precision, recall):
    for cluster_method in clustering:
        for key in cluster_method.keys():
            silhouette[key] = cluster_method[key][0]
            f_measure[key] = cluster_method[key][1][0]
            precision[key] = cluster_method[key][1][1]
            recall[key] = cluster_method[key][1][2]
    return [silhouette, f_measure, precision, recall]

def main():
    [df_numerical, df_numerical_short,df_missing, df_mix, df_categorical] = preprocess()
    
    for df in [df_numerical, df_numerical_short] :
        hopkins_test(df)
    
    #reduce_dimension_global_data_plotly()
    clustering = []
    
    silhouette = {}
    f_measure = {}
    precision = {}
    recall = {}
    
    clustering.append(kmeans(df_numerical, False))
    clustering.append(kmeans(df_numerical_short, False, "/ Short data"))
    clustering.append(kpod(df_numerical, df_missing, False))
    #clustering.append(kprototypes(df_numerical, df_mix, False))
    clustering.append(kmodes(df_numerical, df_categorical, False))
    clustering.append(spectral(df_numerical, False))
    clustering.append(agglomerative(df_numerical, False))
    clustering.append(dbscan(df_numerical, False))
    clustering.append(optics(df_numerical, False))
    clustering.append(kmedoids(df_numerical, False))
    
    [silhouette, f_measure, precision, recall] = fill_dict(
        clustering, silhouette,f_measure, precision, recall)

    silhouette = dict(sorted(silhouette.items(), key=lambda item: item[1], reverse=True))
    
    fig = make_subplots(
    rows=2, cols=1,
    shared_xaxes=True,
    vertical_spacing=0.03,
    specs=[[{"type": "table"}],
           [{"type": "table"}]]
    )
    
    fig.add_trace(
    go.Table(
        header=dict(
            values=[['<b>Algoritmo</b>'],
                  ['<b>Coeficiente de Silhouette</b>']]
        ),
        cells=dict(
            values=[np.array(list(silhouette.keys())), np.array(list(silhouette.values()))],
            align = "left")
    ),
    row=1, col=1
    )
    
    fig.add_trace(
    go.Table(
        header=dict(
            values=[['<b>Algoritmo</b>'],
                  ['<b>Valor-F</b>'],['<b>Precisión</b>'],['<b>Exhaustividad</b>']]
        ),
        cells=dict(
            values=[np.array(list(f_measure.keys())), 
                                        np.array(list(f_measure.values())), 
                                        np.array(list(precision.values())), 
                                        np.array(list(recall.values()))],
            align = "left")
    ),
    row=2, col=1
    )

    fig.update_layout(
    title_text="Evaluación de los métodos de clustering",
    height=800,
    )
    fig.show()

if __name__ == "__main__":
    main()