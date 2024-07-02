import pandas as pd
import os
import numpy as np

script_dir = os.path.dirname(__file__) 

csv = os.path.join(os.path.dirname(__file__), 'data', 'abiertocerrado1.csv')
d1 = pd.read_csv(csv)

csv = os.path.join(os.path.dirname(__file__), 'data', 'abiertocerrado_scrap.csv')
d2 = pd.read_csv(csv)

df_combined = pd.concat([d1, d2], ignore_index=True)
csv = os.path.join(os.path.dirname(__file__), 'data', 'abiertocerrado2.csv')
df_combined.to_csv(csv)
