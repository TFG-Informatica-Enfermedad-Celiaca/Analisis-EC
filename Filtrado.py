#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 16:29:51 2021

@author: pablo
@author: carla
"""

import pandas as pd
import numpy as np
from utils import *

'''
Read data from .csv file stored in local and creates dataframe
'''
def read_data_from_local():
    try:
        df=pd.read_csv(
            '/Users/pablo/Desktop/Universidad/5/TFG/Informática/Datos.csv')
        return df
    except:
        try:
            df=pd.read_csv(
                '/mnt/c/Users/Carla Martínez/Desktop/TFG-Informática/Datos.csv')
            return df
        except:
            print("It was not possible to load data")


'''
Insert columns in the dataframe that show if the patient has celiac family. 
There are 4 levels of kindship so we create 4 columns, each of which contains
0 in case there isn't any celiac relative in that level or 1 in other case.
'''
def process_kindship(df_aux):
    # Create 4 extra columns and fill them with 0s
    df_aux = df_aux.reindex (columns = df_aux.columns.tolist() +
                                ['1º grado','2º grado','3º grado', '4º grado'])
    df_aux.loc[:, ['1º grado','2º grado','3º grado', '4º grado']] = 0

    # In case there is a i-level of kindship it fills the column 'iº grado' with '1'
    for i in range(1, 4):
        df_aux.loc[df_aux['Grado de parentesco'].str.contains(str(i)) | 
            df_aux['Grado de parentesco (si hay más de 1)'].str.contains(str(i)), str(i)+'º grado'] = 1

    # Delete the previous columns releated to kindship
    df_aux.drop(columns=['Grado de parentesco', 'Grado de parentesco (si hay más de 1)'])
    return df_aux

'''
For each different value in 'previous_columns' we create a column. Each record contains 0 in case
the row has not that value and 1 in case the row has that value
'''
def process_columns_to_binary(df_aux, delete_more, records_number, previous_columns):

    # create an array containing the values in previous_colums 
    new_columns= pd.unique(df_aux[previous_columns].values.ravel('K'))
    # Filter out nan value and delete_more in array
    new_columns = list(filter(lambda i: not i in [np.nan] + delete_more, new_columns))

    # Add a new column per desease
    df_aux = df_aux.reindex (columns = df_aux.columns.tolist() +
                                new_columns)
    df_aux.loc[:, new_columns] = 0

    for i in range(0, len(new_columns)):
        for j in range(records_number):
            for z in range (0, len(previous_columns)):
                if (new_columns[i] == df_aux.loc[:,
                                        previous_columns[z]].iloc[j]): 
                    df_aux.loc[:,new_columns[i]].iloc[j] = 1
    
    # Delete previous columns 
    df_aux.drop(columns=previous_columns)
    return df_aux


def main():
    df = read_data_from_local()
    df.excel("DatosBonitos.xlsx")
    df_aux = df
    records_number = df.iloc[:,0].size
    df_aux = process_kindship(df_aux)
    df_aux = process_columns_to_binary(df_aux,to_delete["immunological_desease"], records_number, column_names["immunological_desease"])
    df_aux = process_columns_to_binary(df_aux,to_delete["symptoms"], records_number, column_names["symptoms"])
    df_aux.to_excel("filterData.xlsx")

if __name__ == "__main__":
    main()