#!/bin/bash

# Activar el entorno virtual
source /home/ubuntu/mytilus/venv/bin/activate

# Ejecutar el script de Python
python /home/ubuntu/mytilus/mytilus2/app/forecast24h.py
python /home/ubuntu/mytilus/mytilus2/app/scrap24h.py

#Actualizar git
git push origin main
