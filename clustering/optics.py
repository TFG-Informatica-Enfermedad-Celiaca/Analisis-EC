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
from sklearn.cluster import OPTICS
from rater import rate

def optics (df):
    data = df.drop(columns = ['Diagnóstico'])
     
    opt = OPTICS(min_samples=2, xi=0.006, min_cluster_size=0.02)
   
    clusters = opt.fit_predict(data)

    rate(df, clusters)

    f1_score(clusters)
    
    