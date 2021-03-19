#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 16:29:51 2021

@author: pablo
@author: carla
"""

import pandas as pd
import numpy as np
from utils import european_countries, take_the_highest_value_columns, lies_dcg_numerical,lies_dsg_numerical
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
                r'C:\Users\Carla\Desktop\TFG-Informatica\Datos.csv')
            return df
        except:
            print("It was not possible to load data 1")


'''
Read the relevant columns form .xlsx stored in local and creates deaframe
'''
def read_new_data_from_local():
    try:
        df=pd.read_excel(
            '/Users/pablo/Desktop/Universidad/5/TFG/Informática/Codigo/Datos actualizados.xlsx')
        return df
    except:
        try:
            df=pd.read_excel(
                r'C:\Users\Carla\Desktop\TFG-Informatica\Datos actualizados.xlsx')
            return df
        except:
            print("It was not possible to load data 2")



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
                r'C:\Users\Carla\Desktop\TFG-Informatica\Important columns.xlsx')
            return df
        except:
            print("It was not possible to load data 3")

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
            df_aux.insert(len(df_aux.columns), column, 0)

    # In case there is a i-level of kindship it fills the column 'iº grado' with '1'
    for i in range(1, 4):
        df_aux.loc[df_aux['Grado de parentesco'].str.contains(str(i)) | 
            df_aux['Grado de parentesco (si hay más de 1)'].str.contains(str(i)), str(i)+'º grado'] = 1

    # Delete the previous columns releated to kindship
    df_aux = df_aux.drop(columns=['Grado de parentesco', 'Grado de parentesco (si hay más de 1)'])
    return df_aux


'''
Fill the dataframes with the new cloumns with 1s
'''
def fill_table(new_columns, records_number, previous_columns, data):
    
    data_aux = pd.DataFrame(columns = new_columns,
                                index = range(records_number))
    data_aux.iloc[:,:] = 0
    
    for i in range(0, len(new_columns)):
        for j in range(records_number):
            for z in range (0, len(previous_columns)):
                aux = data.loc[:, previous_columns[z]].iloc[j]
                if (str(aux) != 'nan' and new_columns[i] in aux): 
                    data_aux.loc[:,new_columns[i]].iloc[j] = 1
                    
    data = pd.concat([data, data_aux], axis = 1)
    
    return data

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
    
    df_aux =  fill_table(new_columns, records_number, previous_columns, df_aux)             
    
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
        #df_aux[column] = df_aux[column].fillna(0)
        df_aux[column] = df_aux[column].astype(str)
        df_aux[column] = df_aux[column].apply(lambda x: float(x.replace(',', '.')))
  
    
    min_max = preprocessing.MinMaxScaler()
    scaled_df = min_max.fit_transform(df_aux[column_list].values)
    final_df = pd.DataFrame(scaled_df,columns=column_list)
    df_aux = df_aux.drop(columns= column_list)
    

    df_aux = pd.concat([df_aux, final_df], axis = 1)
    

    return df_aux

'''
Given some columns, take the last column avaliable
'''
def take_last_column_avaliable(df_aux, column_list):
    new_colum = df_aux.loc[:, column_list[len(column_list)-1]]
    for i in reversed(column_list):
        new_colum = new_colum.replace(np.nan, df_aux.loc[:,i])
        
    df_aux = df_aux.drop(columns= column_list)
    df_aux = pd.concat([df_aux, new_colum], axis = 1)
    
    return df_aux

'''
Given some columns, parse the values and create the necessary columns
'''
def parse_values_create_columns_and_fill(df_aux, column_list, records_number):
    val = []
    newColumns = []
    for column in column_list:
        val = df_aux.loc[:,column].values
    
    val = pd.unique(val)
    val = pd.DataFrame(val).dropna()
    val = val.values.tolist()
    
    for i in range(0, len(val)):
        aux = val[i][0].split(',')
        for j in range(0, len(aux)):
            if aux[j] not in newColumns:
                newColumns.append(aux[j])
    
    df_aux = fill_table(newColumns, records_number, column_list, df_aux)
    df_aux = df_aux.drop(columns = column_list)

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
Function that group countries by European or not
'''
def countries_preprocesing(df_aux, european_countries, records_number):
    df_aux["Indique país de origen o en su defecto la información disponible"] = df_aux[
        "Indique país de origen o en su defecto la información disponible"
        ].replace(np.nan, "Desconocido")
    df_aux["Indique país de origen o en su defecto la información disponible"] = df_aux[
        "Indique país de origen o en su defecto la información disponible"
        ].replace([european_countries], "Europeo")

    df_aux.loc[(df_aux["Indique país de origen o en su defecto la información disponible"]
        != "Europeo") & 
        (df_aux["Indique país de origen o en su defecto la información disponible"]
        != "Desconocido"),
        "Indique país de origen o en su defecto la información disponible"
        ] = "Otro" 

    return df_aux



'''
Functions that join several columns and take the higher values 
'''
def take_highest_value(df_aux, posOrNeg, numericalValues, kits,
                       kitOK, finalName1, finalName2):
    kitsAccepted = []
   
    #Check the kits
    for i in kits:
        aux = df_aux[df_aux[i] == kitOK[0]].index.tolist()
        kitsAccepted.append(aux)
        kitsAccepted = np.unique(kitsAccepted)
    
    #Take the most positive values of each rows
    auxPorN = pd.DataFrame(index=range(len(df_aux.loc[:,posOrNeg[0]])),columns=range(1)).squeeze()
    for i in posOrNeg:
        aux = []
        for j in range(len(df_aux.loc[:,posOrNeg[0]])):
            if (df_aux.loc[:,i].iloc[j] == "Positivo") or (
                    (str(auxPorN[j]) == 'nan') & (df_aux.loc[:,i].iloc[j] != 'No hechos')):
                aux.append(df_aux.loc[:,i].iloc[j])
            else:
                aux.append(auxPorN[j])
        auxPorN = aux
    
    #Take the highest numerical values of each rows
    corrValu = df_aux.loc[:,numericalValues[0]]
    for i in numericalValues:
        aux = []
        for j in range(len(corrValu)):
            if (df_aux.loc[:,i].iloc[j] > corrValu[j]) or (
                    str(corrValu[j]) == 'nan'):
                aux.append(df_aux.loc[:,i].iloc[j])
            else:
                aux.append(corrValu[j])
        corrValu = aux
    
    #insert the new columns into the dataframe and remove the old ones
    aux = pd.DataFrame({finalName1[0]:auxPorN, finalName2[0]:corrValu})
    for i in range(0, len(auxPorN)):
        if i not in kitsAccepted:
            aux.loc[i,finalName1[0]] = np.nan
            aux.loc[i,finalName2[0]] = np.nan
    
    df_aux = df_aux.drop(columns= (posOrNeg + numericalValues + kits))
    df_aux = pd.concat([df_aux, aux], axis = 1)
    
    
    return df_aux

'''
Function that formats HLA
'''
def HLA_formating(df_aux):
    df_aux.loc[ (df_aux['Haplotipo1'] == 'SIN RIESGO') | (df_aux['Haplotipo2'] == 'SIN RIESGO')
               , 'HLA: grupos de riesgo'] =  'SIN RIESGO'
    df_aux.loc[ (df_aux['Haplotipo1'] == 'DQ7.5') | (df_aux['Haplotipo2'] == 'DQ7.5')
               , 'HLA: grupos de riesgo'] =  'DQ7.5'
    df_aux.loc[ (df_aux['Haplotipo1'] == 'DQ2.2') | (df_aux['Haplotipo2'] == 'DQ2.2')
               , 'HLA: grupos de riesgo'] =  'DQ2.2'
    df_aux.loc[ (df_aux['Haplotipo1'] == 'DQ8') & (df_aux['Haplotipo2'] == 'DQ8')
               , 'HLA: grupos de riesgo'] =  'DQ8 doble dosis'
    df_aux.loc[ (df_aux['Haplotipo1'] == 'DQ8') | (df_aux['Haplotipo2'] == 'DQ8')
               , 'HLA: grupos de riesgo'] =  'DQ8 una dosis'
    df_aux.loc[ (df_aux['Haplotipo1'] == 'DQ7.5') & (df_aux['Haplotipo2'] == 'DQ2.2')
               , 'HLA: grupos de riesgo'] =  'DQ2.5 una dosis'
    df_aux.loc[ (df_aux['Haplotipo1'] == 'DQ2.2') & (df_aux['Haplotipo2'] == 'DQ7.5')
               , 'HLA: grupos de riesgo'] =  'DQ2.5 una dosis'
    df_aux.loc[ (df_aux['Haplotipo1'] == 'DQ2.5') | (df_aux['Haplotipo2'] == 'DQ2.5')
               , 'HLA: grupos de riesgo'] =  'DQ2.5 una dosis'
    df_aux.loc[ (df_aux['Haplotipo1'] == 'DQ2.2') & (df_aux['Haplotipo2'] == 'DQ2.5')
               , 'HLA: grupos de riesgo'] =  'DQ2.5 doble dosis'
    df_aux.loc[ (df_aux['Haplotipo1'] == 'DQ2.5') & (df_aux['Haplotipo2'] == 'DQ2.2')
               , 'HLA: grupos de riesgo'] =  'DQ2.5 doble dosis'
    df_aux.loc[ (df_aux['Haplotipo1'] == 'DQ2.5') & (df_aux['Haplotipo2'] == 'DQ2.5')
               , 'HLA: grupos de riesgo'] =  'DQ2.5 doble dosis'
    
    df_aux['HLA: grupos de riesgo'] = df_aux['HLA: grupos de riesgo'].fillna('HLA NO HECHO')
    df_aux = df_aux.drop(columns = ['Haplotipo1', 'Haplotipo2'])
    return df_aux 

'''
Function that formats LIEs %GD and LIEs %iNK
'''
def LIEs_DCG_formating(df_aux, columns, new_names, records_number):
    df_aux[columns] = df_aux[columns].fillna(-1)
    pd.concat([df_aux,pd.DataFrame(columns=new_names, index = range(records_number))])
    
    for i in range(records_number):
        vector = []
        for j in range(0, len(columns), 2):
            vector.append((float(df_aux.loc[i:i,columns[j]]), 
                           float(df_aux.loc[i:i,columns[j + 1]])))
    
        compatible = [x for x in vector if x[0] >= 10 and x[1] < 10]
        if len(compatible) > 0:
            x, y = max(compatible,key=lambda item:item[0])
        else :
            compatible_dsg = [x for x in vector if x[0] >= 10 and x[1] > 10]
            if len(compatible_dsg) > 0:
                x,y = max(compatible_dsg, key=lambda item:item[0])
            else :
                x,y = max(vector, key=lambda item:item[0])
                        
        df_aux.loc[i:i,new_names[0]] = x
        df_aux.loc[i:i,new_names[1]] = y
        
    df_aux = df_aux.drop(columns = columns)
    return df_aux
    
'''
Function that formats LIEs %GD and LIEs %iNK
'''
def LIEs_DSG_formating(df_aux, columns, new_names, records_number):
    df_aux[columns] = df_aux[columns].fillna(-1)
    pd.concat([df_aux,pd.DataFrame(columns=new_names, index = range(records_number))])
    
    for i in range(records_number):
        vector = []
        for j in range(0, len(columns), 2):
            vector.append((float(df_aux.loc[i:i,columns[j]]), 
                           float(df_aux.loc[i:i,columns[j + 1]])))
            
        vector = [x for x in vector if x[0] != -1 and x[1] != -1]
        if len(vector) > 0:
            no_compatible = [x for x in vector if x[0] < 10]
            if len(no_compatible) > 0:
                x,y = min(no_compatible,key=lambda item:item[0])
            else:
                compatible_dsg = [x for x in vector if x[0] >= 10 and x[1] > 10]
                if len(compatible_dsg) > 0:
                    x,y = min(compatible_dsg, key=lambda item:item[0])
                else:
                    x,y = min(vector, key=lambda item:item[0])
                        
            df_aux.loc[i:i,new_names[0]] = x
            df_aux.loc[i:i,new_names[1]] = y
        else:
            df_aux.loc[i:i,new_names[0]] = -1
            df_aux.loc[i:i,new_names[1]] = -1
        
    df_aux = df_aux.drop(columns = columns)
    return df_aux
    

'''
Function that fix the EMA columns
'''
def proces_EMA_column(df_aux, columnName):
    aux = df_aux[columnName]
    aux2 = []
    for i in range(0, len(aux)):
        if pd.isna(aux[i]):
            aux2.append(aux[i])
        else:
            aux2.append(aux[i].split()[0])
    
    aux2 = pd.DataFrame(aux2).replace('No', "No hecho")
    aux2 = aux2.replace(np.nan, "No hecho")
    
    df_aux[columnName] = aux2
    
    return df_aux


'''
Function that makes the filtering by columns
'''
def filtering (df_aux):
    
    records_number = df_aux.iloc[:,0].size
    
    df_aux = countries_preprocesing(df_aux, european_countries, records_number)

    df_aux = proces_EMA_column(df_aux, "DCG EMA")
    
   # df_aux = fill_nan_with_zero_and_scale(df_aux, fill_nan_with_zero_column_names)

    df_aux = HLA_formating(df_aux)
    
    
    for column in take_the_highest_value_columns.values():
        df_aux = take_highest_value(df_aux, column[0], column[1], column[2],
                                    column[3], column[4], column[5])
    
    df_aux = LIEs_DCG_formating(df_aux, lies_dcg_numerical[0], lies_dcg_numerical[1],
                                records_number)
    
    df_aux = LIEs_DSG_formating(df_aux, lies_dsg_numerical[0], lies_dsg_numerical[1],
                                records_number)
        
    #for column in columns_to_be_joined.values():
    #    df_aux = take_last_column_avaliable(df_aux, column)

    
    #df_aux = process_kindship(df_aux)
    #df_aux = simple_process_columns_to_binary(df_aux, simple_process_column_names)
    
    #for column in column_to_binary_column_names.values():
    #    df_aux = change_column_to_binary(df_aux, column)
    
    #df_aux = df_aux.loc[:,~df_aux.columns.duplicated()]
    #for column in process_column_names.values():
    #    df_aux = process_columns_to_binary(df_aux,column[1], records_number, column[0])
    
    return df_aux



def main():
    #df = read_data_from_local()
    df = read_new_data_from_local()
    df_aux = df
    df_aux = selectImportantColumns(df_aux)
    df_aux.to_excel("unfilterData.xlsx")

    df_aux = filtering(df_aux)
    
    df_aux.to_excel("filterData.xlsx")
    

if __name__ == "__main__":
    main()
    
    
    
    