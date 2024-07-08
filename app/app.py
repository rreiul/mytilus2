from flask import Flask, render_template, request, url_for
import csv
import os
import pandas as pd

app = Flask(__name__)

# Configuración de la carpeta estática
app.static_folder = 'static'

@app.route('/', methods=['GET', 'POST'])
def index():
    script_dir = os.path.dirname(__file__) 
    csv = os.path.join(os.path.dirname(__file__), 'data', 'porcentajes_rangofechas.csv')
    df = pd.read_csv(csv)

    zona = df['zona'].iloc[1]
    rango = df['rango'].iloc[1]
    porcentaje = df['porcentaje'].iloc[1]

    opciones = df['zona'].tolist()

    if request.method == 'POST':
        zona_seleccionada = str(request.form['zona'])
        print(zona_seleccionada)
        fila_seleccionada = df[df['zona'] == zona_seleccionada]
        zona = str(fila_seleccionada['zona'].iloc[0])
        rango = str(fila_seleccionada['rango'].iloc[0])
        porcentaje = str(fila_seleccionada['porcentaje'].iloc[0])

    imagen1_filename = f"prediccion_{zona}.png"
    imagen1_url = url_for('static', filename=imagen1_filename)

    #imagen2_filename = f"curva_{zona}.png"
    #imagen2_url = url_for('static', filename=imagen2_filename)
        
    return render_template('index.html', zona=zona, rango=rango, porcentaje=porcentaje, opciones=opciones, imagen1_url=imagen1_url) #imagen2_url=imagen2_url)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')