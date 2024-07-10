# Usa una imagen base oficial de Python
FROM python:3.11.9

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos de requerimientos primero para aprovechar el cache de Docker
COPY requirements.txt .

# Instala las dependencias. Agrega un --upgrade para asegurarte de que estás obteniendo las últimas versiones compatibles
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia el contenido del proyecto en el contenedor
COPY . .

# Expone el puerto en el que correrá la aplicación
EXPOSE 5000

# Comando por defecto para ejecutar la aplicación
CMD ["python", "app/app.py"]
