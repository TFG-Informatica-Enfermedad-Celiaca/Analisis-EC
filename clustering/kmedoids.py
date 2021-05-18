# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 11:58:12 2021

@author: pablo
@author: Carla
"""

import plotly.io as pio
pio.renderers.default='browser'
import sys
sys.path.append(r'../')
from reduceDimension import reduce_dimension_after_clustering
from scoreF1 import f1_score
from sklearn_extra.cluster import KMedoids
from rater import rate
from silhouette import silhouette
from sklearn import metrics
import b3

def kmedoids (df, extended_information, name):
    data = df.drop(columns = ['Diagnóstico'])
    
    max_silh_dict = {}
    
    #He quitado las distancias manhattan y euclidean porque pasa algo raro con silhoutte
    #for metr in ['manhattan', 'euclidean', 'cosine']:
    for metr in ['euclidean']:
        
        [n_clusters,max_silhouette] = silhouette("K-Medoids "+ metr + name, data, 
                                None, None, None, KMedoids, None, extended_information, 
                                metric=metr, init='heuristic', random_state= 0, 
                                max_iter=1000)
        
        kmedoids = KMedoids(n_clusters=n_clusters,
                            metric=metr, init='heuristic', random_state= 0, 
                                max_iter=1000)
        
        clusters = kmedoids.fit_predict(data)
        
        
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
        
        
        max_silh_dict["K-Medoids - " + metr + name] = []
        max_silh_dict["K-Medoids - " + metr + name].append(max_silhouette)
        max_silh_dict["K-Medoids - " + metr + name].append(b3.calc_b3(labels_true, labels_pred))
        
        if (extended_information):
            #reduce_dimension_after_clustering(clusters, n_clusters, 
            #                                  'K-Medoids '+ metr + name)
            #f1_score(clusters)
            rate(df, clusters, 'K-Medoids '+ metr + name, max_silhouette, b3.calc_b3(labels_true, labels_pred))
            
    return max_silh_dict
