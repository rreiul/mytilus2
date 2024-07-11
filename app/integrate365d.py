# Librerías utilizadas en este script
import pandas as pd
import os
import numpy as np

# Definir ruta del archivo abiertocerrado1.csv
csv = os.path.join(os.path.dirname(__file__), 'data', 'abiertocerrado1.csv')

# Leer abiertocerrado1.csv y pasarlo a Dataframe
d1 = pd.read_csv(csv)

# Definir ruta del archivo abiertocerrado_scrap.csv
csv = os.path.join(os.path.dirname(__file__), 'data', 'abiertocerrado_scrap.csv')

# Leer abiertocerrado_scrap.csv y pasarlo a Dataframe
d2 = pd.read_csv(csv)

# Combinar ambos Dataframes
df_combined = pd.concat([d1, d2], ignore_index=True)

# Exportar Dataframe combinado a abiertocerrado1.csv
csv = os.path.join(os.path.dirname(__file__), 'data', 'abiertocerrado1.csv')
df_combined.to_csv(csv)
