#!/bin/bash

# Activar el entorno virtual
source ~/venv/bin/activate

# Ejecutar el script de Python
python ~/mytilus2/app/forecast24h.py

# Actualizar git
git push origin main
