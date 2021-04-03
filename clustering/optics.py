# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 11:58:12 2021

@author: pablo
@author: Carla
"""

import pandas as pd
import numpy as np
import plotly.io as pio
pio.renderers.default='browser'
import sys
sys.path.append(r'../')
from loadData import read_numerical_data_from_local
from reduceDimension import reduce_dimension_global_data_plotly, reduce_dimension_after_clustering
from scoreF1 import f1_score
from sklearn.cluster import OPTICS





def main ():
    
    #reduce_dimension_global_data_plotly()
    full_data = read_numerical_data_from_local()
    data = full_data.drop(columns = ['Diagnóstico'])
     
    opt = OPTICS(min_samples=2, xi=0.006, min_cluster_size=0.02)
    
   
    clusters = opt.fit_predict(data)


    copy = pd.DataFrame()
    copy['label'] = clusters;
    cantidadGrupo =  pd.DataFrame()
    cantidadGrupo['cantidad']=copy.groupby('label').size()
    print(cantidadGrupo)
   
                                
    f1_score(clusters)
    
    
if __name__ == "__main__":
    main()
    