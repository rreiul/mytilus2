import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta, date
import os
import io


url = 'http://www.intecmar.gal/Informacion/biotoxinas/Evolucion/CierresBatea.aspx'


response = requests.get(url)


if response.status_code == 200:

    soup = BeautifulSoup(response.content, 'html.parser')
    
    table = soup.find('table', {'id': 'ctl00_Contenido_GridView2'})
    
    if table:
        df_hoy = pd.read_html(str(table))[0]
                
        df_hoy = df_hoy.rename(columns={'Xan': '1', 'Feb': '2', 'Mar': '3', 'Abr': '4', 'Mai': '5', 'Xun': '6', 'Xull': '7', 'Ago': '8', 'Set': '9', 'Out': '10', 'Nov': '11', 'Dec': '12'})
        df_hoy = df_hoy.fillna('0')

        df_hoy = df_hoy[df_hoy['Polígono'] != '0']

        script_dir = os.path.dirname(__file__) 

        hoy = date.today()
        ayer_fecha = hoy - timedelta(1)
        mes = hoy.month
        mes = str(mes)
        ayer_fecha = str(ayer_fecha)
        hoy_fecha = str(hoy)
        
        csv = os.path.join(os.path.dirname(__file__), 'data', 'abiertocerrado_scrap.csv')
        df2 = pd.read_csv(csv)
        
        csv = os.path.join(os.path.dirname(__file__), 'data', 'diascierre_ayer.csv')
        df_ayer = pd.read_csv(csv)

        existe_valor = (df2['dia'] == ayer_fecha).any()

        if hoy.weekday() == 0:
            print('Hoy es lunes, por lo que no se actualizan los datos.')
        elif hoy.weekday() == 6:
            if not (df2['dia'] == hoy_fecha).any():
                ultima_fila = df2.iloc[-1]
                nueva_fila = ultima_fila.copy()
                nueva_fila['dia'] = hoy - timedelta(1)
                df2.loc[len(df2)] = nueva_fila
                nueva_fila['dia'] = hoy
                df2.loc[len(df2)] = nueva_fila
            else:
                print('Ya se ha ejecutado el script hoy.')
        elif hoy.weekday() in [1,2,3,4,5]:
            if not existe_valor:
                for index, row_ayer in df_ayer.iterrows():
                    polig = row_ayer['Polígono']
                    df_hoy_poligono = df_hoy[df_hoy['Polígono'] == polig]
                    v_hoy = df_hoy_poligono[mes].iloc[0]
                    df_ayer_poligono = df_ayer[df_ayer['Polígono'] == polig]
                    v_ayer = df_ayer_poligono[mes].iloc[0]
                    v_hoy = int(v_hoy)
                    v_ayer = int(v_ayer)
                    existe_valor = (df2['dia'] == ayer_fecha).any()
                    if v_ayer != v_hoy:
                        if existe_valor:
                            df2.loc[df2['dia'] == ayer_fecha, polig] = 1.0
                        else:
                            nueva_fila = {'dia': ayer_fecha, polig: 1.0}
                            df2.loc[len(df2)] = nueva_fila
                    else:
                        if existe_valor:
                            df2.loc[df2['dia'] == ayer_fecha, polig] = 0.0
                        else:
                            nueva_fila = {'dia': ayer_fecha, polig: 0.0}
                            df2.loc[len(df2)] = nueva_fila

        file_path = os.path.join(script_dir,'data','abiertocerrado_scrap.csv')
        df2.to_csv(file_path, index=False)
        file_path = os.path.join(script_dir,'data','diascierre_ayer.csv')
        df_hoy.to_csv(file_path, index=False)

    else:
        print('No se encontró la tabla en la página.')
else:
    print('No se pudo acceder a la página.')