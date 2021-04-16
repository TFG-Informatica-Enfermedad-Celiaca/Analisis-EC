# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 21:37:46 2021

@author: Carla
@author: pablo
"""
import sys
sys.path.append(r'./preprocessing')
sys.path.append(r'./clustering')
from preprocess import preprocess
from kmeans import kmeans
from kmodes_prototypes import kmodes, kprototypes
from kpod_a import kpod
from agglomerative import agglomerative
from DBSCAN import dbscan
from kmedoids import kmedoids
from optics import optics
from spectral import spectral
from reduceDimension import reduce_dimension_global_data_plotly
from hopkins_statistics import hopkins_test

def main():
    [df_numerical, df_numerical_short,df_missing, df_mix, df_categorical] = preprocess()
    
    for df in [df_numerical, df_numerical_short] :
        hopkins_test(df)
        
    #reduce_dimension_global_data_plotly()
    #kmeans(df_numerical)
    #kmeans(df_numerical_short)
    #kpod(df_numerical, df_missing)
    #kprototypes(df_numerical, df_mix)
    #kmodes(df_numerical, df_categorical)
    #spectral(df_numerical)
    #agglomerative(df_numerical)
    #dbscan(df_numerical)
    #kmedoids(df_numerical)
    #optics(df_numerical)
    
    
if __name__ == "__main__":
    main()