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
    
    #Manhattan and cosine do not work correctly
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
                                               
        labels_true = df_con_diagnostico['Diagnóstico'].values
        labels_pred = df_con_diagnostico['cluster'].values
        
        
        max_silh_dict["K-Medoids - " + metr + name] = []
        max_silh_dict["K-Medoids - " + metr + name].append(max_silhouette)
        max_silh_dict["K-Medoids - " + metr + name].append(b3.calc_b3(labels_true, labels_pred))
        
        if (extended_information):
            reduce_dimension_after_clustering('K-Medoids '+ metr + name, df)
            rate(df, clusters, 'K-Medoids '+ metr + name, max_silhouette, b3.calc_b3(labels_true, labels_pred))
            
    return max_silh_dict
