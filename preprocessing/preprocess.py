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
from skfeature.function.statistical_based.CFS import cfs
from skfeature.function.information_theoretical_based.FCBF import fcbf

def preprocess():
    df = read_new_data_from_local()
    df = selectImportantColumns(df)
    df.to_excel("unformated_data.xlsx", index = False)
    df = filtering(df)
    df.to_excel("formated_data.xlsx", index = False)
    df = df.drop(columns=["Record Id"])
    
    df_numerical = transform_categorical_to_numerical(df)
    df_mix = fill_null_value_categorical(df)
    df_missing = df_numerical
    df_numerical.to_excel("formated_numerical_data.xlsx", index = False)
    
    #Experiments with delete
    #calculate_information(df)
    #delete_null_columns(df)
    #delete_null_rows(df)
    #delete_percentages(df)
    
    #Paint red the empty cells
    
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
    
    filter_col = [col for col in df_numerical if (col.startswith('HLA: grupos de riesgo') |
                    col.startswith('DCG EMA') | col.startswith('Biopsia DCG') | 
                    col.startswith('Valoracion LIEs DCG_') | col.startswith('Valoracion LIEs DSG_') |
                    col.startswith('Biopsia DSG'))]
    df_try7 = df_numerical.filter(filter_col +['1º grado', 'Diagnóstico',
        'Diarrea crónica', 'Estreñimiento', 'Distensión abdominal','Dispepsia','Malabsorción',
        'Anemia ferropénica o ferropenia', 'DCG_ATG2_Negativo', 'DCG_ATG2_Positivo', 'DCG A-PDG_Negativo', 
        'DCG A-PDG_Positivo'])

    X = df_numerical[df_numerical['Diagnóstico']!= "Sin diagnostico"]
    X = X[X['Diagnóstico']!= "Paciente perdido"]
    X = X[X['Diagnóstico']!= "Aún en estudio"]
    
    y = X['Diagnóstico'].to_numpy()
    X = X.drop(columns=['Diagnóstico']).to_numpy()
    idx_cfs = cfs(X,y)
    
    df_try8 = df_numerical.drop(columns=['Diagnóstico'])
    features_selected = df_try8.columns[idx_cfs]
    print(features_selected)
    df_try8  = df_try8.iloc[:, idx_cfs]
    df_try8 ['Diagnóstico'] = df_numerical['Diagnóstico']
    
    idx_fcbf = fcbf(X,y)
    
    df_try9 = df_numerical.drop(columns=['Diagnóstico'])
    features_selected = df_try9.columns[idx_fcbf[0]]
    print(features_selected)
    df_try9 = df_try9.iloc[:, idx_fcbf[0]]
    df_try9['Diagnóstico'] = df_numerical['Diagnóstico']
    
    numericals_dfs = [df_numerical, df_numerical_short, df_try1, df_try2, 
                     df_try3, df_try4, df_try5, df_try6, df_try7, df_try8, df_try9]
    
    #Categorical Experiments
    df_cat_try1 = df_categorical.drop(columns=try_cat_columns)
    df_cat_try2 = pd.concat([df_categorical.iloc[:, 0:17], df_categorical.iloc[:, 57:70]], axis = 1)
    df_cat_try3 = df_cat_try2.drop(columns=try_cat_columns)
    
    df_cat_try4 = df_categorical.filter(['HLA: grupos de riesgo', '1º grado', 'Diagnóstico',
        'Diarrea crónica', 'Estreñimiento', 'Distensión abdominal','Dispepsia','Malabsorción',
        'Anemia ferropénica o ferropenia', 'DCG EMA', 'DCG_ATG2', 'DCG A-PDG', 'Valoracion LIEs DCG', 
        'Valoracion LIEs DSG', 'Biopsia DCG', 'Biopsia DSG'])
    
    df_cat_try5 = df_categorical.filter(['Diagnóstico', 'Valoración LIEs DCG', 'Biopsia DCG',
        'DCG ATG2', 'DSG ATG2', 'DCG A-PDG', 'Valoración LIEs DSG'])
    
    df_cat_try_6 = df_categorical.filter(['Diagnóstico','Valoración LIEs DCG', 'Biopsia DCG',
                                          'Biopsia DSG', 'Esclerosis múltiple', 'Valoración LIEs DSG',
                                          'Malabsorción','DCG ATG2' ])
    
    categorical_dfs = [df_categorical,df_cat_try1, df_cat_try2,
                       df_cat_try3, df_cat_try4, df_cat_try5, df_cat_try_6]
    
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
    df_mix_try7 = df_mix.filter(['HLA: grupos de riesgo', '1º grado', 'Diagnóstico',
        'Diarrea crónica', 'Estreñimiento', 'Distensión abdominal','Dispepsia','Malabsorción',
        'Anemia ferropénica o ferropenia', 'DCG EMA', 'DCG_ATG2', 'DCG A-PDG', 'Valoracion LIEs DCG', 
        'Valoracion LIEs DSG', 'Biopsia DCG', 'Biopsia DSG'])
    
    '''
    LIEs DSG %GD', 'Biopsia DCG_M0',
       'Valoracion LIEs DCG_No compatible con EC', 'DCG_ATG2_Negativo',
       'DCG_ATG2_VALUE', 'Valoracion LIEs DCG_Compatible con EC activa',
       'DSG ATG2_Negativo', 'LIEs DCG %GD', 'DCG A-PDG_Negativo',
       'DCG_ATG2_Positivo', 'Biopsia DCG_M3b'
    '''
    
    df_mix_try8 = df_mix.filter(['Diagnóstico', 'LIEs DSG %GD', 'Biopsia DCG', 
                                 'Valoracion LIEs DCG', 'DCG_ATG2', 'DCG A-PDG',
                                 'LIEs DCG %GD', 'DSG ATG2'])
    
    '''
    'LIEs DSG %GD', 'Biopsia DCG_M0',
       'Valoracion LIEs DCG_No compatible con EC', 'DCG_ATG2_Negativo',
       'Malabsorción', 'Biopsia DSG_M3b', 'Esclerosis múltiple'
    '''
    df_mix_try_9 = df_mix.filter(['Diagnóstico', 'LIEs DSG %GD', 'Biopsia DCG', 
                                  'Valoracion LIEs DCG', 'DCG_ATG2', 'Biopsia DSG', 
                                  'Esclerosis múltiple', 'Malabsorción'])
    mixs_dfs = [df_mix, df_mix_short, df_mix_try1, df_mix_try2,
                       df_mix_try3, df_mix_try4, df_mix_try5, df_mix_try6, df_mix_try7, df_mix_try8, 
                       df_mix_try_9]
    
    
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
    
    filter_col = [col for col in df_missing if (col.startswith('HLA: grupos de riesgo') |
                    col.startswith('DCG EMA') | col.startswith('Biopsia DCG') | 
                    col.startswith('Valoracion LIEs DCG_') | col.startswith('Valoracion LIEs DSG_') |
                    col.startswith('Biopsia DSG'))]
    df_missing_try7 = df_missing.filter(filter_col +['1º grado', 'Diagnóstico',
        'Diarrea crónica', 'Estreñimiento', 'Distensión abdominal','Dispepsia','Malabsorción',
        'Anemia ferropénica o ferropenia', 'DCG_ATG2_Negativo', 'DCG_ATG2_Positivo', 'DCG A-PDG_Negativo', 
        'DCG A-PDG_Positivo'])
    
    df_missing_try8 = df_missing.drop(columns=['Diagnóstico'])
    df_missing_try8 = df_missing_try8.iloc[:, idx_cfs]
    df_missing_try8['Diagnóstico'] = df_missing['Diagnóstico']
    
    df_missing_try9 = df_numerical.drop(columns=['Diagnóstico'])
    df_missing_try9 = df_missing_try9.iloc[:, idx_fcbf[0]]
    df_missing_try9['Diagnóstico'] = df_numerical['Diagnóstico']
    
    
    missings_dfs = [df_missing, df_missing_short, df_missing_try1, df_missing_try2, 
                     df_missing_try3, df_missing_try4, df_missing_try5, df_missing_try6, 
                     df_missing_try7, df_missing_try8, df_missing_try9]
    
    
    
    return [numericals_dfs, missings_dfs, mixs_dfs, categorical_dfs]




    