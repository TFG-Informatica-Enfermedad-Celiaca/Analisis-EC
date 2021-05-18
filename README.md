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


### Tratamiento de datos incompletos
El mayor problema de los datos de los que disponemos es la gran cantidad de valores vacíos. Estos valores vacíos aparecen por dos motivos principales: o bien al paciente aún no se le han realizado todas las pruebas pertinentes o bien el paciente proviene de otro hospital y por ello no se dispone de todo su historial.
Además como bien sabemos los algoritmos de clustering, en su mayoría, no admiten datasets incompletos. Por este motivo es necesario confrontar este problema. Históricamente se han seguido dos enfoques principales: 
- La *eliminación de datos* aplicamos tres enfoques, la eliminación de columnas con algún dato incompleto, la eliminación de filas con un dato incompleto, y la eliminación según porcentajes de la columna o fila con un mayor número de elementos incompletos. La implementación se puede ver en el fichero deletion.py, 
pero ninguna de estas técnicas funciona con nuestro dataset porque eliminan demasiados datos.
- La *imputación*:  la imputación univariada se descartó totalmente pues no tiene sentido por el tipo de datos (datos médicos) con los que estamos tratando. Por lo que se utilizaron:
  - Imputación multivariada: Hemos utilizado la implementación de sklearn de este imputador [IterativeImputer](https://scikit-learn.org/stable/modules/generated/sklearn.impute.IterativeImputer.html#sklearn.impute.IterativeImputer) sobre nuestro dataset. 
  Pero tuvimos problemas de convergencia aún utilizando un número muy alto de iteraciones (en concreto 100) por lo que consideramos que este tipo imputación es incompatible con nuestro dataset.
  - Imputación por vecinos más cercanos: Hemos utilizado la implementación disponible en sklearn [KNNImputer](https://scikit-learn.org/stable/modules/generated/sklearn.impute.KNNImputer.html#sklearn.impute.KNNImputer) de forma satisfactoria.
  
### Escalado de los datos
Las escalas de los datos numéricos diferían hasta dos órdenes de magnitud, como muchos de los algoritmos de clustering están basados en distancias tener unos datos sin escalar supondría que el método solo tuviera en cuenta las columnas con datos con mayor magnitud.
Aunque existen muchas técnicas la elegida por nosotros fue [QuantileTransformer](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.QuantileTransformer.html). 

## Construcción de los datasets

## Aplicación de los métodos de clustering

## Evaluación de los datasets y de los métodos de clustering

