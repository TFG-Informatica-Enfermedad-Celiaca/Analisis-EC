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
from skfeature.function.statistical_based.CFS import cfs
from skfeature.function.information_theoretical_based.FCBF import fcbf

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
        clustering.append(kmeans(numericals_dfs[i], False, titles_dfs[i]))
    return clustering

def executeKPod(clustering, numericals_dfs, missings_dfs, titles_dfs):
    for i in range(len(missings_dfs)) :
        clustering.append(kpod(numericals_dfs[i], missings_dfs[i], False, titles_dfs[i]))
    return clustering

def executeKPrototypes(clustering, numericals_dfs, mixs_dfs, titles_dfs):
    for i in range(len(mixs_dfs)) :
        clustering.append(kprototypes(numericals_dfs[i], mixs_dfs[i], i, False, titles_dfs[i]))
    return clustering

def executeKModes(clustering, numericals_dfs, categoricals_dfs, titles_dfs):
    for i in range(len(categoricals_dfs)):
        if (i > 5):
            clustering.append(kmodes(numericals_dfs[i], categoricals_dfs[i], False, titles_dfs[i]))
        else:
            clustering.append(kmodes(numericals_dfs[2*i], categoricals_dfs[i], False, titles_dfs[i]))
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
    fig.update_layout(width=500, height=1000, title="Estadístico de Hopkins")
    fig.show()
    
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
    
    #PRUEBA DE CONCEPTO
    '''
    numerical_df = numericals_dfs[0].drop(numericals_dfs[0][(numericals_dfs[0]['Diagnóstico'] != 'EC') &
                    (numericals_dfs[0]['Diagnóstico'] != 'no EC ni SGNC') ].index)
    
    missing_df = missings_dfs[0].drop(missings_dfs[0][(missings_dfs[0]['Diagnóstico'] != 'EC') &
                    (missings_dfs[0]['Diagnóstico'] != 'no EC ni SGNC')].index)
    
    categorical_df = categoricals_dfs[0].drop(categoricals_dfs[0][(categoricals_dfs[0]['Diagnóstico'] != 'EC') &
                    (categoricals_dfs[0]['Diagnóstico'] != 'no EC ni SGNC')].index)
    
    filter_col = [col for col in numerical_df if (col.startswith('HLA: grupos de riesgo') |
                    col.startswith('DCG EMA') | col.startswith('DSG EMA') |
                    col.startswith('Biopsia DCG') | col.startswith('Biopsia DSG'))]
    
    numerical_df = numerical_df.filter(filter_col +['DCG_ATG2_VALUE', 'DCG A-PDG_VALUE', 'DSG ATG2 VALUE', 
        'DSG A-PDG VALUE', 'LIEs DCG %GD', 'LIEs DCG %iNK', 'LIEs DSG %GD', 'LIEs DSG %iNK', 'Diagnóstico'])
    
    missing_df = missing_df.filter(filter_col +['DCG_ATG2_VALUE', 'DCG A-PDG_VALUE', 'DSG ATG2 VALUE', 
        'DSG A-PDG VALUE', 'LIEs DCG %GD', 'LIEs DCG %iNK', 'LIEs DSG %GD', 'LIEs DSG %iNK', 'Diagnóstico'])
    
    categorical_df = categorical_df.filter(['DCG_ATG2', 'DCG A-PDG', 'DSG ATG2', 
        'DSG A-PDG', 'Valoracion LIEs DCG', 'Valoracion LIEs DSG','Biopsia DCG','Biopsia DSG',
        'DCG EMA','DSG EMA  ','Diagnóstico', 'HLA: grupos de riesgo'])
    '''
    
    
    #KMEANS
    clustering_method_results.append(
        executeKMeans(clustering, numericals_dfs, titles_dfs))
    
    
    #KPOD
    clustering = []
    clustering_method_results.append(
        executeKPod(clustering, numericals_dfs, missings_dfs, titles_dfs))
    
    '''
    #KPrototypes
    clustering = []
    clustering_method_results.append(
        executeKPrototypes(clustering, numericals_dfs, mixs_dfs, titles_dfs))
    '''
    
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
    
    
    #Si se quiere hacer pruebas descomentar el array de abajo y ponerle el nombre de los metodos
    #title_methods = ["K-Prototypes"]
    
    for i in range(len(clustering_method_results)):
        silhouette = {}
        f_measure = {}
        precision = {}
        recall = {}
        [silhouette, f_measure, precision, recall] = fill_dict(
            clustering_method_results[i], silhouette,f_measure, precision, recall)
        #silhouette = dict(sorted(silhouette.items(), key=lambda item: item[1], reverse=True))
        plotResults(clustering_method_results[i], silhouette, f_measure, precision, recall, title_methods[i])
    
    
    '''
    final_clustering = []
    final_clustering = chooseFinalResult(final_clustering, numericals_dfs,
                      categoricals_dfs, mixs_dfs, missings_dfs, titles_dfs)
    
    '''
    

if __name__ == "__main__":
    main()