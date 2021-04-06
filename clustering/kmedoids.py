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
#from tqdm import tqdm
#from sklearn.metrics import silhouette_score
#import plotly.graph_objects as go
from rater import rate
def kmedoids (df):
    data = df.drop(columns = ['Diagnóstico'])
     
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
        
        rate(df, kmedoids.labels_)
   
    