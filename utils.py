process_column_names = {
  "immunological_desease": [['Enfermedad inmunológica', 'Enfermedad inmunológica (si hay más de 1)', 
                'Enfermedad inmunológica (si hay más de 2)'], ["Otra"]],
  "symptoms": [['Síntomas específicos', 'Síntomas específicos.1', 'Síntomas específicos.2', 'Otros síntomas'], 
              ["Otros (especificar en otros síntomas)"]],
  "signs": [['Signos  ', 'Signos 2  ', '  Signos 3'], ["Nada"]],
  "kits": [['Indicar el kit empleado con el punto de corte entre paréntesis',
            'Indicar el kit empleado con el punto de corte entre paréntesis.1'], ["Nada"]],
  "DCG": [['DCG Biopsia-AP1  ', 'DCG Biopsia-AP2  '], ["Nada"]],
  "AP_Biopsy": [['AP Biopsia DCG LIEs_1  ', 'AP Biopsia DSG LIEs_1  '], ["Nada"]]
}

simple_process_column_names = ['Diagnóstico', 'HLA: grupos de riesgo', 'Haplotipo1', 'Haplotipo2', 
    'DCG EMA', 'DCG A-PDG_1  ', 'Valoración DCG LIEs1', 'Valoración LIEs2', 'Valoración DSG LIEs1', 
    'Respuesta DSG  ', 'Respuesta DSG Clínica  ','Respuesta DSG Serológica  ','Respuesta DSG Histológica  ', 
    'Marcadores citometría']

column_to_binary_column_names ={
    "gender": ["Sexo", "Sexo_Hombre", "Sexo_Mujer"],
    "DCG_ATG2_1": ["DCG_ATG2_1", "DCG_ATG2_1_Negativo", "DCG_ATG2_1_Positivo"],
    "DSG ATG2_2": ["DSG ATG2_2  ", "DSG ATG2_2  _Negativo", "DSG ATG2_2  _Positivo"],
    "helicobacter" :["Helicobacter pylori en el momento de la biopsia", 
    "Helicobacter pylori en el momento de la biopsia_No", 
    "Helicobacter pylori en el momento de la biopsia_Yes"],
    "olmesartan" :["Olmesartán en el momento de la biopsia",
    "Olmesartán en el momento de la biopsia_No", 
    "Olmesartán en el momento de la biopsia_Yes"], 
    "giardia" :["Giardia en el momento de la biopsia", 
    "Giardia en el momento de la biopsia_No", 
    "Giardia en el momento de la biopsia_Yes"], 
    "overgrowth ": ["Sobrecrecimiento bacteriano en el momento de la biopsia", 
    "Sobrecrecimiento bacteriano en el momento de la biopsia_No",
    "Sobrecrecimiento bacteriano en el momento de la biopsia_Yes"]
}

fill_nan_with_zero_column_names = ["Edad diagnóstico", "Indicar titulo del anticuerpo (DCG ATG_2_1)", 
    "Indique título de anticuerpo  (DCG ATG_2_2)", "Indique el título del anticuerpo (DSG ATG2_1)",
    "Indique el título del anticuerpo (DSG ATG2_2)",
    "LIEs DCG %GD_1  ", "LIEs DCG %iNK_1  ", "LIEs DCG %GD_2  ", "LIEs DCG %iNK_2  ", "LIEs DSG %GD_1  ", 
    "LIEs DSG %iNK_1  ", "N CD8 triple positiva d0", "N CD8 triple positiva d6", "% CD8 triple positiva d0", 
    "% CD8 triple positiva d6", "N GD triple positiva d0", "N GD triple positiva d6", "% GD triple positiva d0", 
    "% GD triple positiva d6", "LIEs %GD  ", "LIEs %iNK  "]

column_with_irrelevant_data_names = {
    "ELISPOT": [['ELISPOT', 'ELISPOT.1'], 'No hecho']
}