# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 11:58:12 2021

@author: pablo
@author: Carla
"""

import plotly.io as pio
import numpy as np
pio.renderers.default='browser'
import sys
sys.path.append(r'../')
from reduceDimension import reduce_dimension_after_clustering
from sklearn.cluster import OPTICS
from rater import rate
from sklearn.metrics import silhouette_score
from sklearn import metrics
import b3

def optics (df, extended_information, name):
    data = df.drop(columns = ['Diagnóstico'])
     
    opt = OPTICS(min_samples=2, xi=0.006, min_cluster_size=0.02).fit(data)
   
    clusters = opt.fit_predict(data)

    df['cluster'] = clusters
    df_con_diagnostico = df[df['Diagnóstico']!= "Sin diagnostico"]
    df_con_diagnostico = df[df['Diagnóstico']!= "Paciente perdido"]
    df_con_diagnostico = df[df['Diagnóstico']!= "Aún en estudio"]
    
                             
    labels_true = df_con_diagnostico['Diagnóstico'].values
    labels_pred = df_con_diagnostico['cluster'].values
    
    if len(np.unique(opt.labels_)) >= 2 :
            silhouette_s = silhouette_score(data, opt.labels_)
    else:
            silhouette_s= -1
            
    if (extended_information):
        rate(df, clusters, 'Optics' + name, silhouette_s, 
                       b3.calc_b3(labels_true, labels_pred))
        reduce_dimension_after_clustering('Optics' + name, df)
    
    return {"Optics" + name: [silhouette_s, 
                       b3.calc_b3(labels_true, labels_pred)]}
    