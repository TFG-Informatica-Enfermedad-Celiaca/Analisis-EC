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
from hopkins_statistics import hopkins_test
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default='browser'
import numpy as np
from plotly.subplots import make_subplots
from skfeature.function.statistical_based.CFS import cfs
from skfeature.function.information_theoretical_based.FCBF import fcbf
import os

if not os.path.exists(r"images"):
    os.mkdir("images")
    
def fill_dict(clustering, silhouette, f_measure, precision, recall):
    for cluster_method in clustering:
        for key in cluster_method.keys():
            silhouette[key] = round(cluster_method[key][0], 3)
            f_measure[key] = round(cluster_method[key][1][0], 3)
            precision[key] = round(cluster_method[key][1][1], 3)
            recall[key] = round(cluster_method[key][1][2], 3)
    return [silhouette, f_measure, precision, recall]


def executeKMeans(clustering, numericals_dfs, titles_dfs):
    for i in range(len(numericals_dfs)) :
        clustering.append(kmeans(numericals_dfs[i], True, titles_dfs[i]))
    return clustering

def executeKPod(clustering, numericals_dfs, missings_dfs, titles_dfs):
    for i in range(len(missings_dfs)) :
        clustering.append(kpod(numericals_dfs[i], missings_dfs[i], True, titles_dfs[i]))
    return clustering

def executeKPrototypes(clustering, numericals_dfs, mixs_dfs, titles_dfs):
    for i in range(len(mixs_dfs)) :
        clustering.append(kprototypes(numericals_dfs[i], mixs_dfs[i], i, True, titles_dfs[i]))
    return clustering

def executeKModes(clustering, numericals_dfs, categoricals_dfs, titles_dfs):
    for i in range(len(categoricals_dfs)):
        if (i > 5):
            clustering.append(kmodes(numericals_dfs[i], categoricals_dfs[i], True, titles_dfs[i]))
        else:
            clustering.append(kmodes(numericals_dfs[2*i], categoricals_dfs[i], True, titles_dfs[i]))
    return clustering

def executeSPECTRAL(clustering, numericals_dfs, titles_dfs):
    for i in range(len(numericals_dfs)):
        clustering.append(spectral(numericals_dfs[i],True, titles_dfs[i]))
    return clustering

def executeAgglomerative(clustering, numericals_dfs, titles_dfs):
    for i in range(len(numericals_dfs)):
        clustering.append(agglomerative(numericals_dfs[i], True, titles_dfs[i]))
    return clustering

def executeDBSCAN(clustering, numericals_dfs, titles_dfs):
    for i in range(len(numericals_dfs)):
        clustering.append(dbscan(numericals_dfs[i],True, titles_dfs[i]))
    return clustering

def executeOPTICS(clustering, numericals_dfs, titles_dfs):
    for i in range(len(numericals_dfs)):
        clustering.append(optics(numericals_dfs[i],True, titles_dfs[i]))
    return clustering

def executeMedoids(clustering, numericals_dfs, titles_dfs):
    for i in range(len(numericals_dfs)):
        clustering.append(kmedoids(numericals_dfs[i],True, titles_dfs[i]))
    return clustering


def plotResults(clustering, silhouette, f_measure, precision, recall, title):
    fig = go.Figure(data=[go.Table(
        columnwidth = [150,30, 30,30,40],
        header=dict(
            values=[['<b>Algoritmo</b>'], ['<b>Silhouette</b>'],
                  ['<b>Valor-F</b>'],['<b>Precisión</b>'],['<b>Exhaustividad</b>']]
        ),
        cells=dict(
            values=[np.array(list(f_measure.keys())), 
                                        np.array(list(silhouette.values())),
                                        np.array(list(f_measure.values())), 
                                        np.array(list(precision.values())), 
                                        np.array(list(recall.values()))],
            align = "left")
    )])
    fig.update_layout(width=1000, height=1000, title_text=title)
    fig.write_html("images/Resumen" + title + ".html")
    

def plot_hopkins(hopkins):
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=[['<b>Dataset</b>'],
                  ['<b>Estadístico de Hopkins</b>']]
        ),
        cells=dict(
            values=[np.array(list(hopkins.keys())), np.array(list(hopkins.values()))],
            align = "left")
    )])
    fig.update_layout(width=500, height=700, title="Estadístico de Hopkins")
    fig.write_html("images/Estadístico de Hopkins.html")
    
def main():
    [numericals_dfs ,missings_dfs, mixs_dfs, categoricals_dfs] = preprocess()
    
    #reduce_dimension_global_data_plotly()
    clustering = []
    
    silhouette = {}
    f_measure = {}
    precision = {}
    recall = {}
    hopkins_numeric = {}
    clustering_method_results = []
    
    
    titles_dfs = ["", " Acortado", " Sin país, sexo ni edad", 
                      " Sin país, sexo ni edad acortado", " Sin sintomas ni signos",
                      " Sin sintomas ni signos acortado",
                      " Sin país, sexo, edad, sintomas ni signos",
                      " Sin país, sexo, edad, sintomas ni signos acortado", 
                      " Elementos diagnósticos principales", 
                      " Selección atributos CFS", 
                      " Selección atributos FCBF"]
    titles_categorical_dfs = ["", " Sin país, sexo ni edad", 
                      " Sin sintomas ni signos", " Sin país, sexo, edad, sintomas ni signos", 
                      " Elementos diagnósticos principales", 
                      " Selección atributos CFS", 
                      " Selección atributos FCBF"]
    
    for i in range(len(titles_dfs)) :
        aux = hopkins_test(numericals_dfs[i], "Numérico-"+ titles_dfs[i])
        hopkins_numeric["Numérico-"+ titles_dfs[i]] = round(aux, 3)
        
    hopkins_numeric = dict(sorted(hopkins_numeric.items(), key=lambda item: item[1]))
    plot_hopkins(hopkins_numeric);    
    
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
        executeKModes(clustering, numericals_dfs, categoricals_dfs, titles_categorical_dfs))
    
    
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
    
    title_methods = ["K-Means", "K-POD", "K-Prototypes", "K-Modes",
                    "Spectral", "Agglomerative", "DBSCAN", "OPTICS", "K-Medoids"]
    
    for i in range(len(clustering_method_results)):
        silhouette = {}
        f_measure = {}
        precision = {}
        recall = {}
        [silhouette, f_measure, precision, recall] = fill_dict(
            clustering_method_results[i], silhouette,f_measure, precision, recall)
        
        plotResults(clustering_method_results[i], silhouette, f_measure, precision, recall, title_methods[i])
    
    

if __name__ == "__main__":
    main()