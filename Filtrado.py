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
from sklearn import preprocessing

'''
Read data from .csv file stored in local and creates dataframe
'''
def read_data_from_local():
    try:
        df=pd.read_csv(
            '/Users/pablo/Desktop/Universidad/5/TFG/Informática/Codigo/Datos.csv')
        return df
    except:
        try:
            df=pd.read_csv(
                '/mnt/c/Users/Carla Martínez/Desktop/TFG-Informática/Datos.csv')
            return df
        except:
            print("It was not possible to load data")


'''
Read the relevant columns form .xlsx stored in local and creates deaframe
'''
def read_columns_from_local():
    try:
        df=pd.read_excel(
            '/Users/pablo/Desktop/Universidad/5/TFG/Informática/Codigo/Important columns.xlsx')
        return df
    except:
        try:
            df=pd.read_excel(
                '/mnt/c/Users/Carla Martínez/Desktop/TFG-Informática/Important columns.xlsx')
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
    new_columns = ['1º grado','2º grado','3º grado', '4º grado']
    for column in new_columns:
        if (column not in df_aux.columns):
            df_aux.insert(0, column, 0)

    # In case there is a i-level of kindship it fills the column 'iº grado' with '1'
    for i in range(1, 4):
        df_aux.loc[df_aux['Grado de parentesco'].str.contains(str(i)) | 
            df_aux['Grado de parentesco (si hay más de 1)'].str.contains(str(i)), str(i)+'º grado'] = 1

    # Delete the previous columns releated to kindship
    df_aux = df_aux.drop(columns=['Grado de parentesco', 'Grado de parentesco (si hay más de 1)'])
    return df_aux

'''
For each different value in 'previous_columns' we create a column. 
Each record contains 0 in case the row has not that value and 1 in
case the row has that value
'''
def process_columns_to_binary(df_aux, delete_more, records_number, previous_columns):
    # Create an array containing the values in previous_colums 
    new_columns= pd.unique(df_aux[previous_columns].values.ravel('K'))
    # Filter out nan value and delete_more in array
    new_columns = list(filter(lambda i: not i in [np.nan] + delete_more, new_columns))
    
    data_aux = pd.DataFrame(columns = new_columns,
                                index = range(records_number))
    data_aux.iloc[:,:] = 0
    
    for i in range(0, len(new_columns)):
        for j in range(records_number):
            for z in range (0, len(previous_columns)):
                if (new_columns[i] == df_aux.loc[:,
                                        previous_columns[z]].iloc[j]): 
                    data_aux.loc[:,new_columns[i]].iloc[j] = 1
                    
    df_aux = pd.concat([df_aux, data_aux], axis = 1)
    
    
    # Delete previous columns 
    df_aux = df_aux.drop(columns=previous_columns)
    return df_aux

'''
Given a list of columns this creates a one binary column per value
IMPORTANT: the values in the columns should be disjoint, if not it 
will create as many new columns as it appears in a different colums
'''
def simple_process_columns_to_binary(df_aux, columns_list):
    df_aux = pd.get_dummies(df_aux, columns=columns_list)
    return df_aux


'''
Changes the value of a column to binary when it only has 2 possible values
'''
def change_column_to_binary(df_aux, column_list):
    df_aux = pd.get_dummies(df_aux, columns ={column_list[0]})
    df_aux = df_aux.drop(columns=column_list[1], axis=1)
    df_aux = df_aux.rename(columns={column_list[2]: column_list[0]})
    return df_aux

'''
Given a column containing numerical data this fills the mising values with ceros
and normalizes the data
'''
def fill_nan_with_zero_and_scale(df_aux, column_list):
    for column in column_list:
        df_aux[column] = df_aux[column].fillna(0)
        df_aux[column] = df_aux[column].astype(str)
        df_aux[column] = df_aux[column].apply(lambda x: float(x.replace(',', '.')))
  
    min_max = preprocessing.MinMaxScaler()
    scaled_df = min_max.fit_transform(df_aux[column_list].values)
    final_df = pd.DataFrame(scaled_df,columns=column_list)
    df_aux = df_aux.drop(columns= column_list)

    df_aux = pd.concat([df_aux, final_df], axis = 1)

    return df_aux


'''
Given a file with the relevant columns name, it selects them in the dataframe
'''
def selectImportantColumns(df_aux):
    important_columns = read_columns_from_local()
    important_columns = list(important_columns.iloc[:,1])
    df_aux = df_aux.loc[:,important_columns]
    return df_aux
    
'''
Preprocessing for column column_name so we only have as values possible_values
'''
def preprocessing_1(df_aux, records_number, column_name, possible_values):
    data_aux = pd.DataFrame(columns = [column_name],
                                index = range(records_number))

    data_aux[column_name] = df_aux[column_name]
    # Get only the first word 
    data_aux[column_name] = data_aux[column_name].apply(lambda x: np.where(pd.isnull(x), x, str(x).split()[0]))

    for j in range(records_number):
        if (~pd.isnull(data_aux.loc[:,column_name].iloc[j])):
            # If the word contains special characters at the end delete them
            if (((data_aux.loc[:,column_name].iloc[j])[-1] == "?") |
            ((data_aux.loc[:,column_name].iloc[j])[-1] == ":") |
            ((data_aux.loc[:,column_name].iloc[j])[-1] == ",") ):
                data_aux.loc[:,column_name].iloc[j] = data_aux.loc[:,column_name].iloc[j][:-1]
            # If we have a value diferent from DSG DCG and Provocación delete it
            enter = 0
            for value in possible_values:
                if data_aux.loc[:,column_name].iloc[j] == value:
                    enter = 1
                    break
            if enter == 0:
                data_aux.loc[:,column_name].iloc[j] = np.nan

    df_aux = df_aux.drop(columns=[column_name])
    df_aux = pd.concat([df_aux, data_aux], axis = 1)
    return df_aux

'''
Processing columns "ELISPOT" y "ELISPOT.1" so we only have values "Negativo" and "Positivo"
and unite them in one with the most up-to-date value 
'''
def elispot_preprocessing (df_aux, records_number):
    columns = ["ELISPOT", "ELISPOT.1"]
    df_aux[columns] = df_aux[columns].apply(lambda x: np.where((x != "Negativo") & (x != "Positivo"), np.nan, x))

    data_aux = pd.DataFrame(columns = ["ELISPOT"],
                                index = range(records_number))

    for j in range(records_number):
        # If there is a value in the second column then we take it
        if (~pd.isnull(df_aux.loc[:,columns[1]].iloc[j])):
            data_aux["ELISPOT"].iloc[j] = df_aux[columns[1]].iloc[j]
        else:
            data_aux["ELISPOT"].iloc[j] = df_aux[columns[0]].iloc[j]
    
    df_aux = df_aux.drop(columns=columns)
    df_aux = pd.concat([df_aux, data_aux], axis = 1)
    return df_aux

def main():
    df = read_data_from_local()
    df_aux = df
    df_aux = selectImportantColumns(df_aux)
    records_number = df_aux.iloc[:,0].size
    for data in preprocessing_1_data.values():
        df_aux = preprocessing_1(df_aux, records_number, data[0][0], data[1])

    df_aux = elispot_preprocessing(df_aux, records_number)
    df_aux.to_excel("unfilterData.xlsx")

    df_aux = process_kindship(df_aux)
    df_aux = simple_process_columns_to_binary(df_aux, simple_process_column_names)
    df_aux = fill_nan_with_zero_and_scale(df_aux, fill_nan_with_zero_column_names)

    for column in column_to_binary_column_names.values():
        df_aux = change_column_to_binary(df_aux, column)
    
    df_aux = df_aux.loc[:,~df_aux.columns.duplicated()]
    for column in process_column_names.values():
        df_aux = process_columns_to_binary(df_aux,column[1], records_number, column[0])

    df_aux.to_excel("filterData.xlsx")
    

if __name__ == "__main__":
    main()
    
    
    
    