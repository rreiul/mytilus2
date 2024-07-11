# Librerías utilizadas en este script
from datetime import timedelta, date
import pandas as pd
from prophet import Prophet
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
from sklearn.model_selection import TimeSeriesSplit
import os
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.dates import MonthLocator, DateFormatter
import numpy as np

# Definir fecha de hoy
fecha_actual = date.today()

# Definir fecha final, 3 meses más que hoy
fecha_final = fecha_actual + timedelta(days=90)

# Crear un rango de fechas desde hoy a la final
rango_fechas = pd.date_range(start=fecha_actual, end=fecha_final, freq='D')

# Crear Dataframe con el rango de fechas
df_fechas = pd.DataFrame(rango_fechas, columns=['dia'])

# Renombrar columna dia
df_fechas = df_fechas[['dia']].rename(columns={'dia': 'ds'})

# Definir diccionario de rangos de colores
ranges = [(0.8, 2, 'red', 1),
          (0.6, 0.8, 'orange', 1),
          (0.4, 0.6, 'yellow', 1),
          (0.2, 0.4, 'green', 1),
          (-1, 0.2, 'blue', 1)] 

# Leer y pasar a Dataframe abiertocerrado1.csv
csv = os.path.join(os.path.dirname(__file__), 'data', 'abiertocerrado1.csv')
df = pd.read_csv(csv)

# Iterar columnas del Dataframe
for column in df.columns:
    print(column)

    # Omitir la primera
    if column=='dia':
        continue
    
    # Crear un Dataframe con columnas dia y column actual
    df2 = df[['dia', column]]

    # Omitir columnas vacías
    if df2[column].isna().any():
        continue
    
    # Renombrar las columnas para usar Prophet
    df2 = df2.rename(columns={'dia': 'ds', column: 'y'})

    # Pasar dia a formato datetime
    df2['ds'] = pd.to_datetime(df2['ds'], format='%d/%m/%Y')

    # Crear objeto TimeSeriesSplit para dividir los datos
    tscv = TimeSeriesSplit(n_splits=4)
    accuracies = []

    # Entrenar el modelo
    for train_index, test_index in tscv.split(df2):
        train_df, test_df = df2.iloc[train_index], df2.iloc[test_index]

        # Crear modelo y entrenarlo
        model = Prophet(growth='flat', seasonality_prior_scale=0.1, changepoint_prior_scale=0.5)
        model.fit(train_df)

        # Predecir el conjunto de prueba
        future = test_df[['ds']].copy() 
        forecast = model.predict(future)

        # Combertir predicciones a binarias según umbral
        threshold = 0.5  
        forecast['yhat_binary'] = (forecast['yhat'] > threshold).astype(int)

        # Evaluar el modelo
        accuracy = accuracy_score(test_df['y'], forecast['yhat_binary'])
        accuracies.append(accuracy)

    # Calcular las métricas promedio
    avg_accuracy = round(np.mean(accuracies),3)
    avg_accuracy = avg_accuracy * 100
    print(f"Average Accuracy: {avg_accuracy:.2f}")

    # Predecir sobre el rango de fechas futuras
    forecast = model.predict(df_fechas)
    csv = os.path.join(os.path.dirname(__file__), 'data', 'forecast_' + column + '.csv')
    forecast[['ds', 'yhat']].to_csv(csv, index=False)

    # Convertir columna a formato datetime
    forecast['ds'] = pd.to_datetime(forecast['ds'])

    print(forecast)

    # Configuración de gráficos
    plt.rcParams['font.family'] = 'Segoe UI'
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(20,6))
    ax.set_facecolor('#14181E')

    # Crear leyenda
    red_patch = Patch(color='red', label='Altamente probable que esté cerrado')
    orange_patch = Patch(color='orange', label='Muy probable que esté cerrado')
    yellow_patch = Patch(color='yellow', label='Moderadamente probable que esté cerrado')
    green_patch = Patch(color='green', label='Poco probable que esté cerrado')
    blue_patch = Patch(color='blue', label='Muy poco probable que esté cerrado')
    ax.legend(loc='upper center', bbox_to_anchor=(0.5,1.1), handles=[red_patch, orange_patch, yellow_patch, green_patch, blue_patch], ncol=5)

    # Pintar áreas de predicción con colores
    for ymin, ymax, color, alpha in ranges:
        fechas_a_pintar = forecast[(forecast['yhat'] >= ymin) & (forecast['yhat'] < ymax)]['ds']
        for date in fechas_a_pintar:
            ax.axvspan(date, date + pd.Timedelta(days=1), color=color, alpha=1)

    # Exportar gráficos
    png = os.path.join(os.path.dirname(__file__), 'static', 'prediccion_' + column + '.png')
    plt.savefig(png, transparent=True, bbox_inches='tight', dpi=150)

    # Leer porcentajes_rangofechas.csv y pasar a Dataframe
    csv = os.path.join(os.path.dirname(__file__), 'data', 'porcentajes_rangofechas.csv')
    df_porcentaje_rangos = pd.read_csv(csv)
    
    # Crear rangos de fechas
    primera_fecha = df2['ds'].iloc[0].date()
    ultima_fecha = df2['ds'].iloc[-1].date()

    rango = str(primera_fecha) + ' - ' + str(ultima_fecha)

    to_add = {'zona' : column,
              'porcentaje' : avg_accuracy,
              'rango' : rango}
    
    fila_existente = df_porcentaje_rangos[(df_porcentaje_rangos['zona'] == to_add['zona'])]

    if not fila_existente.empty:
        df_porcentaje_rangos.loc[fila_existente.index, 'porcentaje'] = to_add['porcentaje']
        df_porcentaje_rangos.loc[fila_existente.index, 'rango'] = to_add['rango']
    else:
        df_porcentaje_rangos = df_porcentaje_rangos._append(to_add, ignore_index=True)

    # Exportar df_porcentaje_rangos
    df_porcentaje_rangos.to_csv(csv, index=False)

    
