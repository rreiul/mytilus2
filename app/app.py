from flask import Flask, render_template_string
import pandas as pd
import plotly.graph_objects as go
import pickle
import os

app = Flask(__name__)

# Cargar el modelo previamente entrenado
with open('decision_tree_model.pkl', 'rb') as file:
    decision_tree = pickle.load(file)

@app.route('/')
def home():
    # Obtener el directorio actual del script
    base_dir = os.path.abspath(os.path.dirname(__file__))

    # Ruta completa al archivo CSV
    csv_path = os.path.join(base_dir, 'cangas_IU_2018.csv')

    # Cargar los datos
    data2 = pd.read_csv(csv_path)

    # Convertir la columna 'fecha' a formato de fecha
    data2['fecha'] = pd.to_datetime(data2['fecha'])

    # Convertir la columna 'fecha' a características numéricas (día, mes y año)
    data2['dia'] = data2['fecha'].dt.day
    data2['mes'] = data2['fecha'].dt.month
    data2['año'] = data2['fecha'].dt.year

    # Guardar la columna 'fecha' y 'abierto/cerrado' para su uso posterior
    fechas = data2['fecha']
    abierto_cerrado = data2['abierto/cerrado']

    # Eliminar la columna original 'fecha' ya que se ha convertido en características numéricas
    data2 = data2.drop('fecha', axis=1)

    # Eliminar la columna 'abierto/cerrado' para la predicción
    data2 = data2.drop('abierto/cerrado', axis=1)

    # Realizar la predicción usando el modelo entrenado
    prediccion = decision_tree.predict(data2)

    # Crear un DataFrame con los resultados
    resultados = pd.DataFrame({
        'fecha': fechas,
        'Real': abierto_cerrado,
        'Predicción': prediccion
    })

    # Crear un gráfico interactivo con Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=resultados['fecha'], y=resultados['Real'], mode='lines', name='Real', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=resultados['fecha'], y=resultados['Predicción'], mode='lines', name='Predicción', line=dict(color='red')))

    # Convertir el gráfico a HTML
    graph_html = fig.to_html(full_html=False)

    # Renderizar el gráfico en la plantilla HTML
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Gráfico Interactivo</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    </head>
    <body>
        <h1>Comparación entre valores reales y predicciones</h1>
        <div>{{ graph_html | safe }}</div>
    </body>
    </html>
    ''', graph_html=graph_html)

if __name__ == '__main__':
    app.run(debug=True)