library(tidyverse)
library(haven)

df = read_sav('BASE_PBI.sav')

head(df)

colnames(df) = tolower(colnames(df))

segmentadores = c(
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

df_segmentadores = df %>% 
  select(all_of(segmentadores))

df_indicadores = df %>% 
  select(-all_of(segmentadores)) %>% 
  bind_cols(df['idbase'])



write_csv(df, 'df.csv', na = '')
