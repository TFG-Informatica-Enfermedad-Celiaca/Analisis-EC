# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 14:23:39 2021

@author: Carla
"""

import pandas as pd
import umap as umap
import plotly.io as pio
import plotly.express as px
pio.renderers.default='browser'
import sys
sys.path.append(r'../preprocessing')
from load_data import read_numerical_data_from_local, read_data_from_local

def reduce_dimension_global_data_plotly(): 
    data = read_data_from_local()
    numeric_data = read_numerical_data_from_local()
    aux_data = numeric_data.drop(columns = ['Diagnóstico'])
    numeric_numpy = aux_data.to_numpy()
    
    reducer = umap.UMAP(random_state=42)
    reducer.fit(numeric_numpy)
    embedding = reducer.transform(numeric_numpy)
    
    x = pd.DataFrame(data={'x_axis':embedding[:, 0]})
    y = pd.DataFrame(data={'y_axis':embedding[:, 1]})
    data = pd.concat((data,x, y),axis=1)
    fig = px.scatter(data, x='x_axis', y='y_axis', 
                     color="Diagnóstico", hover_data={'x_axis' : False, 'y_axis': False, 
                    "Sexo":True, "HLA: grupos de riesgo": True, "DCG EMA": True, 
                    "DSG EMA  ": True, "DCG_ATG2": True, "DCG A-PDG": True,
                    "DSG ATG2": True, "DSG A-PDG": True, "Valoracion LIEs DCG": True, 
                    "Valoracion LIEs DSG": True, "Biopsia DCG": True, "Biopsia DSG": True})
    fig.update_layout(title='Reducción de la dimensionalidad con UMAP', 
                      xaxis_title='',
                      yaxis_title='')    
    fig.show()

def reduce_dimension_after_clustering(clusters, number_of_clusters):
    data = read_data_from_local()
    data = data.fillna("Desconocido")
    numeric_data = read_numerical_data_from_local()
    aux_data = numeric_data.drop(columns = ['Diagnóstico'])
    numeric_numpy = aux_data.to_numpy()
    
    reducer = umap.UMAP(random_state=42)
    reducer.fit(numeric_numpy)
    embedding = reducer.transform(numeric_numpy)
    
    x = pd.DataFrame(data={'x_axis':embedding[:, 0]})
    y = pd.DataFrame(data={'y_axis':embedding[:, 1]})
    cluster = pd.DataFrame(data={'cluster':clusters})
    cluster = cluster.astype({'cluster': object})
    data = pd.concat((data,x, y, cluster),axis=1)
    fig = px.scatter(data, x='x_axis', y='y_axis', 
                     color="cluster", symbol= "Diagnóstico", hover_data={'x_axis' : False, 'y_axis': False, 
                    "Sexo":True, "HLA: grupos de riesgo": True, "DCG EMA": True, 
                    "DSG EMA  ": True, "DCG_ATG2": True, "DCG A-PDG": True,
                    "DSG ATG2": True, "DSG A-PDG": True, "Valoracion LIEs DCG": True, 
                    "Valoracion LIEs DSG": True, "Biopsia DCG": True, "Biopsia DSG": True})
    fig.update_layout(title='Reducción de la dimensionalidad con UMAP', 
                      xaxis_title='',
                      yaxis_title='')    
    fig.show()

    