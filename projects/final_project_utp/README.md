# final_project_utp

Proyecto de análisis y modelado sobre el rendimiento académico de estudiantes de Matemáticas del repositorio **UCI Student Performance**.

## Contexto del proyecto

### Dataset seleccionado

Se utilizará el conjunto de datos `student-mat.csv`, perteneciente al repositorio **UCI Student Performance**. Este contiene información académica, personal, familiar y social de estudiantes que cursaron la asignatura de Matemáticas.

### Pregunta principal

¿En qué medida los factores familiares, personales y digitales se relacionan con el rendimiento académico y permiten identificar estudiantes con riesgo de reprobar Matemáticas?

### Preguntas específicas

1. ¿Los estudiantes con acceso a internet presentan mejores calificaciones que aquellos sin acceso?
2. ¿Existen diferencias en el rendimiento académico entre estudiantes de zonas urbanas y rurales?
3. ¿Cómo se relaciona el nivel educativo de la madre y del padre con la nota final?
4. ¿El apoyo educativo familiar se relaciona con una mayor probabilidad de aprobación?
5. ¿La calidad de las relaciones familiares influye en el desempeño académico?
6. ¿Cuáles factores familiares y digitales tienen mayor importancia en los modelos predictivos?
7. ¿Es posible identificar estudiantes en riesgo utilizando solamente variables familiares, personales y digitales?

### Objetivo general

Analizar la relación entre los factores familiares, personales y digitales y el rendimiento académico de los estudiantes de Matemáticas, mediante técnicas estadísticas, visualizaciones y modelos de aprendizaje automático que permitan identificar estudiantes con riesgo de reprobar.

### Objetivos específicos

1. Comparar las calificaciones de los estudiantes que poseen acceso a internet con las de aquellos que no tienen acceso.
2. Determinar si existen diferencias de rendimiento entre estudiantes de zonas urbanas y rurales.
3. Analizar la relación entre el nivel educativo de los padres y la calificación final del estudiante.
4. Evaluar la asociación entre el apoyo educativo familiar y la probabilidad de aprobar Matemáticas.
5. Examinar la relación entre la calidad de las relaciones familiares y el desempeño académico.
6. Identificar las variables familiares, personales y digitales con mayor importancia predictiva.
7. Entrenar y comparar modelos de clasificación para identificar estudiantes con riesgo de reprobar.
8. Entrenar y comparar modelos de regresión para estimar la calificación final de los estudiantes.

### Hipótesis general

Los estudiantes que cuentan con mejores condiciones familiares y digitales presentan un mejor rendimiento académico y una menor probabilidad de reprobar Matemáticas.

### Hipótesis específicas

- Los estudiantes con acceso a internet presentan una nota final promedio superior.
- Los estudiantes de zonas urbanas presentan mejores resultados que los estudiantes de zonas rurales.
- Un mayor nivel educativo de los padres se relaciona con mejores calificaciones.
- El apoyo educativo familiar se relaciona con una mayor probabilidad de aprobación.
- Una mejor calidad de las relaciones familiares se relaciona con un mejor desempeño académico.
- Los factores familiares, personales y digitales permiten identificar parcialmente a los estudiantes con riesgo académico.

## Estructura del proyecto

- `data/raw/`: archivos fuente originales.
- `data/processed/`: salidas limpias o preparadas.
- `notebooks/`: notebooks del proyecto.
- `scripts/`: automatizaciones o transformaciones reproducibles.
- `docs/`: documentación de apoyo del dataset.
- `archive/legacy_dataset/`: respaldo histórico del paquete original.

## Archivos principales

- `notebooks/proyecto_adtc.ipynb`: limpieza y preparación del dataset.
- `notebooks/proyecto_adtc_analista.ipynb`: análisis exploratorio.
- `notebooks/proyecto_adtc_data_scientist.ipynb`: modelado predictivo del científico de datos.
- `scripts/student-merge.R`: cruce entre `student-mat.csv` y `student-por.csv`.
- `docs/student.txt`: diccionario de atributos del dataset.

## Rutas esperadas

Los notebooks y el script usan rutas relativas, así que deben ejecutarse desde su propia carpeta:

- Notebook de limpieza: `notebooks/`
- Notebook de análisis: `notebooks/`
- Notebook de ciencia de datos: `notebooks/`
- Script R: `scripts/`

## Archivo histórico

El antiguo directorio `Dataset/` se conserva dentro de `archive/legacy_dataset/` para no perder trazabilidad del material original.
