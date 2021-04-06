# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 21:24:43 2021

@author: Carla
@author: pablo
"""
import pandas as pd

def rate(df, clusters):
    aux = pd.DataFrame()
    aux['Cluster']=clusters
    aux['Diagnóstico'] = df['Diagnóstico']
    print(aux)
    mostrar = pd.DataFrame()
    mostrar['result'] = aux.groupby(['Cluster', 'Diagnóstico']).size()
    print(mostrar) 