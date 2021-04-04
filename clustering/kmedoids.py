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
from sklearn_extra.cluster import KMedoids
from tqdm import tqdm
from sklearn.metrics import silhouette_score
import plotly.graph_objects as go







def main ():
    
    #reduce_dimension_global_data_plotly()
    full_data = read_numerical_data_from_local()
    data = full_data.drop(columns = ['Diagnóstico'])
     
    
    '''
    K_MAX = 20
    silhouette= []
    for i in tqdm(range(2, K_MAX)):
        kmedoids = KMedoids(n_clusters=i,
                        metric='euclidean', init='heuristic')
        kmedoids.fit(data)
        labels = kmedoids.labels_
        silhouette.append(silhouette_score(data, labels))
    
    fig = go.Figure(data=go.Scatter(x=np.arange(2,K_MAX), y=silhouette))
    fig.update_layout(title='Coeficiente de Silhouette KMeans',
                   xaxis_title='Número de clusters',
                   yaxis_title='Coeficiente de Silhouette')
    #fig.show()
    
    numberClustes = silhouette.index(max(silhouette)) + 2
    '''
    
    for metr in ['manhattan', 'euclidean', 'cosine']:
        numberClustes = 5
        kmedoids = KMedoids(n_clusters=numberClustes,
                            metric=metr, init='heuristic')
        
        kmedoids = kmedoids.fit(data)
        
        reduce_dimension_after_clustering(kmedoids.labels_, numberClustes)
        f1_score(kmedoids.labels_)
        
        
        
        aux = pd.DataFrame()
        aux['Cluster']=kmedoids.labels_
        aux['Diagnóstico'] = full_data['Diagnóstico']
        print(aux)
        mostrar = pd.DataFrame()
        mostrar['result'] = aux.groupby(['Cluster', 'Diagnóstico']).size()
        print(mostrar)
   
    
    
if __name__ == "__main__":
    main()
    