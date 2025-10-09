# Análisis y Documentación de Scripts de Procesamiento de Datos

Este repositorio contiene una serie de scripts de Python y notebooks de Jupyter diseñados para procesar y analizar datos de encuestas. A continuación se detalla la función de cada archivo y cómo se interrelacionan en un flujo de trabajo de análisis de datos.

## `sample_generator.py`

Este script se utiliza para generar un archivo de datos de SPSS (`.sav`) a partir de un archivo de Excel. Su propósito principal es crear un conjunto de datos de muestra que puede ser utilizado para pruebas y análisis exploratorios.

### Entradas y Salidas

-   **Entrada**: Un archivo de Excel (`course_example.xlsx`) que contiene los datos brutos. La primera fila debe contener los nombres de las variables y la segunda fila las etiquetas de las variables.
-   **Salida**: Un archivo de datos de SPSS (`sample_dataset.sav`) que incluye tanto los datos como los metadatos (etiquetas de variables y etiquetas de valores).

### Funcionalidad

1.  **Carga de Datos**: Carga los datos de una hoja de cálculo de Excel utilizando la biblioteca `pandas`.
2.  **Mapeo de Valores**: Convierte las respuestas categóricas de texto a valores numéricos. Por ejemplo, "Montevideo" se convierte en `1` y "Interior" en `2`.
3.  **Creación de Archivo `.sav`**: Utiliza la biblioteca `pyreadstat` para escribir el `DataFrame` de `pandas` en un archivo `.sav`. El script también define y guarda las etiquetas de las variables y los valores, asegurando que los metadatos se conserven en el archivo de salida.

## `sample_analyzer.ipynb`

Este notebook de Jupyter se utiliza para realizar un análisis exploratorio básico del archivo `sample_dataset.sav` generado por el script `sample_generator.py`.

### Funcionalidad

1.  **Carga de Datos**: Lee el archivo `.sav` utilizando `pyreadstat`, cargando tanto los datos como los metadatos.
2.  **Inspección de Metadatos**: Muestra las etiquetas de las variables y las etiquetas de los valores para entender el contexto de los datos.
3.  **Visualización de Datos**: Muestra las primeras filas del `DataFrame` para una inspección inicial.

## `column_transformation.ipynb`

Este notebook contiene un pipeline de procesamiento de datos más complejo, diseñado para transformar un conjunto de datos de encuesta desde un formato ancho a un formato largo, haciéndolo adecuado para herramientas de visualización como Power BI.

### Funcionalidad

1.  **Carga de Datos**:
    *   Lee un archivo de datos de SPSS (`.sav`) que contiene las respuestas de la encuesta.
    *   Lee un archivo de Excel (`Indice.xlsx`) que sirve como diccionario de datos, conteniendo metadatos como las preguntas completas y la clasificación de las variables.

2.  **Limpieza Inicial**:
    *   Convierte todos los nombres de las columnas a minúsculas para estandarizar el formato.

3.  **Clasificación de Variables**:
    *   Las columnas se dividen en tres categorías principales:
        *   **`segmentadores`**: Variables demográficas o de corte (ej. `sexo`, `edad_tramo`).
        *   **`simples`**: Preguntas de respuesta única.
        *   **`compuestas`**: Preguntas de respuesta múltiple, donde cada opción es una columna separada.

4.  **Transformación de Datos (Pivot)**:
    *   Los `DataFrames` de variables `simples` y `compuestas` se transforman de un formato ancho a uno largo (`melt`). Esto crea una estructura donde cada fila representa una respuesta a una pregunta, en lugar de un encuestado.

5.  **Enriquecimiento con Metadatos**:
    *   El `DataFrame` transformado se une con los metadatos del archivo `Indice.xlsx`. Esto añade columnas con el texto completo de las preguntas y las opciones, proporcionando un contexto claro para cada respuesta.

6.  **Limpieza Adicional**:
    *   Se eliminan las filas donde el valor es `Unchecked`, que son comunes en las preguntas de opción múltiple y no aportan información para el análisis.
    *   Se realizan ajustes específicos en los datos de los segmentadores, como agrupar departamentos o manejar valores faltantes.

7.  **Generación de Archivos de Salida**:
    *   El notebook exporta varios archivos `.csv` que son el producto final del pipeline:
        *   `df_pivoted_without_unchecked.csv`: Contiene los datos principales en formato largo.
        *   `df_segmentadores_pivoted.csv`: Contiene los datos de los segmentadores en formato largo.
        *   `df_segmentadores_with_totals.csv`: Una versión de los datos de segmentadores con totales agregados para facilitar el análisis.

## Flujo de Trabajo General

El flujo de trabajo se puede dividir en dos rutas principales:

1.  **Ruta de Muestra (para pruebas y desarrollo)**:
    *   **Paso 1**: Se utiliza `sample_generator.py` para crear un archivo `sample_dataset.sav` a partir de datos de ejemplo en Excel.
    *   **Paso 2**: Se abre `sample_analyzer.ipynb` para inspeccionar rápidamente el conjunto de datos de muestra y verificar que se haya generado correctamente.

2.  **Ruta de Producción (para el análisis principal)**:
    *   **Paso 1**: Se ejecuta el notebook `column_transformation.ipynb` con el conjunto de datos de la encuesta real (en formato `.sav`) y el diccionario de datos (`Indice.xlsx`).
    *   **Paso 2**: El notebook procesa los datos y genera los archivos `.csv` finales.
    *   **Paso 3**: Estos archivos `.csv` están listos para ser importados en herramientas de BI como Power BI o para ser utilizados en análisis estadísticos más profundos.