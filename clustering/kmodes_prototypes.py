# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 12:08:08 2021

@author: Carla
@author: pablo
"""

from kmodes.kmodes import KModes
from kmodes.kprototypes import KPrototypes
from tqdm import tqdm
from sklearn.metrics import silhouette_score
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default='browser'
import numpy as np
import sys
sys.path.append(r'../')
from reduceDimension import reduce_dimension_after_clustering
from scoreF1 import f1_score
from rater import rate
from utils import categorical_columns
from silhouette import silhouette
from sklearn import metrics
import b3

def kmodes(df_numerical, df, extended_information, name=''):
    data = df.drop(columns = ['Diagnóstico'])
    data_numerical = df_numerical.drop(columns = ['Diagnóstico'])
    
    X = data.to_numpy()

    [n_clusters,max_silhouette] = silhouette("K-Modes" + name, data_numerical, None, X,None, 
                                    KModes,None,extended_information, init='Huang', verbose=0, random_state = 0)

    kmodes = KModes(n_clusters=n_clusters, init='Huang', verbose=0, random_state = 0)
    clusters = kmodes.fit_predict(X)
    
    df['cluster'] = clusters
    df_con_diagnostico = df[df['Diagnóstico']!= "Sin diagnostico"]
    df_con_diagnostico = df[df['Diagnóstico']!= "Paciente perdido"]
    df_con_diagnostico = df[df['Diagnóstico']!= "Aún en estudio"]
        
    df_con_diagnostico.loc[(df_con_diagnostico['Diagnóstico']
                       == "EC") | (df_con_diagnostico['Diagnóstico']
                       == "EC Potencial") | (df_con_diagnostico['Diagnóstico']
                       == "EC Refractaria") | (df_con_diagnostico['Diagnóstico']
                       == "EC dudosa"), 'Diagnóstico'] = "EC"
                                               
    df_con_diagnostico.loc[(df_con_diagnostico['Diagnóstico']
                       == "no EC ni SGNC") | (df_con_diagnostico['Diagnóstico']
                       == "SGNC no estricta") | (df_con_diagnostico['Diagnóstico']
                       == "Sensibilidad al gluten no celíaca (SGNC) estricta") 
                        , 'Diagnóstico'] = "no EC"   
                                                     
    labels_true = df_con_diagnostico['Diagnóstico'].values
    labels_pred = df_con_diagnostico['cluster'].values
    
    if (extended_information):
        #reduce_dimension_after_clustering(clusters, n_clusters, 'K-Modes'+name)
        #f1_score(clusters)
        rate(df, clusters, 'K-Modes'+name, max_silhouette,  b3.calc_b3(labels_true, labels_pred))
    
    return {"K-Modes"+name: [max_silhouette,  b3.calc_b3(labels_true, labels_pred)]}
    

def kprototypes(df_numerical, df, index, extended_information, name=''):
    data = df.drop(columns = ['Diagnóstico'])
    data_numerical = df_numerical.drop(columns = ['Diagnóstico'])
    categories_numbers = [data.columns.get_loc(col) for col in 
                          categorical_columns[str(index)]]
    
    X = data.to_numpy()
    [n_clusters,max_silhouette] = silhouette("K-Prototypes"+name, data_numerical, X, None, 
                                            None, KPrototypes, categories_numbers, 
                                            extended_information,
                                             init='Huang', verbose=0, random_state = 0)

 
    kproto = KPrototypes(n_clusters=n_clusters, init='Huang', verbose=0, random_state = 0)
    clusters = kproto.fit_predict(X, categorical=categories_numbers)
    
    df['cluster'] = clusters
    df_con_diagnostico = df[df['Diagnóstico']!= "Sin diagnostico"]
    df_con_diagnostico = df[df['Diagnóstico']!= "Paciente perdido"]
    df_con_diagnostico = df[df['Diagnóstico']!= "Aún en estudio"]
        
    df_con_diagnostico.loc[(df_con_diagnostico['Diagnóstico']
                       == "EC") | (df_con_diagnostico['Diagnóstico']
                       == "EC Potencial") | (df_con_diagnostico['Diagnóstico']
                       == "EC Refractaria") | (df_con_diagnostico['Diagnóstico']
                       == "EC dudosa"), 'Diagnóstico'] = "EC"
                                               
    df_con_diagnostico.loc[(df_con_diagnostico['Diagnóstico']
                       == "no EC ni SGNC") | (df_con_diagnostico['Diagnóstico']
                       == "SGNC no estricta") | (df_con_diagnostico['Diagnóstico']
                       == "Sensibilidad al gluten no celíaca (SGNC) estricta") 
                        , 'Diagnóstico'] = "no EC"   
                                                     
    labels_true = df_con_diagnostico['Diagnóstico'].values
    labels_pred = df_con_diagnostico['cluster'].values
    
    if(extended_information):
        #reduce_dimension_after_clustering(clusters, n_clusters, 'K-Prototype'+name)
        #f1_score(clusters)
        rate(df, clusters, 'K-Prototype'+name, max_silhouette, b3.calc_b3(labels_true, labels_pred))
    
    return {"K-Prototypes" + name: [max_silhouette, b3.calc_b3(labels_true, labels_pred)]}
    