process_column_names = {
  "immunological_desease": ['Enfermedad inmunológica', 'Enfermedad inmunológica (si hay más de 1)', 
                'Enfermedad inmunológica (si hay más de 2)'],
  "symptoms": ['Síntomas específicos', 'Síntomas específicos.1', 'Síntomas específicos.2', 'Otros síntomas'],
  "signs": ['Signos  ', 'Signos 2  ', '  Signos 3']
}

to_delete = {
    "immunological_desease": ["Otra"], 
    "symptoms": ["Otros (especificar en otros síntomas)"],
    "signs": ["Nada"]
}

simple_process_column_names = ['Diagnóstico', 'HLA: grupos de riesgo', 'Haplotipo1', 'Haplotipo2', 
    'DCG_ATG2_1', 'DCG EMA', 'DCG A-PDG_1  ', 'DSG ATG2_2  ']