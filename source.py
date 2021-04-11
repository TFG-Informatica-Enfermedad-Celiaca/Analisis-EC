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
from kprototypes import kprototypes
from kmodes_a import kmodes
from kpod_a import kpod
from agglomerative import agglomerative
from DBSCAN import dbscan
from kmedoids import kmedoids
from optics import optics

def main():
    [df_numerical, df_numerical_short,df_missing, df_mix, df_categorical] = preprocess()
    #kmeans(df_numerical)
    #kmeans(df_numerical_short)
    kpod(df_missing)
    #kprototypes(df_mix)
    #kmodes(df_categorical)
    #agglomerative(df_numerical)
    #dbscan(df_numerical)
    #kmedoids(df_numerical)
    #optics(df_numerical)
    
    
if __name__ == "__main__":
    main()