# Analisis-EC

El objetivo del proyecto es continuar con la línea de investigación ya empezada en el año 2020 entre la Facultad de Informática de la Universidad Complutense de Madrid y el Hospital Clínico San Carlos. Más concretamente, el objetivo es ayudar al diagnóstico de la enfermedad celiaca en pacientes que no cursan una clínica habitual.
Para ello llevamos a cabo el formateo de los datos (los que por motivos de privacidad no se incluyen en el repositorio) y la posterior aplicación de algoritmos de clustering para tratar de encontrar relaciones entre los pacientes de la base de datos. 


## Cómo ejecutar el proyecto
En este repositorio se incluye un fichero de datos que por supuesto no es el real, pero que tiene la misma estructura (en cuanto a las columnas que contiene) y que permitirá a aquellas personas que lo deseen ejecutar el proyecto y 
visualizar los resultados. 

Para ejecutar el código y visualizar los resultados en local tendrás que tener instaladas las siguientes librerías de Python: 
- [Numpy](https://numpy.org/install/)
- [Pandas](https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html)
- [Plotly](https://plotly.com/python/getting-started/#installation)
- [Plotly orca]
- [Sklearn](https://scikit-learn.org/stable/install.html)
- [Sklearn extra](https://scikit-learn-extra.readthedocs.io/en/stable/install.html)
- [kPOD](https://pypi.org/project/kPOD/)
- [kmodes](https://pypi.org/project/kmodes/)
- [scikit-feature](https://github.com/jundongl/scikit-feature) Tendrá que descargarse este repositorio en local además de hacer los siguientes
Después solo tendrás que ejecutar:
```
python3 source.py
```

## Preprocesado de los datos
Este proceso fue complejo y constó de distintas etapas. 

### Filtrado y formateo de las columnas
En primer lugar se seleccionaron las columnas importantes que fueron elegidas tras una reunión con la Médica. Estas columnas se pueden ver en el fichero Important Columns.xlsx.
Después dada la elevada complejidad de los datos tuvimos que hacer un tratamiento especial para cada una de las columnas relevantes. Aquí detallamos brevemente el tratamiento para cada una de ellas.

### Tratamiento de datos categóricos
La mayoría de los métodos de clustering (excepto KPrototypes y KModes) trabajan únicamente con datos numéricos, sin embargo nuestro dataset contiene muchos datos categóricos, para transformarlos utilizamos la función [get_dummies](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.get_dummies.html). La implementación se puede ver [aquí](preprocessing/categorical_data.py).

### Tratamiento de datos incompletos
El mayor problema de los datos de los que disponemos es la gran cantidad de valores vacíos. Estos valores vacíos aparecen por dos motivos principales: o bien al paciente aún no se le han realizado todas las pruebas pertinentes o bien el paciente proviene de otro hospital y por ello no se dispone de todo su historial.
Además como bien sabemos los algoritmos de clustering, en su mayoría, no admiten datasets incompletos. Por este motivo es necesario confrontar este problema. Históricamente se han seguido dos enfoques principales: 
- La *eliminación de datos* aplicamos tres enfoques, la eliminación de columnas con algún dato incompleto, la eliminación de filas con un dato incompleto, y la eliminación según porcentajes de la columna o fila con un mayor número de elementos incompletos. La implementación se puede ver [aquí](preprocessing/deletion.py), 
pero ninguna de estas técnicas funciona de forma satisfactoria con nuestro dataset porque eliminan demasiados datos.
- La *imputación*:  la imputación univariada se descartó totalmente pues no tiene sentido por el tipo de datos (datos médicos) con los que estamos tratando. Por lo que se utilizaron:
  - Imputación multivariada: Hemos utilizado la implementación de sklearn de este imputador [IterativeImputer](https://scikit-learn.org/stable/modules/generated/sklearn.impute.IterativeImputer.html#sklearn.impute.IterativeImputer) sobre nuestro dataset. 
  Pero tuvimos problemas de convergencia aún utilizando un número muy alto de iteraciones (en concreto 100) por lo que consideramos que este tipo imputación es incompatible con nuestro dataset. Su implementación se puede ver [aquí](preprocessing/imputation.py).
  - Imputación por vecinos más cercanos: Hemos utilizado la implementación disponible en sklearn [KNNImputer](https://scikit-learn.org/stable/modules/generated/sklearn.impute.KNNImputer.html#sklearn.impute.KNNImputer) de forma satisfactoria. Su implementación se puede ver [aquí](preprocessing/imputation.py).
 
### Escalado de los datos
Las escalas de los datos numéricos diferían hasta dos órdenes de magnitud, como muchos de los algoritmos de clustering están basados en distancias tener unos datos sin escalar supondría que el método solo tuviera en cuenta las columnas con datos con mayor magnitud.
Aunque existen muchas técnicas la elegida por nosotros fue [QuantileTransformer](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.QuantileTransformer.html), el escalado se puede ver [aquí](preprocessing/scale.py).

## Construcción de los datasets
Como ya hemos dicho la gran mayoría de los métodos utilizan datasets numéricos, por este motivo solo describiremos aquí los datasets numéricos que construimos. Pero hay que tener en cuenta que también generamos datasets categóricos (para el método KModes), mixtos (para el método KPrototypes) y con datos incompletos (para el método KPOD) cuya selección de columnas sigue la lógica de los otros. 
- *Dataset completo*: Incluye el dataset completo obtenido tras el preprocesado.
- *Dataset resumido*: Elimina las columnas redundantes para las que se tiene tanto resultados numéricos como categóricos, conservando únicamente los numéricos. Este sería el caso de las pruebas de anticuerpos ATG2, A-PDG o la prueba de LIEs.
- *Dataset sin país, sexo, edad de diagnóstico ni grado de parentesco*: Al dataset completo le eliminamos las columnas relativas al país, sexo, edad de diagnóstico y grado de parentesco con otros enfermos celíacos.
- *Dataset sin país, sexo, edad de diagnóstico ni grado de parentesco resumido*: Al dataset resumido le eliminamos las columnas relativas al país, sexo, edad de diagnóstico y grado de parentesco.
- *Dataset sin signos ni síntomas*: Al dataset completo le eliminamos las columnas relativas a los signos, síntomas y enfermedades autoinmunes.
- *Dataset sin signos ni síntomas resumido*: Al dataset resumido le eliminamos las columnas relativas a los signos, síntomas y enfermedades autoinmunes.
- *Dataset sin país, sexo, edad de diagnóstico, grado de parentesco, síntomas ni signos*: Al dataset completo le eliminamos las columnas relativas al país, sexo, edad de diagnóstico, grado de parentesco, signos, síntomas y enfermedades autoinmunes.
- *Dataset sin país, sexo, edad de diagnóstico, grado de parentesco, síntomas ni signos resumido*: Al dataset resumido le eliminamos las columnas relativas al país, sexo, edad de diagnóstico, grado de parentesco, signos, síntomas y enfermedades autoinmunes.
- *Dataset con criterios diagnósticos*: Tras acudir al VII congreso nacional de la SECC (Sociedad Española de la Enfermedad Celiaca) fuimos capaces de determinar cúales eran los criterios para diagnosticar la enfermedad celíaca. Estos son:
  - **Genética:** por ello en este dataset incluimos la columna *HLA: grupos de riesgo*, y el parentesco de primer grado.
  - **Serología en dieta con gluten:** por ello incluimos los resultados de las pruebas EMA,  ATG2,  A-PDG , LIEs.
  - **Sospecha clínica (síntomas y signos compatibles con la enfermedad celíaca):** aunque todos los síntomas y signos que aparecen recogidos en nuestra base de datos son compatibles con la enfermedad celíaca solo incluimos los más comunes Diarrea crónica, Estreñimiento, Distensión abdominal, Dispepsia, Malabsorción, Anemia ferropénica o ferropenia. 
  - **Biopsia en dieta con gluten**
  - **Información relevante en dieta sin gluten**: Resultados de la biopsia una vez el paciente está siguiendo una dieta sin gluten y resultados de los LIEs.
- *Dataset con selección de columnas relevantes mediante CFS*: Este dataset solo contiene las columnas consideradas relevantes por CFS (estas fueron seleccionadas utilizando solo la parte del Dataset con diagnóstico válido, es decir, no vacío). Las columnas elegidas por CFS fueron *LIEs DCG %iNK, Biopsia DCG_M0, Valoracion LIEs DCG_No compatible con EC, DCG_ATG2_VALUE,DCG EMA_Positivo, DCG_ATG2_Negativo, LIEs DCG %GD, Valoracion LIEs DCG_Compatible con EC activa, DSG ATG2_Negativo, DCG A-PDG_Negativo, Biopsia DCG_M3b, LIEs DSG %GD*.
- *Dataset con selección de columnas relevantes mediante FCBF*: Este dataset solo contiene las columnas consideradas relevantes po FCBF (estas fueron seleccionadas utilizando solo la parte del dataset con diagnóstico no vacío). Las columnas elegidas fueron *LIEs DCG %iNK, Biopsia DCG_M0, Valoracion LIEs DCG_No compatible con EC, DCG EMA_Positivo, Biopsia DSG_M3b, Esclerosis múltiple*.

La generación de todos los datasets se puede ver [aquí](preprocessing/preprocess.py)
## Aplicación de los métodos de clustering
Sobre todos los datasets listados en el apartado anterior ejecutamos los algoritmos de clustering más conocidos: [KMeans](clustering/kmeans.py),  [KMedoids](clustering/kmedoids.py), [Clustering aglomerativo](clustering/agglomerative.py), [Clustering espectral](clustering/spectral.py), [DBSCAN](clustering/DBSCAN.py), [Optics](clustering/optics.py).

Además utilizamos otros algoritmos de clustering menos conocidos pero que por el tipo de datos (gran cantidad de datos categóricos, y datos incompletos) resultaban de mucho interés como son: [KPrototypes](clustering/kmodes_prototypes.py), [KModes](clustering/kmodes_prototypes.py), [kPOD](clustering/kpod_a.py).

## Evaluación de los datasets y de los métodos de clustering
Para la evaluación de los datasets utilizamos el [estadístico de Hopkins](clustering/hopkins_statistics.py). 
Para la evaluación de los métodos de clustering utilizamos como método intrínseco el [coeficiente de Silhouette](clustering/silhouette.py) y como método extrínseco [la precisión y exhaustividad BCubed](clustering/b3.py).

## Visualización de los resultados
Para la visualización de los resultados estamos utilizando la librería Plotly y tenemos tres elementos básicos de visualización:
1. Comparación de la calidad de los datasets mediante estadístico de Hopkins.
2. Comparación de los datasets para cada método mediante coeficiente de Silhouette y precisión y exhaustividad BCubed.
3. Clasificación de los pacientes en clústeres según su diagnóstico. 

Además utilizamos dos herramientas más de visualización que fueron muy útiles durante el desarrollo aunque no tanto para el análisis final de los resultados:
1. Visualización de los pacientes y resultado del clustering en 2D
2. Visualización del peso de las variables


## Referencias
Chi JT, Chi EC, Baraniuk RG (2016). “k-POD: A Method for k-Means Clustering of Missing Data.” The American Statistician, 70, 91–99. doi: 10.1080/00031305.2015.1086685, http://www.tandfonline.com/doi/abs/10.1080/00031305.2015.1086685.

Radia, Ishaan (2020). “A Python implementation of k-POD.” https://github.com/iiradia/kPOD/.

Nelis J. de Vos (2015-2021). "kmodes categorical clustering library" https://github.com/nicodv/kmodes

Li, Jundong and Cheng, Kewei and Wang, Suhang and Morstatter, Fred and Trevino, Robert P and Tang, Jiliang and Liu, Huan (2018). "Feature selection: A data perspective"
ACM Computing Surveys (CSUR). https://arxiv.org/pdf/1601.07996.pdf

Matthew Wiesner. "A Python implementation of BCubed" https://github.com/m-wiesner/BCUBED

Ismaël Lachheb (2019) "pyclustertend" https://github.com/lachhebo/pyclustertend
## Autores
**Carla Martínez Nieto-Márquez**- [LinkedIn](https://www.linkedin.com/in/carla-mart%C3%ADnez-nieto-m%C3%A1rquez-a59435176/)- [Github](https://github.com/carlita98)

**Pablo Sanz Caperote** -[Github](https://github.com/SCPablo)

