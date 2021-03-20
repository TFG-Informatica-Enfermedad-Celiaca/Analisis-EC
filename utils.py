process_column_names = {
  "immunological_desease": [['Enfermedad inmunológica', 'Enfermedad inmunológica (si hay más de 1)', 
                'Enfermedad inmunológica (si hay más de 2)'], ["Otra"]],
  "symptoms": [['Síntomas específicos', 'Síntomas específicos.1', 'Síntomas específicos.2'], 
              ["Otros (especificar en otros síntomas)"]],
  "signs": [['Signos  ', 'Signos 2  ', '  Signos 3'], ["Nada"]],
  "Biopsia": [["DCG Biopsia-AP2  "], ["Sin biopsia hecha en DCG"]],
  "Halotipos": [["Haplotipo1", "Haplotipo2"], ["SIN RIESGO"]]
}

simple_process_column_names = ['Diagnóstico', 'HLA: grupos de riesgo', 
    'Valoración DCG LIEs1', 'Valoración LIEs2',
    'Valoración DSG LIEs1', 'AP Biopsia DCG LIEs_1  ', 'AP Biopsia DSG LIEs_1  ']
'''
'DCG A-PDG_1  ', 'DCG EMA'
'''


column_to_binary_column_names ={
    "gender": ["Sexo", "Sexo_Hombre", "Sexo_Mujer"],
    
    "DSG ATG2_2": ["DSG ATG2_2  ", "DSG ATG2_2  _Negativo", "DSG ATG2_2  _Positivo"],
    "helicobacter" :["Helicobacter pylori en el momento de la biopsia", 
    "Helicobacter pylori en el momento de la biopsia_No", 
    "Helicobacter pylori en el momento de la biopsia_Yes"]
}
'''
Esta línea la he quitado de arriba justo (del hueco) porque al ejecutarse 
convierte la columna de neg/pos a 0 y 1 pero rellenando con 0s
 "DCG_ATG2": ["DCG_ATG2", "DCG_ATG2_Negativo", "DCG_ATG2_Positivo"],
'''


fill_nan_with_zero_column_names = ["Edad diagnóstico", "Indicar titulo del anticuerpo (DCG ATG_2_1)", 
    "Indique título de anticuerpo  (DCG ATG_2_2)",
    "Indique el título del anticuerpo (A-PDG_1)",
    "Indique el título del anticuerpo (A-PDG_2)",
    "Indique el título del anticuerpo (DSG ATG2_1)",
    "Indique el título del anticuerpo (DSG ATG2_2)",
    "LIEs DCG %GD_2  ", "LIEs DCG %iNK_2  ", "LIEs DSG %GD_1  ", 
    "LIEs DSG %iNK_1  "]


columns_to_be_joined = {
    "DCG": ['DCG Biopsia-AP1  ', 'DCG Biopsia-AP2  '],
    "LIEs_GD": ["LIEs DCG %GD_1  ", "LIEs DCG %GD_2  "],
    "LIEs_iNK": ["LIEs DCG %iNK_1  ", "LIEs DCG %iNK_2  "]
}


take_the_highest_value_columns = {
    "DCG":[["DCG_ATG2_1", "DCG ATG2_2  "],
           ["Indicar titulo del anticuerpo (DCG ATG_2_1)", "Indique título de anticuerpo  (DCG ATG_2_2)"],
           ["Indicar el kit empleado con el punto de corte entre paréntesis"],
           ["Aeskulisa tTg-A de Grifols (20)"], ['DCG_ATG2'], ['DCG_ATG2_VALUE']],
    "DCG A-PDG": [["DCG A-PDG_1  ", "DCG A-PDG_2  "],
                  ["Indique el título del anticuerpo (A-PDG_1)", "Indique el título del anticuerpo (A-PDG_2)"],
                  ["Indicar el kit empleado con el punto de corte entre paréntesis 1"],
                  ["Euroimmun (25)"], ['DCG A-PDG'], ['DCG A-PDG_VALUE']]
}



european_countries = [ "Alemania", "Austria", "Bélgica", "Bulgaria",
    "Chequia", "Chipre", "Croacia", "Dinamarca", "Eslovaquia", "Eslovenia",
    "España", "Estonia", "Finlandia", "Francia", "Grecia", "Hungría",
    "Irlanda", "Italia", "Letonia", "Lituania", "Luxemburgo", "Malta",
    "Países Bajos", "Polonia", "Portugal", "Rumanía", "Suecia"
    ]

lies_dcg_numerical = [["LIEs DCG %GD_1  ", "LIEs DCG %iNK_1  ", "LIEs DCG %GD_2  ", 
                  "LIEs DCG %iNK_2  "], ["LIEs DCG %GD", "LIEs DCG %iNK"]]
lies_dsg_numerical = [["LIEs DSG %GD_1  ", "LIEs DSG %iNK_1  ", "LIEs DSG %GD_2  ", 
                  "LIEs DSG %iNK_2  ", "LIEs DSG %GD_3  ", "LIEs DSG %iNK_3  "]
                 , ["LIEs DSG %GD", "LIEs DSG %iNK"]]
lies_valoracion = {
    "DCG": [["Valoración DCG LIEs1", "Valoración LIEs2"],["Valoracion LIEs DCG"], 
            ["LIEs no hecho"],["Compatible con EC activa", "Compatible con EC en DSG", 
              "No compatible con EC"]],
    "DSG": [["Valoración DSG LIEs1", "Valoración DSG LIEs2", "Valoración DSG LIEs3"],
            ["Valoracion LIEs DSG"], ["LIEs no hecho"], 
            ["No compatible con EC", "Compatible con EC en DSG", 
              "Compatible con EC activa"]]
}

biopsias_AP = {
    "DCG": [["DCG Biopsia-AP1  ", "DCG Biopsia-AP2  "], ["Sin biopsia hecha en DCG"], 
            ["Sin biopsia hecha"]], 
    "DSG": [["DSG Biopsia AP1", "DSG Biopsia AP2"],["Sin biopsia hecha en DCG"],
            ["Sin biopsia hecha"]]
}

biopsias_LIEs = {
    "DCG": [["AP Biopsia DCG LIEs_1  ", "AP en Biopsia DCG LIEs_2  "],
            ["Sin biopsia hecha"]], 
    "DSG": [["AP Biopsia DSG LIEs_1  ", "AP en Biopsia DSG LIEs_2  ", 
             "AP en Biopsia DSG LIEs_3  "],["Sin biopsia hecha"]]    
}

dates = ["Fecha DCG Biopsia1", "Fecha DCG Biopsia2  ", "Fecha DSG biopsia1", 
         "Fecha DSG biopsia2", "FECHA LIEs DCG_1  ", "FECHA LIEs DCG_2",
         "FECHA LIEs DSG_1  ", "FECHA LIEs DSG_2  ", "FECHA LIEs DSG_3  "]
biopsias_delete_dsg = [["Fecha DCG Biopsia1", "Fecha DCG Biopsia2  ",
         "FECHA LIEs DCG_1  ", "FECHA LIEs DCG_2"],["Fecha DSG biopsia1", 
         "Fecha DSG biopsia2","FECHA LIEs DSG_1  ", "FECHA LIEs DSG_2  ", 
         "FECHA LIEs DSG_3  "], ["DSG Biopsia AP1", "DSG Biopsia AP2", 
        "AP Biopsia DSG LIEs_1  ", "AP en Biopsia DSG LIEs_2  ", 
             "AP en Biopsia DSG LIEs_3  "]]
                                 
join_biopsias = {
    "DCG": [["DCG Biopsia-AP1  ", "DCG Biopsia-AP2  ", "AP Biopsia DCG LIEs_1  ",
                  "AP en Biopsia DCG LIEs_2  "], ["Biopsia DCG"], ["Sin biopsia hecha"] , 
                 ["M3c", "M3b", "M3a", "M2", "M1", "M0"]],
    "DSG": [["DSG Biopsia AP1", "DSG Biopsia AP2", "AP Biopsia DSG LIEs_1  ",
             "AP en Biopsia DSG LIEs_2  ", "AP en Biopsia DSG LIEs_3  "], ["Biopsia DSG"], 
            ["Sin biopsia hecha"] , ["M0", "M1", "M2", "M3a", "M3b", "M3c"]]
}