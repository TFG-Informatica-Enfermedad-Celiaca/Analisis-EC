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




def executeKMeans(clustering, numericals_dfs, titles_dfs):
    for i in range(len(numericals_dfs)) :
        clustering.append(kmeans(numericals_dfs[i], False, titles_dfs[i]))
    return clustering


def executeKPod(clustering, numericals_dfs, missings_dfs, titles_dfs):
    for i in range(len(numericals_dfs)) :
        clustering.append(kpod(numericals_dfs[i], missings_dfs[i], False, titles_dfs[i]))
    return clustering

def executeKPrototypes(clustering, numericals_dfs, mixs_dfs, titles_dfs):
    for i in range(len(numericals_dfs)) :
        clustering.append(kprototypes(numericals_dfs[i], mixs_dfs[0], False, titles_dfs[i]))
    return clustering

def executeKModes(clustering, numericals_dfs, categoricals_dfs, titles_dfs):
    for i in range(len(numericals_dfs)):
        clustering.append(kmodes(numericals_dfs[i], categoricals_dfs[i] ,False, titles_dfs[i]))
    return clustering

def executeSPECTRAL(clustering, numericals_dfs, titles_dfs):
    for i in range(len(numericals_dfs)):
        clustering.append(spectral(numericals_dfs[i],False, titles_dfs[i]))
    return clustering

def executeAgglomerative(clustering, numericals_dfs, titles_dfs):
    for i in range(len(numericals_dfs)):
        clustering.append(agglomerative(numericals_dfs[i], False, titles_dfs[i]))
    return clustering

def executeDBSCAN(clustering, numericals_dfs, titles_dfs):
    for i in range(len(numericals_dfs)):
        clustering.append(dbscan(numericals_dfs[i],False, titles_dfs[i]))
    return clustering

def executeOPTICS(clustering, numericals_dfs, titles_dfs):
    for i in range(len(numericals_dfs)):
        clustering.append(optics(numericals_dfs[i],False, titles_dfs[i]))
    return clustering

def executeMedoids(clustering, numericals_dfs, titles_dfs):
    for i in range(len(numericals_dfs)):
        clustering.append(kmedoids(numericals_dfs[i],False, titles_dfs[i]))
    return clustering


def plotResults(clustering, silhouette, f_measure, precision, recall, title):
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
    title_text = title,
    height=800,
    )
    fig.show()
    
    
def chooseFinalResult(final_clustering, numericals_dfs,
                      categoricals_dfs, mixs_dfs, missings_dfs, titles_dfs):

    final_clustering.append(kmeans(numericals_dfs[6], True, titles_dfs[6]))
    final_clustering.append(kpod(numericals_dfs[6], missings_dfs[6], True, titles_dfs[5]))
    
    #KProto fallaba
    ##final_clustering.
    
    final_clustering.append(kmodes(numericals_dfs[2], categoricals_dfs[2], True, titles_dfs[3]))
    final_clustering.append(spectral(numericals_dfs[7], True, titles_dfs[7]))
    
    #Agglomerative salen 4. Hay que quedarse con ward creo (no estoy seguro)
    final_clustering.append(agglomerative(numericals_dfs[7], True, titles_dfs[7]))
    
    

    return final_clustering


def main():
    [numericals_dfs ,missings_dfs, mixs_dfs, categoricals_dfs] = preprocess()
    
    
    
    #reduce_dimension_global_data_plotly()
    clustering = []
    
    silhouette = {}
    f_measure = {}
    precision = {}
    recall = {}
    clustering_method_results = []
    
    
    titles_dfs = ["", " Short data", " Sin país, sexo ni edad", 
                      " Sin país, sexo ni edad acortado", " Sin sintomas ni signos",
                      " Sin sintomas ni signos acortado",
                      " Sin país, sexo, edad, sintomas ni signos",
                      " Sin país, sexo, edad, sintomas ni signos acortado"]
    
    for i in range(len(titles_dfs)) :
        hopkins_test(numericals_dfs[i], titles_dfs[i])
    
    
    '''
    #KMEANS
    clustering_method_results.append(
        executeKMeans(clustering, numericals_dfs, titles_dfs))
    
    #KPOD
    clustering = []
    clustering_method_results.append(
        executeKPod(clustering, numericals_dfs, missings_dfs, titles_dfs))
    
    
    #KPrototypes
    clustering = []
    clustering_method_results.append(
        executeKPrototypes(clustering, numericals_dfs, mixs_dfs, titles_dfs))
    
    
    #KModes
    clustering = []
    clustering_method_results.append(
        executeKModes(clustering, numericals_dfs, categoricals_dfs, titles_dfs))
    
    
    #SPECTRAL
    clustering = []
    clustering_method_results.append(
        executeSPECTRAL(clustering, numericals_dfs, titles_dfs))
    
    
    #Agglomerative
    clustering = []
    clustering_method_results.append(
        executeAgglomerative(clustering, numericals_dfs, titles_dfs))
    
    
    #DBSCAN
    clustering = []
    clustering_method_results.append(
        executeDBSCAN(clustering, numericals_dfs, titles_dfs))
    
    
    #OPTICS
    clustering = []
    clustering_method_results.append(
        executeOPTICS(clustering, numericals_dfs, titles_dfs))
    
    
    #KMedoids
    clustering = []
    clustering_method_results.append(
        executeMedoids(clustering, numericals_dfs, titles_dfs))

    '''
    title_methods = ["K-Means", "K-POD", "K-Prototypes", "K-Modes",
                     "Spectral", "Agglomerative", "DBSCAN", "OPTICS", "K-Medoids"]
    
    '''
    #Si se quiere hacer pruebas descomentar el array de abajo y ponerle el nombre de los metodos
    #title_methods = ['KPrototype']
    
    for i in range(len(clustering_method_results)):
        silhouette = {}
        f_measure = {}
        precision = {}
        recall = {}
        [silhouette, f_measure, precision, recall] = fill_dict(
            clustering_method_results[i], silhouette,f_measure, precision, recall)
        silhouette = dict(sorted(silhouette.items(), key=lambda item: item[1], reverse=True))
        plotResults(clustering_method_results[i], silhouette, f_measure, precision, recall, title_methods[i])
    
    
    '''
    final_clustering = []
    final_clustering = chooseFinalResult(final_clustering, numericals_dfs,
                      categoricals_dfs, mixs_dfs, missings_dfs, titles_dfs)
    
    

    
    

if __name__ == "__main__":
    main()