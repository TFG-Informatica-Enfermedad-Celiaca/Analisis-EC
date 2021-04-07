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
from agglomerative import agglomerative
from DBSCAN import dbscan
from kmedoids import kmedoids
from optics import optics

def main():
    [df_numerical, df_categorical] = preprocess()
    kmeans(df_numerical)
    kprototypes(df_categorical)
    agglomerative(df_numerical)
    dbscan(df_numerical)
    kmedoids(df_numerical)
    optics(df_numerical)
    
    
if __name__ == "__main__":
    main()