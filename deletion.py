# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 20:26:22 2021

@author: Carla
@author: pablo
"""
from loadData import read_new_data_from_local
from Filtrado import filtering, selectImportantColumns

def main():
    df = read_new_data_from_local()
    
    df = selectImportantColumns(df)
    df = filtering(df)
    
    #################################################
    # Delete incomplete information in the dataset
    #################################################
    df_delete = df.copy()
    df_delete = df_delete.drop(columns=["Diagnóstico"])
    number_of_nulls = df_delete.isnull().sum().sum()
    total_cells = df_delete.size
    percentage_of_nulls = number_of_nulls/total_cells
    print(number_of_nulls)
    print(total_cells)
    print(percentage_of_nulls)
    print(len(df_delete.columns))
    
    #################################################
    ## Delete the columns with null values
    df_delete1 = df_delete.dropna(1)
    print(len(df_delete1.columns))
    # Which are the columns that we have deleted 
    print(set(df_delete.columns).symmetric_difference(set(df_delete1.columns)))
    
    #################################################
    ## Delete the rows with null values
    df_delete2 = df_delete.dropna()
    print(len(df_delete2))
    
    #################################################
    ## Delete the rows and columns with null values depending on percentage
    df_delete3 = df_delete.copy()
    while (df_delete3.isnull().sum().sum() > 0):
        percentages_columns = df_delete3.isnull().mean().tolist()
        max_columns = max(percentages_columns)
        percentages_rows = df_delete3.isnull().mean(axis=1).tolist()
        max_rows = max(percentages_rows)
        if(max_columns > max_rows):
            df_delete3 = df_delete3.drop(columns = df_delete3
                    .columns[percentages_columns.index(max_columns)])
        else:
            df_delete3 = df_delete3.drop(df_delete3
                            .index[[percentages_rows.index(max_rows)]])
            
    print(len(df_delete3.columns))
    print(len(df_delete3))
    print(set(df_delete.columns).symmetric_difference(set(df_delete3.columns)))

if __name__ == "__main__":
    main()
    