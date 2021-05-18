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

def main():
    
    columns = read_columns_from_local()
    
    df = pd.DataFrame()
    
    pos_neg = ["Positivo", "Negativo"]
    
    
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
    
    
    df.to_excel("Simulación.xlsx", index = False)
    



if __name__ == "__main__":
    main()