"""
Created on Wed Feb 24 16:29:51 2021

@author: pablo
@author: carla
"""

import pandas as pd
import numpy as np
from utils import european_countries, take_the_highest_value_columns, lies_dcg_numerical,lies_dsg_numerical
from utils import lies_valoracion, biopsias_AP, biopsias_LIEs, dates, biopsias_delete_dsg, join_biopsias
from utils import process_column_names,fill_nan_value, take_the_lower_value_columns, to_drop_values
from utils import lies_valoracion_preprocess
import datetime as dt
import operator
from load_data import read_new_data_from_local, read_columns_from_local
'''
Given a file with the relevant columns name, it selects them in the dataframe
'''
def selectImportantColumns(df):
    important_columns = read_columns_from_local()
    important_columns = list(important_columns.iloc[:,1])
    df = df.loc[:,important_columns]
    return df

##################################################################
#           PROCESS KINDSHIP
##################################################################
'''
Insert columns in the dataframe that show if the patient has celiac family. 
There are 4 levels of kindship so we create 4 columns, each of which contains
0 in case there isn't any celiac relative in that level or 1 in other case.
'''
def process_kindship(df):
    # Create 4 extra columns and fill them with 0s
    new_columns = ['1º grado','2º grado','3º grado', '4º grado']
    for column in new_columns:
        if (column not in df.columns):
            df.insert(len(df.columns), column, 0)

    # In case there is a i-level of kindship it fills the column 'iº grado' with '1'
    for i in range(1, 4):
        df.loc[df['Grado de parentesco'].str.contains(str(i)) | 
            df['Grado de parentesco (si hay más de 1)'].str.contains(str(i)), str(i)+'º grado'] = 1

    # Delete the previous columns releated to kindship
    df = df.drop(columns=['Grado de parentesco', 'Grado de parentesco (si hay más de 1)'])
    return df

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
def process_columns_to_binary(df, delete_more, records_number, previous_columns):
    # Create an array containing the values in previous_colums 
    new_columns= pd.unique(df[previous_columns].values.ravel('K'))
    # Filter out nan value and delete_more in array
    new_columns = list(filter(lambda i: not i in [np.nan] + delete_more, new_columns))
    
    df =  fill_table(new_columns, records_number, previous_columns, df)             
    
    # Delete previous columns 
    df = df.drop(columns=previous_columns)
    return df

##################################################################
#           PROCESS GENDER
#           PROCESS HELICOBACTER PILORY
##################################################################
'''
Function that fills the nan cells with nan_value
'''
def fill_nan_with_value(df, column, nan_value):
    df[column] = df[column].fillna(nan_value)
    return df

##################################################################
#           PROCESS NACIONALITY
##################################################################
'''
Function that group countries by European or not
'''
def countries_preprocesing(df, european_countries, records_number):
    
    df["Indique país de origen o en su defecto la información disponible"] = df[
        "Indique país de origen o en su defecto la información disponible"
        ].replace(np.nan, "Desconocido")
    df["Indique país de origen o en su defecto la información disponible"] = df[
        "Indique país de origen o en su defecto la información disponible"
        ].replace(european_countries, "Europeo")

    df.loc[(df["Indique país de origen o en su defecto la información disponible"]
        != "Europeo") & 
        (df["Indique país de origen o en su defecto la información disponible"]
        != "Desconocido"),
        "Indique país de origen o en su defecto la información disponible"
        ] = "Otro" 

    return df


'''
Function that fill the empty values and remove the old columns and
 concate the new ones with the hole dataframe
'''
def fill_and_concatenate_columns(df, aux, columns_to_delete,
                                 kitsAccepted, finalName1, finalName2, cut_point):
    
    df = df.drop(columns= (columns_to_delete))
    df = pd.concat([df, aux], axis = 1)
    
    #Fix the input errors
    df.loc[df[finalName2[0]] < cut_point, finalName1[0]] = "Negativo"
    df.loc[df[finalName2[0]] > cut_point, finalName1[0]] = "Positivo"
    
    df[finalName1[0]] = df[finalName1[0]].fillna("No hecho")
    df[finalName2[0]] = df[finalName2[0]].fillna(-1)
    
    return df


'''
Check if there is a valid kit
'''
def check_kits(df, kits, kitOK):
    kitsAccepted = [] 
    for i in kits:
        aux = df[df[i] == kitOK[0]].index.tolist()
        kitsAccepted.append(aux)
        kitsAccepted = np.unique(kitsAccepted)
    
    return kitsAccepted

'''
Functions that join several columns and take the higher values 
'''
def take_highest_value(df, posOrNeg, numericalValues, kits,
                       kitOK, finalName1, finalName2, cut_point):
   
    #Check the kits
    kitsAccepted = check_kits(df, kits, kitOK) 
    
    #Take the most positive values of each rows
    auxPorN = pd.DataFrame(index=range(len(df.loc[:,posOrNeg[0]])),columns=range(1)).squeeze()
    for i in posOrNeg:
        aux = []
        for j in range(len(df.loc[:,posOrNeg[0]])):
            if (df.loc[:,i].iloc[j] == "Positivo") or (
                    (str(auxPorN[j]) == 'nan') & (df.loc[:,i].iloc[j] != 'No hechos')):
                aux.append(df.loc[:,i].iloc[j])
            else:
                aux.append(auxPorN[j])
        auxPorN = aux
    
    #Take the highest numerical values of each rows
    corrValu = df.loc[:,numericalValues[0]]
    for i in numericalValues:
        aux = []
        for j in range(len(corrValu)):
            if (df.loc[:,i].iloc[j] > corrValu[j]) or (
                    str(corrValu[j]) == 'nan'):
                aux.append(df.loc[:,i].iloc[j])
            else:
                aux.append(corrValu[j])
        corrValu = aux
    
    #insert the new columns into the dataframe and remove the old ones
    aux = pd.DataFrame({finalName1[0]:auxPorN, finalName2[0]:corrValu})
    columns_to_delete = posOrNeg + numericalValues + kits
    df = fill_and_concatenate_columns(df, aux,
            columns_to_delete, kitsAccepted, finalName1, finalName2, cut_point)
    
    return df



'''
Functions that join several columns and take the lower values 
'''
def take_lower_value(df, posOrNeg, numericalValues, kits,
                       kitOK, finalName1, finalName2, cut_point):
    
    #Check the kits
    kitsAccepted = check_kits(df, kits, kitOK) 
    
    #Take the least positive values of each rows
    auxPorN = pd.DataFrame(index=range(len(df.loc[:,posOrNeg[0]])),columns=range(1)).squeeze()
    for i in posOrNeg:
        aux = []
        for j in range(len(df.loc[:,posOrNeg[0]])):
            if (df.loc[:,i].iloc[j] == "Negativo") or (
                    (str(auxPorN[j]) == 'nan') & (df.loc[:,i].iloc[j] != 'No hechos')):
                aux.append(df.loc[:,i].iloc[j])
            else:
                aux.append(auxPorN[j])
        auxPorN = aux
    
    #Take the lowest numerical values of each rows
    corrValu = df.loc[:,numericalValues[0]]
    for i in numericalValues:
        aux = []
        for j in range(len(corrValu)):
            if (df.loc[:,i].iloc[j] < corrValu[j]) or (
                    str(corrValu[j]) == 'nan'):
                aux.append(df.loc[:,i].iloc[j])
            else:
                aux.append(corrValu[j])
        corrValu = aux
    
    #insert the new columns into the dataframe and remove the old ones
    aux = pd.DataFrame({finalName1[0]:auxPorN, finalName2[0]:corrValu})
    columns_to_delete = posOrNeg + numericalValues + kits
    df = fill_and_concatenate_columns (df, aux,
            columns_to_delete, kitsAccepted, finalName1, finalName2, cut_point)
    
    return df

##################################################################
#           PROCESS HLA AND HAPLOTIPOS
##################################################################
'''
Function that formats HLA
'''
def HLA_formating(df):
    data = np.array([(operator.or_, 'SIN RIESGO', 'SIN RIESGO', 'SIN RIESGO'),
            (operator.or_, 'DQ7.5', 'DQ7.5', 'DQ7.5'), (operator.or_, 'DQ2.2', 'DQ2.2', 'DQ2.2'), 
            (operator.and_, 'DQ8', 'DQ8', 'DQ8 doble dosis'), (operator.or_, 'DQ8', 'DQ8', 'DQ8 una dosis'), 
            (operator.and_, 'DQ7.5', 'DQ2.2', 'DQ2.5 una dosis'), (operator.and_,'DQ2.2', 'DQ7.5','DQ2.5 una dosis'), 
            (operator.or_, 'DQ2.5', 'DQ2.5', 'DQ2.5 una dosis'), (operator.and_, 'DQ2.2', 'DQ2.5', 'DQ2.5 doble dosis'), 
            (operator.and_,'DQ2.5', 'DQ2.2', 'DQ2.5 doble dosis'), (operator.and_, 'DQ2.5', 'DQ2.5', 'DQ2.5 doble dosis')])
    
    for element in data:
        df.loc[element[0]((df['Haplotipo1'] == element[1]) ,(df['Haplotipo2'] == element[2]))
               , 'HLA: grupos de riesgo'] = element[3]
    
    df['HLA: grupos de riesgo'] = df['HLA: grupos de riesgo'].fillna('HLA NO HECHO')
    df = df.drop(columns = ['Haplotipo1', 'Haplotipo2'])
    return df

##################################################################
#           PROCESS LIEs DCG %GD, LIEs DCG %iNK
#           PROCESS LIEs DSG %GD, LIEs DSG %iNK
#           PROCESS Valoración DCG LIEs
#           PROCESS Valoración DSG LIEs
##################################################################
'''
Preprocess valoracion LIEs. If there is a value in the numerical column 
then we fill Valoracion column with "Resultado no claro"
'''
def preprocess_LIEs_valoracion(df):
    for item in lies_valoracion_preprocess:
        df.loc[((df[item[0]] >= 10)  & (df[item[1]]< 10)) & (df[item[2]].isnull()),
               item[2]]= "Compatible con EC activa"
        df.loc[((df[item[0]] >= 10)  & (df[item[1]]> 10)) & (df[item[2]].isnull()),
               item[2]]= "Compatible con EC en DSG"
        df.loc[(df[item[0]] < 10) & (df[item[2]].isnull()),
               item[2]]= "No compatible con EC"
        #df.loc[(~df[item[0]].isnull()) & (~df[item[1]].isnull())& (df[item[2]].isnull()),
        #       item[2]]= "Resultado no claro"

    return df
'''
Function that formats columns "LIEs DCG %GD_1  ", "LIEs DCG %iNK_1  ", "LIEs DCG %GD_2  ", 
"LIEs DCG %iNK_2  "
'''
def LIEs_DCG_formating(df, columns, new_names, records_number):
    df[columns] = df[columns].fillna(-1)
    pd.concat([df,pd.DataFrame(columns=new_names, index = range(records_number))])
    
    for i in range(records_number):
        vector = []
        for j in range(0, len(columns), 2):
            vector.append((float(df.loc[i:i,columns[j]]), 
                           float(df.loc[i:i,columns[j + 1]])))
    
        compatible = [x for x in vector if x[0] >= 10 and x[1] < 10]
        if len(compatible) > 0:
            x, y = max(compatible,key=lambda item:item[0])
        else :
            compatible_dsg = [x for x in vector if x[0] >= 10 and x[1] > 10]
            if len(compatible_dsg) > 0:
                x,y = max(compatible_dsg, key=lambda item:item[0])
            else :
                x,y = max(vector, key=lambda item:item[0])
                        
        df.loc[i:i,new_names[0]] = x
        df.loc[i:i,new_names[1]] = y
        
    df = df.drop(columns = columns)
    return df

'''
Function that formats "LIEs DSG %GD_1  ", "LIEs DSG %iNK_1  ", "LIEs DSG %GD_2  ", 
"LIEs DSG %iNK_2  ", "LIEs DSG %GD_3  ", "LIEs DSG %iNK_3  "
'''
def LIEs_DSG_formating(df, columns, new_names, records_number):
    df[columns] = df[columns].fillna(-1)
    pd.concat([df,pd.DataFrame(columns=new_names, index = range(records_number))])
    
    for i in range(records_number):
        vector = []
        for j in range(0, len(columns), 2):
            vector.append((float(df.loc[i:i,columns[j]]), 
                           float(df.loc[i:i,columns[j + 1]])))
            
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
                        
            df.loc[i:i,new_names[0]] = x
            df.loc[i:i,new_names[1]] = y
        else:
            df.loc[i:i,new_names[0]] = -1
            df.loc[i:i,new_names[1]] = -1
        
    df = df.drop(columns = columns)
    return df

'''
Function that join columns, in column new_name, with null_value for the nan 
giving priority to values
'''
def join_columns(df, columns, new_name, null_value, values,records_number):
    df = pd.concat([df, pd.DataFrame(columns=new_name, index = range(records_number))], axis = 1)
    df[new_name] = null_value 

    for i in range(records_number):
        for value in values:
            aux = 0
            for column in columns:
                if df[column].iloc[i] == value :
                   df.loc[i:i, new_name] = value
                   aux = 1
                   break;
            if aux == 1: break
           
    df = df.drop(columns = columns)

    return df


def process_LIEs (df, records_number):
    df = preprocess_LIEs_valoracion(df)
    
    df= LIEs_DCG_formating(df, lies_dcg_numerical[0], lies_dcg_numerical[1],
                                records_number)
    
    df = LIEs_DSG_formating(df, lies_dsg_numerical[0], lies_dsg_numerical[1],
                                records_number)
    
    for value in lies_valoracion.values():
        df = join_columns(df, value[0], value[1], 
                                           value[2][0],value[3], records_number)
    return df

##################################################################
#           PROCESS DCG Biopsia, DSG Biopsia, Biopsia DCG LIEs, Biopsia DCG LIEs
##################################################################

'''
Function that preprocesses columns "DCG Biopsia-AP1  ", "DCG Biopsia-AP2  ", 
["DSG Biopsia AP1", "DSG Biopsia AP2". It converts M3b/c in M3b and fills 
nan values with "Sin biopsia hecha"
'''    
def preprocess_Biopsias_AP(df, columns, current_nan_value, final_nan_value, records_number):
    
    for i in range(records_number):
            for column in columns:
                if ((str(df[column].iloc[i]) != "nan") and
                    (str(df[column].iloc[i]) != current_nan_value) and
                    (len(str(df[column].iloc[i])) > 2)):
                    df.loc[i:i, column] = str(df[column].iloc[i])[0:3]
                    
                if str(df[column].iloc[i]) == current_nan_value:
                    df.loc[i:i, column] = final_nan_value
                   
    df[columns] = df[columns].fillna(final_nan_value)
    
    return df

'''
Function that preprocesses columns "AP Biopsia DCG LIEs_1  ", "AP en Biopsia DCG LIEs_2  ", 
"AP Biopsia DSG LIEs_1  ", "AP en Biopsia DSG LIEs_2  ", "AP en Biopsia DSG LIEs_3  ". 
It changes Marsh 0 and Marsh 1 to M0, M1. And deletes information about Helicobacter
pilory that follows the result of the Biopsy after "-".
'''
def preprocess_Biopsias_LIEs(df, columns, nan_value, records_number):
    
    for i in range(records_number):
            for column in columns:
                if ((str(df[column].iloc[i]) != "nan") and
                    (len(str(df[column].iloc[i])) > 2)):
                    s = str(df[column].iloc[i])
                    s = s.replace("Marsh ", "M")
                    index = s.rfind("-")
                    if index != -1:
                        df.loc[i:i, column] = s[0:index]
                    else:
                        df.loc[i:i, column] = s

    df[columns] = df[columns].fillna(nan_value)
    
    return df

'''
Function that converts the dates in seconds since epoch.
'''
def preprocess_dates(df, columns):
    for column in columns:
        df[column]= pd.to_datetime(df[column],format='%d/%m/%y', errors='coerce')
        df[column]=(df[column] - dt.datetime(1970,1,1)).dt.total_seconds()
    df[columns] = df[columns].fillna(0)
    return df

'''
Function that deletes DSG biopsies that where made with less than 6 months since
the last DCG biopsy. 
'''
def delete_DSG_biopsias(df, dcg_dates, dsg_dates, dsg_biopsias, records_number):
    pd.concat([df,pd.DataFrame(columns=['max_dcg'], index = range(records_number))])
    df['max_dcg'] = df[dcg_dates].max(axis=1)
    for i in range(len(dsg_dates)):
        df[dsg_biopsias[i]] = df[dsg_biopsias[i]]
        df.loc[df[dsg_dates[i]] - df['max_dcg'] < 15811171, 
                   dsg_biopsias[i]] = "Sin biopsia hecha"
        #Borrar cuando se descomente la linea anterior
        #df.loc[df[dsg_dates[i]] - df['max_dcg'] < 15811171, 
        #           dsg_biopsias[i]] = np.NAN
        
    df = df.drop(columns=['max_dcg'])
    df = df.drop(columns=dcg_dates)
    df = df.drop(columns=dsg_dates)
    return df

def process_biopsias(df, records_number):
    for value in biopsias_AP.values():
        df = preprocess_Biopsias_AP(df, value[0], value[1][0], value[2][0],
                                     records_number)
    for value in biopsias_LIEs.values():
        df = preprocess_Biopsias_LIEs(df, value[0], value[1][0], 
                                          records_number)
        
    df = preprocess_dates(df, dates)
        
    df = delete_DSG_biopsias(df,biopsias_delete_dsg[0], biopsias_delete_dsg[1],
                                 biopsias_delete_dsg[2], records_number)
    
    for value in join_biopsias.values():
        df= join_columns(df, value[0], value[1], 
                                           value[2][0],value[3],records_number)
    return df

##################################################################
#           PROCESS DCG EMA, DSG EMA
##################################################################

'''
Function that fix the EMA columns
'''
def proces_EMA_column(df, columnName):
    aux = df[columnName]
    aux2 = []
    for i in range(0, len(aux)):
        if pd.isna(aux[i]):
            aux2.append(aux[i])
        else:
            aux2.append(aux[i].split()[0])
    
    aux2 = pd.DataFrame(aux2).replace('No', "No hecho")
    aux2 = aux2.replace(np.nan, "No hecho")
    
    df[columnName] = aux2
    
    #ATG2 + and Kit == Otro => DCG EMA +
    df['DCG EMA'] = np.where( ((df['DCG_ATG2_1'] == "Positivo") |
                    (df["DCG ATG2_2  "] == "Positivo")) &
                    (df["Indicar el kit empleado con el punto de corte entre paréntesis"] == "Otro"),
                    "Positivo", "Negativo")
    
    return df



##################################################################
#           PROCESS Edad diagnostico, Fecha nacimiento
##################################################################

'''
Given a list of column, split each column in several strips
'''
def split_by_strips(df, columns):
    for column in columns:
        conditionlist = [
        (df[column] < 18) ,
        ((18 <= df[column]) & (df[column] < 28)),
        (28 <= df[column]) & (df[column]< 38),
        (38 <= df[column]) & (df[column]< 48),
        (48 <= df[column]) & (df[column] < 58),
        (58 <= df[column]) & (df[column] < 70),
        (df[column] > 70)]
        
        choicelist = ["-18", "18 - 27", "28 - 37", "38 - 47",
            "48 - 57", "58 - 70", "+70"]
        
        df[column] = np.select(conditionlist,
                        choicelist, default='Desconocido')
    return df

'''
Function that proceses the age columns, 'Edad de diagnostico'
 and 'Fecha nacimiento'.
'''
def calculate_age(df, age, age_diagnostic):
    df[age]= pd.to_datetime(df[age],format='%d/%m/%y', errors='coerce')
    df[age]=(dt.datetime.now() - df[age]).dt.total_seconds()//(31536000)
    
    df = split_by_strips(df, [age, age_diagnostic])
    df = df[~(df['Fecha nacimiento'].str.contains("-18"))]
    df = df.reset_index(drop=True)
    return df

##################################################################
#           PROCESS Diagnóstico
##################################################################
def process_diagnostico(df):
    df['Diagnóstico']= df['Diagnóstico'].fillna('Sin diagnostico')
    
    return df

def drop_values(df):
    for to_drop in to_drop_values.values():
        df[to_drop[0]] = df[to_drop[0]].replace(to_drop[1], np.nan)
    return df


##################################################################
#           DCG ATG2 - => DCG EMA -
##################################################################
def last_adjustments(df):    
    df.loc[df.DCG_ATG2 == "Negativo", "DCG EMA"] = "Negativo"
    return df



'''
Function that makes the filtering by columns
'''
def filtering (df_aux):
    
    df_aux = calculate_age(df_aux, "Fecha nacimiento", "Edad diagnóstico")
    
    records_number = df_aux.iloc[:,0].size
    
    df_aux = countries_preprocesing(df_aux, european_countries, records_number)

    df_aux = proces_EMA_column(df_aux, "DCG EMA")

    df_aux = HLA_formating(df_aux)
    
    
    for column in take_the_highest_value_columns.values():
        df_aux = take_highest_value(df_aux, column[0], column[1], column[2],
                                    column[3], column[4], column[5], column[6])

    for column in take_the_lower_value_columns.values():
        df_aux = take_lower_value(df_aux, column[0], column[1], column[2],
                                    column[3], column[4], column[5], column[6])
        
    df_aux = process_kindship(df_aux)
    
    for element in fill_nan_value.values():
        df_aux = fill_nan_with_value(df_aux, element[0], element[1])
    
    for column in process_column_names.values():
        df_aux = process_columns_to_binary(df_aux,column[1], records_number, column[0])  
    
    df_aux = df_aux.loc[:,~df_aux.columns.duplicated()]
    
    df_aux = process_LIEs(df_aux, records_number)
    
    df_aux = process_biopsias(df_aux, records_number)
    
    df_aux = process_diagnostico(df_aux)

    df_aux = drop_values(df_aux)
    
    df_aux = last_adjustments(df_aux)
    
    
    return df_aux

    
    
    