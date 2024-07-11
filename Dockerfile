# Usar una imagen base oficial de Python
FROM python:3.11.9

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar los archivos de requerimientos primero para aprovechar el cache de Docker
COPY requirements.txt .

# Instalar las dependencias. Agrega un --upgrade para asegurarte de que estás obteniendo las últimas versiones compatibles
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar el contenido del proyecto en el contenedor
COPY . .

# Exponer el puerto en el que correrá la aplicación
EXPOSE 5000

# Ejecutar la aplicación
CMD ["python", "app/app.py"]
