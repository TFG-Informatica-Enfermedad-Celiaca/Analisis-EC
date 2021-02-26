#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 16:29:51 2021

@author: pablo
@author: carla
"""

import pandas as pd
import numpy as np


def main():
    df = read_data_from_local()
    df_aux = df
    records_number = df.iloc[:,0].size
    column = df.columns
    df_aux = process_kindship(df_aux)
    modified_data = process_data(data)
    write_data_to_database(modified_data)

if __name__ == "__main__":
    main()


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
    df_f.loc[:, ['1º grado','2º grado','3º grado', '4º grado']] = 0

    # In case there is a i-level of kindship it fills the column 'iº grado' with '1'
    for i in range(1, 4):
        df_aux.loc[df_aux['Grado de parentesco'].str.contains(str(i)) | 
            df_aux['Grado de parentesco (si hay más de 1)'].str.contains(str(i)), str(i)+'º grado'] = 1

    # Delete the previous columns releated to kindship
    df_aux.drop(columns=['Grado de parentesco', 'Grado de parentesco (si hay más de 1)'])
    return df_aux

'''
For each immunological desease we create a column. This column contains 0 in case
the patient does not suffer this desease and 1 in other case.
'''
def process_immunological_desease(df_aux):
    previous_columns = ['Enfermedad inmunológica', 'Enfermedad inmunológica (si hay más de 1)', 
                'Enfermedad inmunológica (si hay más de 2)']

    # Select the columns containing immunological deseases
    immunological_columns= pd.unique(df[[previous_columns].values.ravel('K'))
    # Filter out nan value in array
    immunological_columns = list(filter(lambda i: not i is np.nan, immunological_columns))

    # Add a new column per desease
    df_aux = df_aux.reindex (columns = df_aux.columns.tolist() +
                                immunological_columns)
    df_aux.loc[:, immunological_columns] = 0

    for i in range(0, len(immunological_columns)):
        for j in range(records_number):
            for z in range (0, len(previous_columns)):
                if (immunological_columns[i] == data.loc[:,
                                        previous_columns[z]].iloc[j]): 
                    data_aux.loc[:,immunological_columns[i]].iloc[j] = 1
    
    return df_aux


#Funcion que sirve para borrar casillas que pone algun string que se le pasa
def borrarOtrosSintomas (data, columna, columnaALimpiar, stringABorrar):
    indexNames = data[ data[columna] == 
                  stringABorrar].index
    # Delete these row indexes from dataFrame
    return columnaALimpiar.drop(indexNames , inplace=True)


'''Dado una lista de columnas, comprueba si cada uno de los pacientes
cumple la condición de cada columna. En caso afirmativo, escribe un 1'''
def rellenarCasillas (data, pacientesTotales,
                      listaColumnas, nombresColumnasAAnalizar, data_aux):
    for i in range(0, len(listaColumnas)):
        for j in range(pacientesTotales):
            for z in range (0, len(nombresColumnasAAnalizar)):
                if (listaColumnas[i] == data.loc[:,
                                        nombresColumnasAAnalizar[z]].iloc[j]): 
                    data_aux.loc[:,listaColumnas[i]].iloc[j] = 1
    return data_aux



#Creo una nueva tabla auxiliar que será la que vamos a limpiar a partir de la original
data_aux = data




'''
print(data.head())
print(data.info())
print(data.describe())
'''


'''Filtrado de enfermedad inmunológica'''




    



'''Filtrado de sintomas'''
#Selecciono todas las columnas que tengan sintomas
columna_sintomas1 = data.loc[:,'Síntomas específicos'].dropna()
columna_sintomas2 = data.loc[:, 
                'Síntomas específicos.1'].dropna()
columna_sintomas3 = data.loc[:,
                'Síntomas específicos.2'].dropna()
columna_sintomas4 = data.loc[:,
                'Otros síntomas'].dropna()

#Limpio las casillas en las que pone "otros sintomas"
borrarOtrosSintomas (data, 'Síntomas específicos',
                     columna_sintomas1, 'Otros (especificar en otros síntomas)')
borrarOtrosSintomas (data, 'Síntomas específicos.1',
                     columna_sintomas2, 'Otros (especificar en otros síntomas)')
borrarOtrosSintomas (data, 'Síntomas específicos.2',
                     columna_sintomas3, 'Otros (especificar en otros síntomas)')

#De la ultima columna solo cojo las casillas donde hay menos de 2 palabras porque si no se liaba mucho
indexNames = []
for index, value in columna_sintomas4.items():
    if len(value.split()) > 2:
        indexNames.append(index)
columna_sintomas4.drop(indexNames , inplace=True)


#Creo una lista de enfermedades inmunologicas unicas
columna_sintomas = pd.concat([columna_sintomas1,
                                  columna_sintomas2,
                                  columna_sintomas3,
                                  columna_sintomas4], axis = 0)
columna_sintomas = pd.unique(columna_sintomas)


'''Creo un dataframe con las columnas de los sintomas
 y todas las casillas inicializadas a 0'''
data_sintomas = pd.DataFrame(columns = columna_sintomas,
                             index=range(total_pacientes))
data_sintomas.iloc[:,:] = 0

columna_sintomas = pd.Series(columna_sintomas)

nombresColumnasAAnalizar = ['Síntomas específicos',
                            'Síntomas específicos.1',
                            'Síntomas específicos.2',
                            'Otros síntomas'] 

#Relleno el nuevo dataframe
data_sintomas = rellenarCasillas (data, total_pacientes,
              columna_sintomas, nombresColumnasAAnalizar, data_sintomas)

#Junto los dos dataframe
data_aux = pd.concat([data_aux, data_sintomas], axis = 1)

 


aux = data_aux.iloc[:, 170:231]

    
    
    



