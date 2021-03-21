"""
Created on Wed Feb 24 16:29:51 2021

@author: pablo
@author: carla
"""

import pandas as pd
import numpy as np
from utils import european_countries, take_the_highest_value_columns, lies_dcg_numerical,lies_dsg_numerical
from utils import lies_valoracion, biopsias_AP, biopsias_LIEs, dates, biopsias_delete_dsg, join_biopsias
from utils import process_column_names, fill_nan_value
import datetime as dt
import operator

##################################################################
#           IMPORT DATA
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

'''
Given a file with the relevant columns name, it selects them in the dataframe
'''
def selectImportantColumns(df_aux):
    important_columns = read_columns_from_local()
    important_columns = list(important_columns.iloc[:,1])
    df_aux = df_aux.loc[:,important_columns]
    return df_aux

##################################################################
#           PROCESS KINDSHIP
##################################################################
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

##################################################################
#           PROCESS IMMUNOLOGICAL DESEASES
#           PROCESS SYMPTOMS
#           PROCESS SIGNS
##################################################################
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

##################################################################
#           PROCESS GENDER
#           PROCESS HELICOBACTER PILORY
##################################################################
'''
Function that fills the nan cells with nan_value
'''
def fill_nan_with_value(df_aux, column, nan_value):
    df_aux[column] = df_aux[column].fillna(nan_value)
    return df_aux

##################################################################
#           PROCESS NACIONALITY
##################################################################
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

##################################################################
#           PROCESS HLA AND HAPLOTIPOS
##################################################################
'''
Function that formats HLA
'''
def HLA_formating(df_aux):
    data = np.array([(operator.or_, 'SIN RIESGO', 'SIN RIESGO', 'SIN RIESGO'),
            (operator.or_, 'DQ7.5', 'DQ7.5', 'DQ7.5'), (operator.or_, 'DQ2.2', 'DQ2.2', 'DQ2.2'), 
            (operator.and_, 'DQ8', 'DQ8', 'DQ8 doble dosis'), (operator.or_, 'DQ8', 'DQ8', 'DQ8 una dosis'), 
            (operator.and_, 'DQ7.5', 'DQ2.2', 'DQ2.5 una dosis'), (operator.and_,'DQ2.2', 'DQ7.5','DQ2.5 una dosis'), 
            (operator.or_, 'DQ2.5', 'DQ2.5', 'DQ2.5 una dosis'), (operator.and_, 'DQ2.2', 'DQ2.5', 'DQ2.5 doble dosis'), 
            (operator.and_,'DQ2.5', 'DQ2.2', 'DQ2.5 doble dosis'), (operator.and_, 'DQ2.5', 'DQ2.5', 'DQ2.5 doble dosis')])
    
    for element in data:
        df_aux.loc[element[0]((df_aux['Haplotipo1'] == element[1]) ,(df_aux['Haplotipo2'] == element[2]))
               , 'HLA: grupos de riesgo'] = element[3]
    
    df_aux['HLA: grupos de riesgo'] = df_aux['HLA: grupos de riesgo'].fillna('HLA NO HECHO')
    df_aux = df_aux.drop(columns = ['Haplotipo1', 'Haplotipo2'])
    return df_aux 

##################################################################
#           PROCESS LIEs DCG %GD, LIEs DCG %iNK
#           PROCESS LIEs DSG %GD, LIEs DSG %iNK
#           PROCESS Valoración DCG LIEs
#           PROCESS Valoración DSG LIEs
##################################################################
'''
Function that formats columns "LIEs DCG %GD_1  ", "LIEs DCG %iNK_1  ", "LIEs DCG %GD_2  ", 
"LIEs DCG %iNK_2  "
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
Function that formats "LIEs DSG %GD_1  ", "LIEs DSG %iNK_1  ", "LIEs DSG %GD_2  ", 
"LIEs DSG %iNK_2  ", "LIEs DSG %GD_3  ", "LIEs DSG %iNK_3  "
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
Function that join columns, in column new_name, with null_value for the nan 
giving priority to values
'''
def join_columns(df_aux, columns, new_name,null_value, values,records_number):
    pd.concat([df_aux,pd.DataFrame(columns=new_name, index = range(records_number))])
    df_aux[new_name] =null_value 

    for i in range(records_number):
        for value in values:
            aux = 0
            for column in columns:
                if df_aux[column].iloc[i] == value :
                   df_aux.loc[i:i, new_name] = value
                   aux = 1
                   break;
            if aux == 1: break
           
    df_aux = df_aux.drop(columns = columns)

    return df_aux


def process_LIEs (df_aux, records_number):
    df_aux = LIEs_DCG_formating(df_aux, lies_dcg_numerical[0], lies_dcg_numerical[1],
                                records_number)
    
    df_aux = LIEs_DSG_formating(df_aux, lies_dsg_numerical[0], lies_dsg_numerical[1],
                                records_number)
    
    for value in lies_valoracion.values():
        df_aux = join_columns(df_aux, value[0], value[1], 
                                           value[2][0],value[3], records_number)
    return df_aux

##################################################################
#           PROCESS DCG Biopsia, DSG Biopsia, Biopsia DCG LIEs, Biopsia DCG LIEs
##################################################################

'''
Function that preprocesses columns "DCG Biopsia-AP1  ", "DCG Biopsia-AP2  ", 
["DSG Biopsia AP1", "DSG Biopsia AP2". It converts M3b/c in M3v and fills 
nan values with "Sin biopsia hecha"
'''    
def preprocess_Biopsias_AP(df_aux, columns, current_nan_value, final_nan_value, records_number):
    
    for i in range(records_number):
            for column in columns:
                if ((str(df_aux[column].iloc[i]) != "nan") and
                    (str(df_aux[column].iloc[i]) != current_nan_value) and
                    (len(str(df_aux[column].iloc[i])) > 2)):
                    df_aux.loc[i:i, column] = str(df_aux[column].iloc[i])[0:3]
                    
                if str(df_aux[column].iloc[i]) == current_nan_value:
                    df_aux.loc[i:i, column] = final_nan_value
                   
    df_aux[columns] = df_aux[columns].fillna(final_nan_value)
    
    return df_aux

'''
Function that preprocesses columns "AP Biopsia DCG LIEs_1  ", "AP en Biopsia DCG LIEs_2  ", 
"AP Biopsia DSG LIEs_1  ", "AP en Biopsia DSG LIEs_2  ", "AP en Biopsia DSG LIEs_3  ". 
It changes Marsh 0 and Marsh 1 to M0, M1. And deletes information about Helicobacter
pilory that follows the result of the Biopsy after "-".
'''
def preprocess_Biopsias_LIEs(df_aux, columns, nan_value, records_number):
    
    for i in range(records_number):
            for column in columns:
                if ((str(df_aux[column].iloc[i]) != "nan") and
                    (len(str(df_aux[column].iloc[i])) > 2)):
                    s = str(df_aux[column].iloc[i])
                    s = s.replace("Marsh ", "M")
                    index = s.rfind("-")
                    if index != -1:
                        df_aux.loc[i:i, column] = s[0:index]
                    else:
                        df_aux.loc[i:i, column] = s

    df_aux[columns] = df_aux[columns].fillna(nan_value)
    
    return df_aux

'''
Function that converts the dates in seconds since epoch.
'''
def preprocess_dates(df_aux, columns):
    for column in columns:
        df_aux[column]= pd.to_datetime(df_aux[column],format='%d/%m/%y', errors='coerce')
        df_aux[column]=(df_aux[column] - dt.datetime(1970,1,1)).dt.total_seconds()
    df_aux[columns] = df_aux[columns].fillna(0)
    return df_aux

'''
Function that deletes DSG biopsies that where made with less than 6 months since
the last DCG biopsy. 
'''
def delete_DSG_biopsias(df_aux, dcg_dates, dsg_dates, dsg_biopsias, records_number):
    pd.concat([df_aux,pd.DataFrame(columns=['max_dcg'], index = range(records_number))])
    df_aux['max_dcg'] = df_aux[dcg_dates].max(axis=1)
    for i in range(len(dsg_dates)):
        df_aux[dsg_biopsias[i]] = df_aux[dsg_biopsias[i]]
        df_aux.loc[df_aux[dsg_dates[i]] - df_aux['max_dcg'] < 15811171, 
                   dsg_biopsias[i]] = "Sin biopsia hecha"
        
    df_aux = df_aux.drop(columns=['max_dcg'])
    df_aux = df_aux.drop(columns=dcg_dates)
    df_aux = df_aux.drop(columns=dsg_dates)
    return df_aux

def process_biopsias(df_aux, records_number):
    for value in biopsias_AP.values():
        df_aux = preprocess_Biopsias_AP(df_aux, value[0], value[1][0], value[2][0],
                                     records_number)
    for value in biopsias_LIEs.values():
        df_aux = preprocess_Biopsias_LIEs(df_aux, value[0], value[1][0], 
                                          records_number)
        
    df_aux = preprocess_dates(df_aux, dates)
        
    df_aux = delete_DSG_biopsias(df_aux,biopsias_delete_dsg[0], biopsias_delete_dsg[1],
                                 biopsias_delete_dsg[2], records_number)
    
    for value in join_biopsias.values():
        df_aux = join_columns(df_aux, value[0], value[1], 
                                           value[2][0],value[3],records_number)
    return df_aux

##################################################################
#           PROCESS DCG EMA, DSG EMA
##################################################################

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
    
    df_aux = process_kindship(df_aux)
    
    for element in fill_nan_value.values():
        df_aux = fill_nan_with_value(df_aux, element[0], element[1])
    
    for column in process_column_names.values():
        df_aux = process_columns_to_binary(df_aux,column[1], records_number, column[0])
        
    
    df_aux = proces_EMA_column(df_aux, "DCG EMA")

    df_aux = HLA_formating(df_aux)    
    
    for column in take_the_highest_value_columns.values():
        df_aux = take_highest_value(df_aux, column[0], column[1], column[2],
                                    column[3], column[4], column[5])
    
    df_aux = df_aux.loc[:,~df_aux.columns.duplicated()]
    
    df_aux = process_LIEs(df_aux, records_number)
    
    df_aux = process_biopsias(df_aux, records_number)
            
    return df_aux



def main():
    df = read_new_data_from_local()
    df_aux = df
    df_aux = selectImportantColumns(df_aux)
    df_aux.to_excel("unfilterData.xlsx")

    df_aux = filtering(df_aux)
    
    df_aux.to_excel("filterData.xlsx")
    

if __name__ == "__main__":
    main()
    
    
    
    