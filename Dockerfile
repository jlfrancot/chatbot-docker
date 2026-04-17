# Imagen base oficial de Python 3.11 versión ligera
FROM python:3.11-slim

# Evita que Python escriba archivos .pyc y que bufferice la salida
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalar las dependencias necesarias para Tkinter y X11
RUN apt-get update && apt-get install -y \
    python3-tk \
    tk-dev \
    libx11-6 \
    && rm -rf /var/lib/apt/lists/*

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar los archivos de la aplicación al contenedor
COPY app.py .
COPY base_datos.json .

# Puerto estándar del protocolo X11 (Tkinter usa display gráfico, no HTTP)
EXPOSE 6000

# Ejecutar la aplicación al iniciar el contenedor
CMD ["python3", "app.py"]
