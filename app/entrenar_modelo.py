import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import pickle
import numpy as np
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import os

# Obtener el directorio actual del script
base_dir = os.path.abspath(os.path.dirname(__file__))

# Ruta completa al archivo CSV
csv_path = os.path.join(base_dir, 'cangas_IU.csv')

# Cargar los datos
data = pd.read_csv(csv_path)

# Convertir la columna 'fecha' a formato de fecha
data['fecha'] = pd.to_datetime(data['fecha'])

# Dividir los datos en características (X) y etiquetas (y)
X = data[['fecha', 'UI']]
y = data['abierto/cerrado']

# Convertir la columna 'fecha' a características numéricas (día, mes y año)
X['dia'] = X['fecha'].dt.day
X['mes'] = X['fecha'].dt.month
X['año'] = X['fecha'].dt.year

# Eliminar la columna original 'fecha' ya que se ha convertido en características numéricas
X = X.drop('fecha', axis=1)

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Eliminar filas con valores NaN en los conjuntos de entrenamiento y prueba
X_train = X_train.dropna()
y_train = y_train[X_train.index]  # Asegurarse de que y_train tenga la misma longitud que X_train

X_test = X_test.dropna()
y_test = y_test[X_test.index]  # Asegurarse de que y_test tenga la misma longitud que X_test

# Luego, puedes proceder con el entrenamiento y evaluación de los modelos.

from sklearn.ensemble import RandomForestClassifier
# Crear el modelo
decision_tree = RandomForestClassifier(random_state=14)


# Entrenar el modelo
decision_tree.fit(X_train, y_train)

# Guardar el modelo entrenado en un archivo
with open('decision_tree_model.pkl', 'wb') as file:
    pickle.dump(decision_tree, file)
