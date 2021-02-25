#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 16:29:51 2021

@author: pablo
"""

import pandas as pd
import numpy as np


#Función que comprueba
def comprobarParentesco (data_aux, cadena):
    for i in range (0, len(cadena)):
        if ~ cadena[i].isalnum():
            if '1' in cadena[i]:
                data_aux.loc[:,'1º grado'].iloc[i] = 1
            elif '2' in cadena[i]:
                data_aux.loc[:,'2º grado'].iloc[i] = 1
            elif '3' in cadena[i]:
                data_aux.loc[:,'3º grado'].iloc[i] = 1
            elif '4' in cadena[i]:
                data_aux.loc[:,'4º grado'].iloc[i] = 1
            
    return data_aux


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





data=pd.read_csv(
    '/Users/pablo/Desktop/Universidad/5/TFG/Informática/Datos.csv')

#Creo una nueva tabla auxiliar que será la que vamos a limpiar a partir de la original
data_aux = data


total_pacientes = data.iloc[:,0].size
lista_columnas = data.columns

'''
print(data.head())
print(data.info())
print(data.describe())
'''




'''Insertar columnas que reflejen si el paciente
tiene en la familia personas diagnosticadas.
Hay 4 grados de parentescos posibles. 
Por lo tanto, creamos 4 columnas y en cada una poner 0 si no tienen
 ningún familiar de ese grado diagnosticado o 1 en caso contrario'''


#Creo las 4 columnas extras y las relleno de 0s
data_aux = data_aux.reindex (columns = data_aux.columns.tolist() +
                             ['1º grado','2º grado','3º grado', '4º grado'])
data_aux.loc[:, ['1º grado','2º grado','3º grado', '4º grado']] = 0


#En la tabla original había dos columnas de parentesco
columna_parentesco1 = data.loc[:,'Grado de parentesco']
columna_parentesco2 = data.loc[:,
        'Grado de parentesco (si hay más de 1)']

#Relleno con 0s en forma de string los valores qué eran nan para que no se lie
columna_parentesco1 = columna_parentesco1.fillna("0")
columna_parentesco2 = columna_parentesco2.fillna("0")

#A partir de las 2 columnas anteriores relleno las 4 columnas extras
data_aux = comprobarParentesco(data_aux, columna_parentesco1)
data_aux = comprobarParentesco(data_aux, columna_parentesco2)





'''Filtrado de enfermedad inmunológica'''

#Selecciono todas las columnas que tengan enfermedades inmunologicas
columna_inmunologica1 = data.loc[:,'Enfermedad inmunológica'].dropna()
columna_inmunologica2 = data.loc[:, 
                'Enfermedad inmunológica (si hay más de 1)'].dropna()
columna_inmunologica3 = data.loc[:,
                'Enfermedad inmunológica (si hay más de 2)'].dropna()

#Creo una lista de enfermedades inmunologicas unicas
columna_inmunologica = pd.concat([columna_inmunologica1,
                                  columna_inmunologica2,
                                  columna_inmunologica3], axis = 0)
columna_inmunologica = pd.unique(columna_inmunologica)

'''Creo un dataframe con las columnas de las enfermedades
 y todas las casillas inicializadas a 0'''
data_inmunologia = pd.DataFrame(columns = columna_inmunologica,
                                index = range(total_pacientes))
data_inmunologia.iloc[:,:] = 0


columna_inmunologica = pd.Series(columna_inmunologica)
nombresColumnasAAnalizar = ['Enfermedad inmunológica',
                            'Enfermedad inmunológica (si hay más de 1)',
                            'Enfermedad inmunológica (si hay más de 2)']

#Relleno el nuevo dataframe
data_inmunologia = rellenarCasillas (data, total_pacientes,
              columna_inmunologica, nombresColumnasAAnalizar, data_inmunologia)

#Junto los dos dataframe
data_aux = pd.concat([data_aux, data_inmunologia], axis = 1)



    



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

    
    
    



