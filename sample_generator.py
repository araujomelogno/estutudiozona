import pandas as pd
import pyreadstat

# Load your data
file_path = "/Users/blanc/Library/CloudStorage/GoogleDrive-dblancbellido@gmail.com/.shortcut-targets-by-id/153DRxBD4jspE3sko8JH1R6j2AYv7OrgD/PBI - Comunidad Zona/datos/course_example.xlsx"
df = pd.read_excel(file_path, sheet_name='Sheet1')
print(df.head())
# Extract variable names, labels, and data
variable_names = df.columns.tolist()  # First row has variable names
variable_labels = df.iloc[0]  # Second row has variable labels
data = df.iloc[1:].reset_index(drop=True)  # Data starts from the third row

mappings = {
    "region": {"Montevideo": 1, "Interior": 2},
    "sexo": {"Hombre": 1, "Mujer": 2},
    "a1": {"Muy buena": 1, "Buena": 2, "Mala": 3, "Muy mala": 4}
}

for col, mapping in mappings.items():
    if col in data.columns:
        data[col] = data[col].map(mapping)

# Prepare metadata
variable_label_dict = variable_labels.to_dict()

value_label_dict = {
    "region": {1: "Montevideo", 2: "Interior"},
    "sexo": {1: "Hombre", 2: "Mujer"},
    "a1": {1: "Muy buena", 2: "Buena", 3: "Mala", 4: "Muy mala"}
}

sav_file_path = "sample_dataset.sav"
pyreadstat.write_sav(data, sav_file_path, 
                    variable_value_labels=value_label_dict, 
                    column_labels=variable_label_dict)
print(f"File saved at: {sav_file_path}")