# ===================================================================================
# ANÁLISIS Y PREPARACIÓN DE DATOS PARA POWER BI
# ===================================================================================
#
# Autor: Jules, Ingeniero de Software
# Fecha: 2025-10-06
#
# Descripción:
# Este script de R procesa una base de datos en formato SPSS (.sav) para su posterior
# uso en herramientas de visualización como Power BI.
#
# El script realiza las siguientes operaciones:
# 1. Carga las librerías necesarias para el análisis.
# 2. Importa los datos desde un archivo .sav.
# 3. Limpia los datos, estandarizando los nombres de las columnas a minúsculas.
# 4. Convierte las variables etiquetadas de SPSS a factores de R para facilitar
#    su interpretación.
# 5. Divide el conjunto de datos en dos tablas: una con variables de segmentación
#    y otra con variables de indicadores, manteniendo un ID común.
# 6. Exporta los datos procesados a archivos CSV.
#
# ===================================================================================

# --- PASO 1: Cargar Librerías ---
# Se cargan las librerías 'tidyverse' para la manipulación general de datos (incluye dplyr, readr)
# y 'haven' para leer archivos de formatos estadísticos como SPSS (.sav).

# install.packages("tidyverse") # Descomentar y ejecutar si no tienes 'tidyverse' instalado
# install.packages("haven")     # Descomentar y ejecutar si no tienes 'haven' instalado

library(tidyverse)
library(haven)

# --- PASO 2: Importar Datos ---
# Se leen los datos desde el archivo 'BASE_PBI.sav'.
# Es importante que este archivo se encuentre en el directorio de trabajo de R.
# Puedes verificar tu directorio de trabajo con getwd() y cambiarlo con setwd("ruta/a/tu/directorio").

dfb <- read_sav('BASE_PBI.sav')

# --- PASO 3: Limpieza y Estandarización ---
# Se convierten todos los nombres de las columnas a minúsculas para facilitar
# su manipulación y evitar errores por mayúsculas/minúsculas.

colnames(dfb) <- tolower(colnames(dfb))

# Se crea una copia del dataframe con las etiquetas de SPSS convertidas a factores.
# Esto es útil para el análisis, ya que en lugar de ver códigos numéricos (ej: 1, 2),
# veremos las etiquetas de texto correspondientes (ej: "Masculino", "Femenino").
dfb_labels <- dfb %>% mutate(across(where(is.labelled), as_factor))


# --- PASO 4: Separación de Variables ---
# Se define un vector con los nombres de las columnas que se consideran
# "variables de segmentación" (ej: datos demográficos).

segmentadores <- c(
  'idbase',
  'sexo',
  'edad_tramo',
  'depto',
  'hijos',
  'barrio',
  'cargo_declarado',
  'edu_rec',
  'industria_rec',
  'modalidad_trabajo'
)

# Se crea un dataframe 'dfb_segmentadores' que contiene únicamente las columnas de segmentación.
dfb_segmentadores <- dfb_labels %>%
  select(all_of(segmentadores))

# Se crea un dataframe 'dfb_indicadores' que contiene el resto de las columnas (los indicadores),
# asegurándonos de mantener la columna 'idbase' para poder relacionar ambas tablas.
dfb_indicadores <- dfb_labels %>%
  select(-all_of(segmentadores)) %>%
  bind_cols(dfb_labels['idbase'])

# --- PASO 5: Exportación de Resultados ---
# Se guardan los dataframes procesados en archivos CSV.
# 'na = ""' asegura que los valores faltantes (NA) se guarden como celdas vacías.

# Exporta el dataframe con las etiquetas convertidas a factores.
# Este suele ser el más útil para análisis y visualización.
write_csv(dfb_labels, 'dfb_labels.csv', na = '')

# Exporta el dataframe con los datos originales (valores numéricos en lugar de etiquetas).
write_csv(dfb, 'dfb_original_limpio.csv', na = '')

# Exporta las tablas de segmentadores e indicadores por separado.
write_csv(dfb_segmentadores, 'dfb_segmentadores.csv', na = '')
write_csv(dfb_indicadores, 'dfb_indicadores.csv', na = '')

# --- FIN DEL SCRIPT ---
# Se muestra un mensaje en la consola indicando que el proceso ha finalizado con éxito.
print("Proceso completado. Los archivos CSV han sido generados en el directorio de trabajo.")