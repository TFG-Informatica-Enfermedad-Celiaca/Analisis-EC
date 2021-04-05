# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 20:26:22 2021

@author: Carla
@author: pablo
"""

def calculate_information(df):
    df = df.drop(columns=["Diagnóstico"])
    number_of_nulls = df.isnull().sum().sum()
    total_cells = df.size
    percentage_of_nulls = number_of_nulls/total_cells
    print(number_of_nulls)
    print(total_cells)
    print(percentage_of_nulls)
    print(len(df.columns))

def delete_null_columns(df):
    df_delete = df.dropna(1)
    print(len(df_delete.columns))
    # Which are the columns that we have deleted 
    print(set(df.columns).symmetric_difference(set(df_delete.columns)))

def delete_null_rows(df):
    print(len(df.dropna()))
    
def delete_percentages(df):
    df_delete = df.copy()
    while (df_delete.isnull().sum().sum() > 0):
        percentages_columns = df_delete.isnull().mean().tolist()
        max_columns = max(percentages_columns)
        percentages_rows = df_delete.isnull().mean(axis=1).tolist()
        max_rows = max(percentages_rows)
        if(max_columns > max_rows):
            df_delete = df_delete.drop(columns = df_delete
                    .columns[percentages_columns.index(max_columns)])
        else:
            df_delete = df_delete.drop(df_delete
                            .index[[percentages_rows.index(max_rows)]])
            
    print(len(df_delete.columns))
    print(len(df_delete))
    print(set(df.columns).symmetric_difference(set(df_delete.columns)))
