# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 21:02:56 2021

@author: Carla
@author: pablo
"""
from format_data import selectImportantColumns, filtering
from load_data import read_new_data_from_local
from categorical_data import transform_categorical_to_numerical, fill_null_value_categorical
from imputation import knn_imputation
from scale import quantile_transformer
from utils import numerical_columns

def preprocess():
    df = read_new_data_from_local()
    df = selectImportantColumns(df)
    df.to_excel("unformated_data.xlsx", index = False)
    df = filtering(df)
    df.to_excel("formated_data.xlsx", index = False)
    
    df_numerical = transform_categorical_to_numerical(df)
    df_categorical = fill_null_value_categorical(df)
    df_numerical.to_excel("formated_numerical_data.xlsx", index = False)
    df_categorical.to_excel("formated_categorical_data.xlsx", index = False)
    
    #Experiments with delete
    #calculate_information(df)
    #delete_null_columns(df)
    #delete_null_rows(df)
    #delete_percentages(df)
    
    df_numerical = knn_imputation(df_numerical)
    df_categorical[numerical_columns] = df_numerical[numerical_columns]
    df_numerical.to_excel("formated_imputed_numerical_data.xlsx", index = False)
    df_categorical.to_excel("formated_imputed_categorical_data.xlsx", index = False)
    
    df_numerical = quantile_transformer(df_numerical)
    df_categorical[numerical_columns] = df_numerical[numerical_columns]
    df_numerical.to_excel("formated_imputed_scaled_numerical_data.xlsx", index = False)
    df_categorical.to_excel("formated_imputed_scaled_categorical_data.xlsx", index = False)
    
    return [df_numerical, df_categorical]
    