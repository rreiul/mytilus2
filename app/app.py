from flask import Flask, render_template, send_file
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import MonthLocator, DateFormatter
import os
import io

app = Flask(__name__)

@app.route('/')
def index():
    csv = os.path.join(os.path.dirname(__file__), 'forecast.csv')
    df = pd.read_csv(csv)
    df['ds'] = pd.to_datetime(df['ds'])

    ranges = [(0.8, 2, 'red', 1),
              (0.6, 0.8, 'orange', 1),
              (0.4, 0.6, 'yellow', 1),
              (0.2, 0.4, 'green', 1),
              (-1, 0.2, 'blue', 1)]  

    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(20,6))

    ax.plot(df['ds'], df['yhat'],  linestyle='-', color='w')
    fechas_a_pintar = df[df['yhat'] < 0.34]['ds']
    for ymin, ymax, color, alpha in ranges:
        fechas_a_pintar = df[(df['yhat'] >= ymin) & (df['yhat'] < ymax)]['ds']
        for date in fechas_a_pintar:
            ax.axvspan(date, date + pd.Timedelta(days=1), color=color, alpha=1)
    plt.title('Predicción de estado')

    # Guardar el gráfico en un archivo temporal
    img_bytes = io.BytesIO()
    plt.savefig(img_bytes, format='png')
    img_bytes.seek(0)

    # Limpiar la figura para liberar memoria
    plt.close()

    # Mostrar la imagen en la página web
    return render_template('index.html', image=img_bytes)

if __name__ == '__main__':
    app.run(debug=True)
