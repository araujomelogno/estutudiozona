# Importar las bibliotecas necesarias
import pandas as pd
import pyreadstat

# --- Carga de Datos ---
# Define la ruta del archivo de Excel que contiene los datos de la encuesta.
# NOTA: Esta es una ruta local y necesitará ser ajustada si el script se ejecuta en una máquina diferente.
file_path = "/Users/blanc/Library/CloudStorage/GoogleDrive-dblancbellido@gmail.com/.shortcut-targets-by-id/153DRxBD4jspE3sko8JH1R6j2AYv7OrgD/PBI - Comunidad Zona/datos/course_example.xlsx"
# Carga la hoja 'Sheet1' del archivo Excel en un DataFrame de pandas.
df = pd.read_excel(file_path, sheet_name='Sheet1')
# Imprime las primeras filas del DataFrame para una verificación rápida.
print(df.head())

# --- Extracción de Metadatos y Datos ---
# El script asume una estructura específica en el archivo Excel:
# - La primera fila contiene los nombres de las variables (ej. 'region', 'sexo').
# - La segunda fila contiene las etiquetas de las variables (ej. 'En qué región vive?', 'Cúal es su sexo?').
# - Las filas subsiguientes contienen los datos de los encuestados.

# Extrae los nombres de las columnas del DataFrame para usarlos como nombres de variables.
variable_names = df.columns.tolist()
# Extrae la primera fila de datos (índice 0) para usarla como etiquetas de las variables.
variable_labels = df.iloc[0]
# Selecciona el resto de las filas como los datos reales de la encuesta y resetea el índice.
data = df.iloc[1:].reset_index(drop=True)

# --- Mapeo de Valores Categóricos a Numéricos ---
# Define un diccionario para mapear respuestas de texto a códigos numéricos.
# SPSS trabaja internamente con valores numéricos y les asocia etiquetas de valor.
mappings = {
    "region": {"Montevideo": 1, "Interior": 2},
    "sexo": {"Hombre": 1, "Mujer": 2},
    "a1": {"Muy buena": 1, "Buena": 2, "Mala": 3, "Muy mala": 4}
}

# Itera sobre el diccionario de mapeos.
for col, mapping in mappings.items():
    # Verifica si la columna existe en el DataFrame de datos.
    if col in data.columns:
        # Aplica el mapeo para convertir los valores de texto a numéricos.
        data[col] = data[col].map(mapping)

# --- Preparación de Metadatos para SPSS ---
# Convierte la serie de pandas con las etiquetas de las variables a un diccionario.
variable_label_dict = variable_labels.to_dict()

# Define un diccionario para las etiquetas de los valores.
# Esto le dice a SPSS qué etiqueta de texto corresponde a cada código numérico.
value_label_dict = {
    "region": {1: "Montevideo", 2: "Interior"},
    "sexo": {1: "Hombre", 2: "Mujer"},
    "a1": {1: "Muy buena", 2: "Buena", 3: "Mala", 4: "Muy mala"}
}

# --- Creación del Archivo .sav ---
# Define el nombre y la ruta del archivo de salida de SPSS.
sav_file_path = "sample_dataset.sav"
# Utiliza pyreadstat para escribir el DataFrame en un archivo .sav.
# - `variable_value_labels`: Asigna las etiquetas de texto a los valores numéricos.
# - `column_labels`: Asigna las etiquetas de las variables a las columnas.
pyreadstat.write_sav(data, sav_file_path,
                    variable_value_labels=value_label_dict,
                    column_labels=variable_label_dict)

# Imprime un mensaje de confirmación indicando dónde se guardó el archivo.
print(f"File saved at: {sav_file_path}")