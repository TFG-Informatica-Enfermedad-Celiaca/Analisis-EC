# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 13:42:38 2021

@author: Carla
@author: Pablo
"""
import pandas as pd
##################################################################
#           IMPORT Datos actualizados and Important columns
#           This functions are used in Filtrado.py
##################################################################
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


##################################################################
#           IMPORT filterData and filterDataNumerical
#           This functions are used in kprototypes.py
##################################################################
'''
Read the relevant columns form .xlsx stored in local and creates deaframe
'''
def read_data_from_local():
    try:
        df=pd.read_excel(
            '/Users/pablo/Desktop/Universidad/5/TFG/Informática/Codigo/filterData.xlsx')
        return df
    except:
        try:
            df=pd.read_excel(
                r'C:\Users\Carla\Desktop\TFG-Informatica\filterData.xlsx')
            return df
        except:
            print("It was not possible to load data 2")

def read_numerical_data_from_local():
    try:
        df=pd.read_excel(
            '/Users/pablo/Desktop/Universidad/5/TFG/Informática/Codigo/filterDataNumerical.xlsx')
        return df
    except:
        try:
            df=pd.read_excel(
                r'C:\Users\Carla\Desktop\TFG-Informatica\filterDataNumerical.xlsx')
            return df
        except:
            print("It was not possible to load data 2")