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
from scoreF1 import f1_score
from sklearn.cluster import OPTICS
from rater import rate
from sklearn.metrics import silhouette_score
from sklearn import metrics
import b3

def optics (df, extended_information, name):
    data = df.drop(columns = ['Diagnóstico'])
     
    opt = OPTICS(min_samples=2, xi=0.006, min_cluster_size=0.02).fit(data)
   
    clusters = opt.fit_predict(data)

    if (extended_information):
        rate(df, clusters, 'Optics' + name)
        f1_score(clusters)
        aux = len(np.unique(opt.labels_))
        reduce_dimension_after_clustering(clusters, aux, 'Optics' + name)
    
    df['cluster'] = clusters
    df_con_diagnostico = df[df['Diagnóstico']!= "Sin diagnóstico"]
    labels_true = df_con_diagnostico['Diagnóstico'].values
    labels_pred = df_con_diagnostico['cluster'].values
    
    return {"Optics" + name: [silhouette_score(data, opt.labels_), 
                       b3.calc_b3(labels_true, labels_pred)]}
    