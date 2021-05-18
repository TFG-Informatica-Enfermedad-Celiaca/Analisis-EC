# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 21:24:43 2021

@author: Carla
@author: pablo
"""
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default='browser'
import numpy as np
from plotly.subplots import make_subplots
import matplotlib, random


def rate(df, clusters, algorithm, silhouette, b3):
    aux = pd.DataFrame()
    aux['Cluster']=clusters

    aux['Diagnóstico'] = df['Diagnóstico']
    
    #Generate colors randomly
    colors = ['lightgoldenrodyellow','lightgray', 'lightgreen', 
              'lightpink', 'lightsalmon', 'lightseagreen',
                'lightskyblue', 'lightyellow', 'lime', 'linen',
                'magenta',  'mediumaquamarine']

    colors_final= []
    for c in clusters:
        colors_final.append(colors[int(c)%len(colors)])

    aux['Color'] = colors_final
    mostrar = pd.DataFrame()
    mostrar['result'] = aux.groupby(['Cluster','Color','Diagnóstico']).size()
    
    fig = make_subplots(
    rows=2, cols=1,
    shared_xaxes=True,
    vertical_spacing=0.03,
    specs=[[{"type": "table"}],
           [{"type": "table"}]]
    )
    
    fig.add_trace(
    go.Table(
        columnwidth = [60,30],
        header=dict(
            values=[['<b>Diagnóstico</b>'], ['<b>Número</b>']]
        ),
        cells=dict(
            values=[mostrar.reset_index()['Diagnóstico'], mostrar.reset_index()['result']],
            fill_color=[mostrar.reset_index()['Color']],
            align = "left")
    ),
    row=1, col=1
    )
    
    fig.add_trace(
    go.Table(
        columnwidth = [30,30, 30, 30],
        header=dict(
            values=[['<b>Silhouette</b>'], ['<b>Valor-F</b>'], ['<b>Precisión</b>'], ['<b>Exhaustividad</b>']]
        ),
        cells=dict(
            values=[silhouette, b3[0], b3[1], b3[2]],
            align = "left")
    ),
    row=2, col=1
    )
    fig.update_layout(width=500, height=1300, title =  algorithm)
    fig.show()
    