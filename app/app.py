# Librerías utilizadas en este script
from flask import Flask, render_template, request, url_for
import csv
import os
import pandas as pd

# Nombre de la aplicación
app = Flask(__name__)

# Configuración de la carpeta estática
app.static_folder = 'static'

# Definir la ruta principal que maneja peticiones GET y POST
@app.route('/', methods=['GET', 'POST'])
def index():
    # Definir ruta del archivo porcentajes_rangofechas.csv
    csv = os.path.join(os.path.dirname(__file__), 'data', 'porcentajes_rangofechas.csv')

    # Leer porcentajes_rangofechas.csv y pasarlo a Dataframe
    df = pd.read_csv(csv)

    # Definir valores iniciales para zona, rango y porcentaje
    zona = df['zona'].iloc[1]
    rango = df['rango'].iloc[1]
    porcentaje = df['porcentaje'].iloc[1]

    # Crear lista de opciones a partir de la columna 'zona'
    opciones = df['zona'].tolist()

    # Si se recibe una solicitud POST
    if request.method == 'POST':

        # Obtener zona seleccionada
        zona_seleccionada = str(request.form['zona'])

        # Filtrar Dataframe para obtener la fila correspondiente a la zona seleccionada
        fila_seleccionada = df[df['zona'] == zona_seleccionada]

        # Actualizar valores de zona, rango y porcentaje
        zona = str(fila_seleccionada['zona'].iloc[0])
        rango = str(fila_seleccionada['rango'].iloc[0])
        porcentaje = str(fila_seleccionada['porcentaje'].iloc[0])

    # Construir URL de la imagen a mostrar
    imagen1_filename = f"prediccion_{zona}.png"
    imagen1_url = url_for('static', filename=imagen1_filename)
    
    # Renderizar plantilla con variables necesarias
    return render_template('index.html', zona=zona, rango=rango, porcentaje=porcentaje, opciones=opciones, imagen1_url=imagen1_url)

# Iniciar la aplicación flask
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')