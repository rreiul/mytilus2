import pandas as pd
import os
import numpy as np

script_dir = os.path.dirname(__file__) 

csv = os.path.join(os.path.dirname(__file__), 'data', 'abiertocerrado.csv')
d1 = pd.read_csv(csv)
print(d1)
d1.fillna(value=np.nan, inplace=True)
csv = os.path.join(os.path.dirname(__file__), 'data', 'abiertocerrado1.csv')
d1.to_csv(csv, index=False)