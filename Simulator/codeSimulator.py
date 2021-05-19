#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 18 21:02:31 2021

@author: pablo
"""

import pandas as pd
import numpy as np
import random


def read_columns_from_local():
    try:
        df=pd.read_excel(
            '/Users/pablo/Desktop/Universidad/5/TFG/Informática/Código/Important columns.xlsx')
        return df
    except:
        try:
            df=pd.read_excel(
                r'C:\Users\Carla\Desktop\TFG-Informatica\Analisis-EC\Important columns.xlsx')
            return df
        except:
            print("It was not possible read the columns names")





def random_colum(column):
    random_c = []
    for i in range(0, 500):
      random_c += [random.choice(column)]
    return random_c


def posNegativeValue(df, value_column, pos_neg_col, pos_neg):
    df[value_column] = random_colum(pos_neg)
    df[pos_neg_col] = np.where((df[value_column] == "Negativo"),
                              np.random.randint(0, 20, 500),
                              np.random.randint(20, 300, 500))
    return df



def check_HLA(df):
    if((df['HLA: grupos de riesgo'] == 'DQ8 doble dosis') |
    (df['HLA: grupos de riesgo'] == 'DQ8 una dosis') |
    (df['HLA: grupos de riesgo'] == 'DQ2.5 una dosis')):
        return 1
    return 0


def check_sintoms_and_signs(df):
    if(((df['Síntomas específicos'] != "Otros (especificar en otros síntomas)") |
    (df['Síntomas específicos.1'] != "Otros (especificar en otros síntomas)")) &
    ((df['Signos  '] != "Nada") | (df['Signos 2  '] != "Nada"))):
        return 1
    return 0


def check_biopsy(df):
    if((df['Biopsia DCG'] == 'M3a') | (df['Biopsia DCG'] == 'M3b') |
     (df['Biopsia DCG'] == 'M3c')):
        return 1
    
    return 0
    

def check_response_to_DSG(df):
    if((check_biopsy(df) &  (df['Biopsia DSG'] == 'M0')) |
       (check_ATG(df) & (df['DSG ATG2 VALUE'] == "Negativo"))):
        return 1
    return 0


def check_ATG(df):
    if((df['DCG_ATG2_VALUE'] == 'Positivo')):
        return 1
    return 0


def check_compatibility(df):
    compatiblity = 0
    if(check_HLA(df)):
        compatiblity += 1
    '''
    if(check_sintoms_and_signs(df)):
        compatiblity += 1
    if(check_biopsy(df)):
        compatiblity += 1
    if(check_response_to_DSG(df)):
        compatiblity += 1
    if(check_ATG(df)):
        compatiblity += 1
    '''
    
    if(compatiblity > 3):
        return 1
            
    return 0
    

def diagnostic(df):
    
    df['Diagnóstico'] = np.where((
        (((df['HLA: grupos de riesgo'] == 'DQ8 doble dosis') |
    (df['HLA: grupos de riesgo'] == 'DQ8 una dosis') |
    (df['HLA: grupos de riesgo'] == 'DQ2.5 una dosis')) & 
         (((df['Síntomas específicos'] != "Otros (especificar en otros síntomas)") |
    (df['Síntomas específicos.1'] != "Otros (especificar en otros síntomas)")) &
    ((df['Signos  '] != "Nada") | (df['Signos 2  '] != "Nada")) &
    (((df['Síntomas específicos'] != "Otros (especificar en otros síntomas)") |
    (df['Síntomas específicos.1'] != "Otros (especificar en otros síntomas)"))) &
    ((df['Signos  '] != "Nada") | (df['Signos 2  '] != "Nada"))) &
    ((df['Biopsia DCG'] == 'M3a') | (df['Biopsia DCG'] == 'M3b') |
     (df['Biopsia DCG'] == 'M3c')) &
    ((df['DCG_ATG2_VALUE'] == 'Positivo')) &
    ((((df['Biopsia DCG'] == 'M3a') | (df['Biopsia DCG'] == 'M3b') |
     (df['Biopsia DCG'] == 'M3c')) &  (df['Biopsia DSG'] == 'M0')) |
       (((df['DCG_ATG2_VALUE'] == 'Positivo')) & (df['DSG ATG2 VALUE'] == "Negativo")))) |
        
    (((df['HLA: grupos de riesgo'] == 'DQ8 doble dosis') |
    (df['HLA: grupos de riesgo'] == 'DQ8 una dosis') |
    (df['HLA: grupos de riesgo'] == 'DQ2.5 una dosis')) & 
         (((df['Síntomas específicos'] != "Otros (especificar en otros síntomas)") |
    (df['Síntomas específicos.1'] != "Otros (especificar en otros síntomas)")) &
    ((df['Signos  '] != "Nada") | (df['Signos 2  '] != "Nada")) &
    (((df['Síntomas específicos'] != "Otros (especificar en otros síntomas)") |
    (df['Síntomas específicos.1'] != "Otros (especificar en otros síntomas)"))) &
    ((df['Signos  '] != "Nada") | (df['Signos 2  '] != "Nada"))) &
    ((df['Biopsia DCG'] == 'M3a') | (df['Biopsia DCG'] == 'M3b') |
     (df['Biopsia DCG'] == 'M3c')) &
    ((df['DCG_ATG2_VALUE'] == 'Positivo')))   |
    
    (((df['HLA: grupos de riesgo'] == 'DQ8 doble dosis') |
    (df['HLA: grupos de riesgo'] == 'DQ8 una dosis') |
    (df['HLA: grupos de riesgo'] == 'DQ2.5 una dosis')) & 
         (((df['Síntomas específicos'] != "Otros (especificar en otros síntomas)") |
    (df['Síntomas específicos.1'] != "Otros (especificar en otros síntomas)")) &
    ((df['Signos  '] != "Nada") | (df['Signos 2  '] != "Nada")) &
    (((df['Síntomas específicos'] != "Otros (especificar en otros síntomas)") |
    (df['Síntomas específicos.1'] != "Otros (especificar en otros síntomas)"))) &
    ((df['Signos  '] != "Nada") | (df['Signos 2  '] != "Nada"))) &
    ((df['Biopsia DCG'] == 'M3a') | (df['Biopsia DCG'] == 'M3b') |
     (df['Biopsia DCG'] == 'M3c')) &
    ((((df['Biopsia DCG'] == 'M3a') | (df['Biopsia DCG'] == 'M3b') |
     (df['Biopsia DCG'] == 'M3c')) &  (df['Biopsia DSG'] == 'M0')) |
       (((df['DCG_ATG2_VALUE'] == 'Positivo')) & (df['DSG ATG2 VALUE'] == "Negativo"))))   |
    
    (((df['HLA: grupos de riesgo'] == 'DQ8 doble dosis') |
    (df['HLA: grupos de riesgo'] == 'DQ8 una dosis') |
    (df['HLA: grupos de riesgo'] == 'DQ2.5 una dosis')) & 
         (((df['Síntomas específicos'] != "Otros (especificar en otros síntomas)") |
    (df['Síntomas específicos.1'] != "Otros (especificar en otros síntomas)")) &
    ((df['Signos  '] != "Nada") | (df['Signos 2  '] != "Nada")) &
    (((df['Síntomas específicos'] != "Otros (especificar en otros síntomas)") |
    (df['Síntomas específicos.1'] != "Otros (especificar en otros síntomas)"))) &
    ((df['Signos  '] != "Nada") | (df['Signos 2  '] != "Nada"))) &
    ((df['DCG_ATG2_VALUE'] == 'Positivo')) &
    ((((df['Biopsia DCG'] == 'M3a') | (df['Biopsia DCG'] == 'M3b') |
     (df['Biopsia DCG'] == 'M3c')) &  (df['Biopsia DSG'] == 'M0')) |
       (((df['DCG_ATG2_VALUE'] == 'Positivo')) & (df['DSG ATG2 VALUE'] == "Negativo"))))   |
    
    (((df['HLA: grupos de riesgo'] == 'DQ8 doble dosis') |
    (df['HLA: grupos de riesgo'] == 'DQ8 una dosis') |
    (df['HLA: grupos de riesgo'] == 'DQ2.5 una dosis')) & 
    ((df['Biopsia DCG'] == 'M3a') | (df['Biopsia DCG'] == 'M3b') |
     (df['Biopsia DCG'] == 'M3c')) &
    ((df['DCG_ATG2_VALUE'] == 'Positivo')) &
    ((((df['Biopsia DCG'] == 'M3a') | (df['Biopsia DCG'] == 'M3b') |
     (df['Biopsia DCG'] == 'M3c')) &  (df['Biopsia DSG'] == 'M0')) |
       (((df['DCG_ATG2_VALUE'] == 'Positivo')) & (df['DSG ATG2 VALUE'] == "Negativo"))))  |
    
    ((((df['Síntomas específicos'] != "Otros (especificar en otros síntomas)") |
    (df['Síntomas específicos.1'] != "Otros (especificar en otros síntomas)")) &
    ((df['Signos  '] != "Nada") | (df['Signos 2  '] != "Nada")) &
    (((df['Síntomas específicos'] != "Otros (especificar en otros síntomas)") |
    (df['Síntomas específicos.1'] != "Otros (especificar en otros síntomas)"))) &
    ((df['Signos  '] != "Nada") | (df['Signos 2  '] != "Nada"))) &
    ((df['Biopsia DCG'] == 'M3a') | (df['Biopsia DCG'] == 'M3b') |
     (df['Biopsia DCG'] == 'M3c')) &
    ((df['DCG_ATG2_VALUE'] == 'Positivo')) &
    ((((df['Biopsia DCG'] == 'M3a') | (df['Biopsia DCG'] == 'M3b') |
     (df['Biopsia DCG'] == 'M3c')) &  (df['Biopsia DSG'] == 'M0')) |
       (((df['DCG_ATG2_VALUE'] == 'Positivo')) & (df['DSG ATG2 VALUE'] == "Negativo"))))
    
        
        
    
        
        
        )
        
        
        
        
        
        
        , "EC", "No EC")
    
    return df


def main():
    
    columns = read_columns_from_local()
    
    df = pd.DataFrame()
    
    pos_neg = ["Positivo", "Negativo", "Positivo", "Positivo", "Positivo"]

    
    
    df['Indique país de origen o en su defecto la información disponible'] = np.random.randint(0, 1, 500)
    df['Sexo'] = np.random.randint(0, 2, 500)
    df['Edad diagnóstico'] = np.random.randint(10, 90, 500)
    df['1º grado'] = np.random.randint(0, 2, 500)
    
    
    #HLA
    HLA = ['SIN RIESGO', 'DQ7.5', 'DQ2.2', 'DQ2.2',
           'DQ8', 'DQ8 doble dosis', 'DQ8 una dosis', 'DQ2.5 una dosis']
    df['HLA: grupos de riesgo'] = random_colum(HLA)
    
    
    
    df['DCG EMA'] = np.random.randint(0, 2, 500)
    
    
    #DCG ATG2
    df = posNegativeValue(df, 'DCG_ATG2_VALUE', 'DCG_ATG2', pos_neg)
    
    
    #DCG A-PDG
    df = posNegativeValue(df, 'DCG A-PDG_VALUE', 'DCG_ATG2', pos_neg)
    
    
    #DSG ATG2
    df = posNegativeValue(df, 'DSG ATG2 VALUE', 'DSG ATG2', pos_neg)
    
    #DSG A-PDG
    df = posNegativeValue(df, 'DSG A-PDG VALUE', 'DSG A-PDG', pos_neg)
    
    df['LIEs DCG %GD'] = np.random.randint(0, 75, 500)
    df['LIEs DCG %iNK'] = np.random.randint(0, 75, 500)
    df['LIEs DSG %GD'] = np.random.randint(0, 75, 500)
    df['LIEs DSG %iNK'] = np.random.randint(0, 75, 500)
    
    
    #Biopsias
    Biopsia = ['M0', 'M1', 'M2', 'M3a', 'M3b', 'M3c']
    df['Biopsia DCG'] = random_colum(Biopsia)
    df['Biopsia DSG'] = random_colum(Biopsia)
    
    
    #Sintomas y signos
    sintomns = ["Diarrea crónica", "Estreñimiento", "Distensión abdominal",
                "Dispepsia", "Vómitos", "Fibromialgia",
                "Otros (especificar en otros síntomas)"]
    df['Síntomas específicos'] = random_colum(sintomns)
    df['Síntomas específicos.1'] = random_colum(sintomns)
    
    signs = ["Hipertransaminasemia", "Anemia ferropénica o ferropenia",
             "Déf Vit B12", "Déficits nutricionales debidos a malabsorción",
             "Nada"]
    df['Signos  '] = random_colum(signs)
    df['Signos 2  '] = random_colum(signs)
    
    
    
    #Diagnostico
    df = diagnostic(df)

    
    
    
    
    
    df.to_excel("Simulación.xlsx", index = False)
    



if __name__ == "__main__":
    main()