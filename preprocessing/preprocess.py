# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 21:02:56 2021

@author: Carla
@author: pablo
"""
from format_data import selectImportantColumns, filtering
from load_data import read_new_data_from_local
from categorical_data import transform_categorical_to_numerical, fill_null_value_categorical
from imputation import imputation
from scale import quantile_transformer
from utils import numerical_columns, try1_columns, try_cat_columns
import pandas as pd

def preprocess():
    df = read_new_data_from_local()
    df = selectImportantColumns(df)
    df.to_excel("unformated_data.xlsx", index = False)
    df = filtering(df)
    df.to_excel("formated_data.xlsx", index = False)
    
    df_numerical = transform_categorical_to_numerical(df)
    df_mix = fill_null_value_categorical(df)
    df_missing = df_numerical
    df_numerical.to_excel("formated_numerical_data.xlsx", index = False)
    
    #Experiments with delete
    #calculate_information(df)
    #delete_null_columns(df)
    #delete_null_rows(df)
    #delete_percentages(df)
    
    df_numerical = imputation(df_numerical)
    df_mix[numerical_columns] = df_numerical[numerical_columns]
    df_numerical_short = df_numerical.drop(columns = ["DCG_ATG2_Negativo", "DCG_ATG2_Positivo", 
        "DSG ATG2_Negativo", "DSG ATG2_Positivo","DCG A-PDG_Negativo","DCG A-PDG_Positivo",
        "DSG A-PDG_Negativo","DSG A-PDG_Positivo", "Valoracion LIEs DCG_Compatible con EC activa",
        "Valoracion LIEs DCG_Compatible con EC en DSG", "Valoracion LIEs DCG_No compatible con EC", 
        "Valoracion LIEs DSG_Compatible con EC activa", "Valoracion LIEs DSG_Compatible con EC en DSG",
        "Valoracion LIEs DSG_No compatible con EC"])
    df_numerical.to_excel("formated_imputed_numerical_data.xlsx", index = False)
    #df_categorical.to_excel("formated_imputed_categorical_data.xlsx", index = False)
    
    
    df_numerical = quantile_transformer(df_numerical)
    df_missing = quantile_transformer(df_missing)
    df_numerical_short[numerical_columns] = df_numerical[numerical_columns]
    df_mix[numerical_columns] = df_numerical[numerical_columns]
    df_categorical = df_mix.drop(columns= numerical_columns)
    df_categorical.to_excel("formated_categorical_data.xlsx", index = False)
    df_numerical.to_excel("formated_imputed_scaled_numerical_data.xlsx", index = False)
    df_mix.to_excel("mix.xlsx", index = False)
    #df_categorical.to_excel("formated_imputed_scaled_categorical_data.xlsx", index = False)
    
    #Numerical Experiments 
    df_try1 = df_numerical.drop(columns=try1_columns)
    df_try2 = df_numerical_short.drop(columns=try1_columns)
    df_try3 = pd.concat([df_numerical.iloc[:, 0:8], df_numerical.iloc[:, 48:108]], axis = 1)
    df_try4 = df_try3.drop(columns = ["DCG_ATG2_Negativo", "DCG_ATG2_Positivo", 
        "DSG ATG2_Negativo", "DSG ATG2_Positivo","DCG A-PDG_Negativo","DCG A-PDG_Positivo",
        "DSG A-PDG_Negativo","DSG A-PDG_Positivo", "Valoracion LIEs DCG_Compatible con EC activa",
        "Valoracion LIEs DCG_Compatible con EC en DSG", "Valoracion LIEs DCG_No compatible con EC", 
        "Valoracion LIEs DSG_Compatible con EC activa", "Valoracion LIEs DSG_Compatible con EC en DSG",
        "Valoracion LIEs DSG_No compatible con EC"])
    
    df_try5 = df_try3.drop(columns=try1_columns)
    df_try6 = df_try4.drop(columns = try1_columns)
    
    numericals_dfs = [df_numerical, df_numerical_short, df_try1, df_try2, 
                     df_try3, df_try4, df_try5, df_try6]
    
    #Categorical Experiments
    df_cat_try1 = df_categorical.drop(columns=try_cat_columns)
    df_cat_try2 = pd.concat([df_categorical.iloc[:, 0:17], df_categorical.iloc[:, 57:70]], axis = 1)
    df_cat_try3 = df_cat_try2.drop(columns=try_cat_columns)
    
    categorical_dfs = [df_categorical,df_cat_try1, df_cat_try2,
                       df_cat_try3]
    
    #Mix experiments
    df_mix_short = df_mix.drop(columns = ["DCG_ATG2", "DSG ATG2",
        "DCG A-PDG", "DSG A-PDG", "Valoracion LIEs DCG",
         "Valoracion LIEs DSG"])
    df_mix_try1 = df_mix.drop(columns=try_cat_columns)
    df_mix_try2 = df_mix_short.drop(columns = try_cat_columns)
    df_mix_try3 = pd.concat([df_mix.iloc[:, 0:21], df_mix.iloc[:, 61:70]], axis = 1)
    df_mix_try4 = df_mix_try3.drop(columns = ["DCG_ATG2", "DSG ATG2",
        "DCG A-PDG", "DSG A-PDG", "Valoracion LIEs DCG",
         "Valoracion LIEs DSG"])
    df_mix_try5 = df_mix_try3.drop(columns=try_cat_columns)
    df_mix_try6 = df_mix_try4.drop(columns = try_cat_columns)
    

    mixs_dfs = [df_mix, df_mix_short, df_mix_try1, df_mix_try2,
                       df_mix_try3, df_mix_try4, df_mix_try5, df_mix_try6]
    
    
    #Missing Experiments
    df_missing_short = df_missing.drop(columns = ["DCG_ATG2_Negativo", "DCG_ATG2_Positivo", 
        "DSG ATG2_Negativo", "DSG ATG2_Positivo","DCG A-PDG_Negativo","DCG A-PDG_Positivo",
        "DSG A-PDG_Negativo","DSG A-PDG_Positivo", "Valoracion LIEs DCG_Compatible con EC activa",
        "Valoracion LIEs DCG_Compatible con EC en DSG", "Valoracion LIEs DCG_No compatible con EC", 
        "Valoracion LIEs DSG_Compatible con EC activa", "Valoracion LIEs DSG_Compatible con EC en DSG",
        "Valoracion LIEs DSG_No compatible con EC"])
    df_missing_try1 = df_missing.drop(columns=try1_columns)
    df_missing_try2 = df_missing_short.drop(columns=try1_columns)
    df_missing_try3 = pd.concat([df_numerical.iloc[:, 0:8], df_numerical.iloc[:, 48:108]], axis = 1)
    df_missing_try4 = df_missing_try3.drop(columns = ["DCG_ATG2_Negativo", "DCG_ATG2_Positivo", 
        "DSG ATG2_Negativo", "DSG ATG2_Positivo","DCG A-PDG_Negativo","DCG A-PDG_Positivo",
        "DSG A-PDG_Negativo","DSG A-PDG_Positivo", "Valoracion LIEs DCG_Compatible con EC activa",
        "Valoracion LIEs DCG_Compatible con EC en DSG", "Valoracion LIEs DCG_No compatible con EC", 
        "Valoracion LIEs DSG_Compatible con EC activa", "Valoracion LIEs DSG_Compatible con EC en DSG",
        "Valoracion LIEs DSG_No compatible con EC"])
    
    df_missing_try5 = df_missing_try3.drop(columns=try1_columns)
    df_missing_try6 = df_missing_try4.drop(columns = try1_columns)
    
    missings_dfs = [df_missing, df_missing_short, df_missing_try1, df_missing_try2, 
                     df_missing_try3, df_missing_try4, df_missing_try5, df_missing_try6]
    
    
    
    return [numericals_dfs, missings_dfs, mixs_dfs, categorical_dfs]




    