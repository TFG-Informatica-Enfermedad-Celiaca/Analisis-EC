# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 11:58:12 2021

@author: pablo
@author: Carla
"""

import pandas as pd
from kmodes.kprototypes import KPrototypes
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default='browser'
from tqdm import tqdm
import sys
sys.path.append(r'../')
from loadData import read_data_from_local
from utils import final_columns_to_numeric, final_column_to_one_hot
from reduceDimension import reduce_dimension_global_data_plotly, reduce_dimension_after_clustering
from scoreF1 import f1_score

def main ():
    reduce_dimension_global_data_plotly()
    full_data = read_data_from_local()
    data = full_data.drop(columns = ['Diagnóstico'])
    train_numpy = full_data.to_numpy()

    categories_numbers = [data.columns.get_loc(col) for col in 
                          final_columns_to_numeric + final_column_to_one_hot]
    
    X = train_numpy[:, 1:]
    #y = train_numpy[:, 0]
    
    K_MAX = 10
    #Elbow plot: must find the value at wich the cost starts decreasing in 
    # a lineal way
    costs = []
    n_clusters = []
    clusters_assigned = []
    
    for i in tqdm(range(2, K_MAX)):
        try:
            # The model will select the i first different elements 
            # in the dataset as centroids
            kproto = KPrototypes(n_clusters=i, init='Huang', verbose=0, random_state = 0)
            clusters = kproto.fit_predict(X, categorical=categories_numbers)
            # Cost is defined as the sum of the distance from all the points 
            # to the centroid
            costs.append(kproto.cost_)
            n_clusters.append(i)
            clusters_assigned.append(clusters)
        except:
            print(f"Can't cluster with {i} clusters")
            
    fig = go.Figure(data=go.Scatter(x=n_clusters, y=costs))
    fig.update_layout(title='Elbow plot',
                   xaxis_title='Número clusters',
                   yaxis_title='Suma distancias de cada punto a su centro')
    fig.show()
    
    N_CLUSTER = 4
    # When we see the Elbow plot it is clear that the elbow is in 4
    # So we are going to use n_cluster = 4
    kproto = KPrototypes(n_clusters=N_CLUSTER, init='Huang', verbose=0, random_state = 0)
    clusters = kproto.fit_predict(X, categorical=categories_numbers)

    reduce_dimension_after_clustering(clusters, N_CLUSTER)
    f1_score(clusters)
    
    aux = pd.DataFrame()
    aux['Cluster']=clusters
    aux['Diagnóstico'] = full_data['Diagnóstico']
    print(aux)
    mostrar = pd.DataFrame()
    mostrar['result'] = aux.groupby(['Cluster', 'Diagnóstico']).size()
    print(mostrar)
    
    
if __name__ == "__main__":
    main()
    