process_column_names = {
  "immunological_desease": [['Enfermedad inmunológica', 'Enfermedad inmunológica (si hay más de 1)', 
                'Enfermedad inmunológica (si hay más de 2)'], ["Otra"]],
  "symptoms": [['Síntomas específicos', 'Síntomas específicos.1', 'Síntomas específicos.2'], 
              ["Otros (especificar en otros síntomas)"]],
  "signs": [['Signos  ', 'Signos 2  ', '  Signos 3'], ["Nada"]]
}

fill_nan_value = {
    "gender": ["Sexo", "Desconocido"], 
    "helicobacter" :["Helicobacter pylori en el momento de la biopsia", "Desconocido"]
}

take_the_highest_value_columns = {
    "DCG ATG2":[["DCG_ATG2_1", "DCG ATG2_2  "],
           ["Indicar titulo del anticuerpo (DCG ATG_2_1)", "Indique título de anticuerpo  (DCG ATG_2_2)"],
           ["Indicar el kit empleado con el punto de corte entre paréntesis"],
           ["Aeskulisa tTg-A de Grifols (20)"], ['DCG_ATG2'], ['DCG_ATG2_VALUE'], 20],
    "DCG A-PDG": [["DCG A-PDG_1  ", "DCG A-PDG_2  "],
                  ["Indique el título del anticuerpo (A-PDG_1)", "Indique el título del anticuerpo (A-PDG_2)"],
                  ["Indicar el kit empleado con el punto de corte entre paréntesis 1"],
                  ["Euroimmun (25)"], ['DCG A-PDG'], ['DCG A-PDG_VALUE'], 25]
}

take_the_lower_value_columns = {
    "DSG ATG2":[["DSG ATG2_1  ", "DSG ATG2_2  "],
           ["Indique el título del anticuerpo (DSG ATG2_1)", "Indique el título del anticuerpo (DSG ATG2_2)"],
           ["Indicar el kit empleado con el punto de corte entre paréntesis 2"],
           ["Aeskulisa tTg-A de Grifols (20)"], ['DSG ATG2'], ['DSG ATG2 VALUE'], 20],
    "DSG APDG": [["DSG A-PDG_1  "],
                 ["Valor  A-PDG_1  "],
                 ["A-PDG kit  "], ["Euroimmun (25)"],
                 ["DSG A-PDG"], ["DSG A-PDG VALUE"], 25]
}

european_countries = [ "Alemania", "Austria", "Bélgica", "Bulgaria",
    "Chequia", "Chipre", "Croacia", "Dinamarca", "Eslovaquia", "Eslovenia",
    "España", "Estonia", "Finlandia", "Francia", "Grecia", "Hungría",
    "Irlanda", "Italia", "Letonia", "Lituania", "Luxemburgo", "Malta",
    "Países Bajos", "Polonia", "Portugal", "Rumanía", "Suecia"
    ]

hla_haplotipos = [['SIN RIESGO', 'SIN RIESGO', 'SIN RIESGO'], ['DQ7.5', 'DQ7.5', 'DQ7.5'], 
                  ['DQ2.2', 'DQ2.2', 'DQ2.2'], ['DQ8', 'DQ8', 'DQ8 doble dosis'], 
                  'DQ8']
lies_valoracion_preprocess = [["LIEs DCG %GD_1  ", "LIEs DCG %iNK_1  ", "Valoración DCG LIEs1"], 
                              ["LIEs DCG %GD_2  ", "LIEs DCG %iNK_2  ", "Valoración LIEs2"], 
                              ["LIEs DSG %GD_1  ", "LIEs DSG %iNK_1  ", "Valoración DSG LIEs1"],
                              ["LIEs DSG %GD_2  ", "LIEs DSG %iNK_2  ", "Valoración DSG LIEs2"],
                              [ "LIEs DSG %GD_3  ", "LIEs DSG %iNK_3  ","Valoración DSG LIEs3"]]

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

to_drop_values = {
    "1" : ["Indique país de origen o en su defecto la información disponible", 
           "Desconocido"], 
    "2" : ["Sexo", "Desconocido"], 
    "3" : ["Edad diagnóstico", "Desconocido"], 
    "4" : ["HLA: grupos de riesgo", "HLA NO HECHO"], 
    "5" : ["DCG EMA", "No hecho"],
    "6" : ["DSG EMA  ", "No hecho"], 
    "7" : ["Helicobacter pylori en el momento de la biopsia", "Desconocido"], 
    "8" : ["Fecha nacimiento", "Desconocido"],
    "9" : ["DCG_ATG2", "No hecho"], 
    "10": ["DCG A-PDG", "No hecho"], 
    "11": ["DSG ATG2", "No hecho"], 
    "12": ["DSG A-PDG", "No hecho"], 
    "13": ["Valoracion LIEs DCG", "LIEs no hecho"], 
    "14": ["Valoracion LIEs DSG", "LIEs no hecho"], 
    "15": ["Biopsia DCG", "Sin biopsia hecha"], 
    "16": ["Biopsia DSG", "Sin biopsia hecha"],
    "17": ["DCG_ATG2_VALUE", -1], 
    "18": ["DCG A-PDG_VALUE", -1], 
    "19": ["DSG ATG2 VALUE", -1], 
    "20": ["DSG A-PDG VALUE", -1],
    "21": ["LIEs DCG %GD", -1],
    "22": ["LIEs DCG %iNK", -1],
    "23": ["LIEs DSG %GD", -1], 
    "24": ["LIEs DSG %iNK", -1]    
}

numerical_columns = ["DCG_ATG2_VALUE", "DCG A-PDG_VALUE", "DSG ATG2 VALUE", "DSG A-PDG VALUE", 
        "LIEs DCG %GD", "LIEs DCG %iNK", "LIEs DSG %GD", "LIEs DSG %iNK"]

categorical_columns = {
    "0": ["Indique país de origen o en su defecto la información disponible", 
        "Sexo", "Edad diagnóstico", "HLA: grupos de riesgo", "DCG EMA", "DSG EMA  ", 
        "Helicobacter pylori en el momento de la biopsia", "Fecha nacimiento", 
        "DCG_ATG2", "DCG A-PDG", "DSG ATG2", "DSG A-PDG", "Valoracion LIEs DCG", 
        "Valoracion LIEs DSG", "Biopsia DCG", "Biopsia DSG"],
    "1": ["Indique país de origen o en su defecto la información disponible", 
        "Sexo", "Edad diagnóstico", "HLA: grupos de riesgo", "DCG EMA", "DSG EMA  ", 
        "Helicobacter pylori en el momento de la biopsia", "Fecha nacimiento", 
        "Biopsia DCG", "Biopsia DSG"],
    "2": ["HLA: grupos de riesgo", "DCG EMA", "DSG EMA  ", 
        "Helicobacter pylori en el momento de la biopsia", "Fecha nacimiento", 
        "DCG_ATG2", "DCG A-PDG", "DSG ATG2", "DSG A-PDG", "Valoracion LIEs DCG", 
        "Valoracion LIEs DSG", "Biopsia DCG", "Biopsia DSG"],
    "3": ["HLA: grupos de riesgo", "DCG EMA", "DSG EMA  ", 
        "Helicobacter pylori en el momento de la biopsia", "Fecha nacimiento", 
        "Biopsia DCG", "Biopsia DSG"],
    
    "4": ["Indique país de origen o en su defecto la información disponible", 
        "Sexo", "Edad diagnóstico", "HLA: grupos de riesgo", "DCG EMA", "DSG EMA  ", 
        "Helicobacter pylori en el momento de la biopsia", "Fecha nacimiento", 
        "DCG_ATG2", "DCG A-PDG", "DSG ATG2", "DSG A-PDG", "Valoracion LIEs DCG", 
        "Valoracion LIEs DSG", "Biopsia DCG", "Biopsia DSG"], 
    "5": ["Indique país de origen o en su defecto la información disponible", 
        "Sexo", "Edad diagnóstico", "HLA: grupos de riesgo", "DCG EMA", "DSG EMA  ", 
        "Helicobacter pylori en el momento de la biopsia", "Fecha nacimiento", 
        "Biopsia DCG", "Biopsia DSG"],
    "6": ["HLA: grupos de riesgo", "DCG EMA", "DSG EMA  ", 
        "Helicobacter pylori en el momento de la biopsia", "Fecha nacimiento", 
        "DCG_ATG2", "DCG A-PDG", "DSG ATG2", "DSG A-PDG", "Valoracion LIEs DCG", 
        "Valoracion LIEs DSG", "Biopsia DCG", "Biopsia DSG"],
    "7": ["HLA: grupos de riesgo", "DCG EMA", "DSG EMA  ", 
        "Helicobacter pylori en el momento de la biopsia", "Fecha nacimiento", 
        "Biopsia DCG", "Biopsia DSG"],
    }
    


try1_columns = ['Indique país de origen o en su defecto la información disponible_Europeo',
                'Indique país de origen o en su defecto la información disponible_Otro',
                'Sexo_Hombre', 'Sexo_Mujer', 'Edad diagnóstico_+70', 'Edad diagnóstico_-18',
                'Edad diagnóstico_18 - 27', 'Edad diagnóstico_28 - 37', 'Edad diagnóstico_38 - 47',
                'Edad diagnóstico_48 - 57', 'Edad diagnóstico_58 - 70', 
                '1º grado', '2º grado', '3º grado', '4º grado', 'Fecha nacimiento_+70', 
                'Fecha nacimiento_18 - 27', 'Fecha nacimiento_28 - 37', 'Fecha nacimiento_38 - 47', 
                'Fecha nacimiento_48 - 57', 'Fecha nacimiento_58 - 70']

try_cat_columns = ['Indique país de origen o en su defecto la información disponible',
                   'Sexo', 'Edad diagnóstico', '1º grado', '2º grado', '3º grado', '4º grado']



