from datetime import timedelta, date
import pandas as pd
from prophet import Prophet
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
import os
import matplotlib.pyplot as plt
from matplotlib.dates import MonthLocator, DateFormatter

script_dir = os.path.dirname(__file__) 

fecha_actual = date.today()

fecha_final = fecha_actual + timedelta(days=90)

rango_fechas = pd.date_range(start=fecha_actual, end=fecha_final, freq='D')

df_fechas = pd.DataFrame(rango_fechas, columns=['fecha'])

#
#
# HACER MERGE DE LAS PREDICCIONES
#
#

csv = os.path.join(os.path.dirname(__file__), 'data', 'abiertocerrado.csv')
df = pd.read_csv(csv)
df = df[['fecha', 'abierto/cerrado']].rename(columns={'fecha': 'ds', 'abierto/cerrado': 'y'})

df['ds'] = pd.to_datetime(df['ds'], format='%d/%m/%Y')

train_size = 0.8  # 80% para entrenamiento
train, test = train_test_split(df, train_size=train_size, shuffle=False, random_state=42)

# Inicializar el modelo Prophet desactivando la tendencia y la estacionalidad
model = Prophet(growth='flat', seasonality_prior_scale=0.1, changepoint_prior_scale=0.5)
# Entrenar el modelo
model.fit(train)

# Realizar predicciones en el conjunto de prueba
df_fechas = df_fechas[['fecha']].rename(columns={'fecha': 'ds'})
forecast = model.predict(df_fechas)
forecast[['ds', 'yhat']].to_csv('forecast.csv', index=False)

# Convertir las predicciones en valores binarios
#threshold = 0.5  # Umbral para la clasificación
#forecast['yhat_binary'] = (forecast['yhat'] > threshold).astype(int)

csv = os.path.join(os.path.dirname(__file__), 'data', 'forecast.csv')
forecast[['ds', 'yhat']].to_csv(csv, index=False)

#####################################################

# Leer datos y configurar índice
csv = os.path.join(os.path.dirname(__file__), 'data', 'forecast.csv')
df = pd.read_csv(csv)

df['ds'] = pd.to_datetime(df['ds'])  # Asegurarse de que 'ds' sea de tipo fecha
#df.set_index('ds', inplace=True)

ranges = [(0.8, 2, 'red', 1),
          (0.6, 0.8, 'orange', 1),
          (0.4, 0.6, 'yellow', 1),
          (0.2, 0.4, 'green', 1),
          (-1, 0.2, 'blue', 1)]  # Ordenados de mayor a menor para que el rojo esté primero

# Graficar la serie de tiempo
plt.rcParams['font.family'] = 'Segoe UI'
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(20,6))
ax.set_facecolor('#14181E')
ax.plot(df['ds'], df['yhat'],  linestyle='-', color='w')

for ymin, ymax, color, alpha in ranges:
    fechas_a_pintar = df[(df['yhat'] >= ymin) & (df['yhat'] < ymax)]['ds']
    for date in fechas_a_pintar:
        ax.axvspan(date, date + pd.Timedelta(days=1), color=color, alpha=1)

png = os.path.join(os.path.dirname(__file__), 'static', 'prediccion.png')
plt.savefig(png, transparent=True, bbox_inches='tight', dpi=94)


