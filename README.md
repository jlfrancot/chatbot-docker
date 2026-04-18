Chatbot Docker en Pyton con Tkinter
Chatbot con interfaz gráfica desarrollado en Python con Tkinter, le chat responde preguntas sobre comandos de Docker consultando una base de en formato JSON. La aplicación está creada con Docker y desplegada con Docker Compose.
Descripción del proyecto
El chatbot funciona en una ventana gráfica (Tkinter) y permite al usuario escribir preguntas sobre comandos Docker. El programa busca en un archivo base_datos.json la respuesta comparando palabras clave de como mínimo 2 caracteres, luego muestra el resultado junto con un enlace a la documentación oficial.
Tecnologías utilizadas:
•	Python 3.11
•	Tkinter (interfaz gráfica)
•	JSON (base de conocimiento)
•	Docker + Docker Compose
•	X11 (comunicación gráfica entre contenedor y host)

Instrucciones de instalación y despliegue
Requisitos previos
•	Ubuntu (o sistema Linux con entorno gráfico)
•	Docker instalado
•	Docker Compose instalado
sudo apt install docker.io docker-compose -y
1. Clonar el repositorio
git clone https://github.com/tu-usuario/chatbot-docker.git
cd chatbot-docker
2. Permitir conexiones gráficas desde Docker
xhost +local:docker
3. Construir la imagen
docker build -t chatbot-docker .
4. Levantar los servicios con Docker Compose
docker-compose up
Se abrirá automáticamente la ventana gráfica del chatbot en tu escritorio.

Explicación del Dockerfile
# Imagen base oficial de Python 3.11 versión ligera
FROM python:3.11-slim
# Evitan la generación de archivos .pyc y aseguran que los logs aparezcan en tiempo real.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Instala las dependencias necesarias para que Tkinter pueda conectarse al servidor gráfico X11 del host.
RUN apt-get update && apt-get install -y \
    python3-tk \
    tk-dev \
    libx11-6 \
    && rm -rf /var/lib/apt/lists/*
# Establece el directorio de trabajo y copia los archivos de la aplicación al contenedor.
WORKDIR /app
COPY app.py .
COPY base_datos.json .
# Puerto estándar del protocolo X11. Tkinter usa display gráfico en lugar de HTTP, por lo que la # comunicación se realiza a través del socket X11 (/tmp/.X11-unix) y no por un puerto HTTP     # convencional.
EXPOSE 6000
# Comando que se ejecuta al arrancar el contenedor.
CMD ["python3", "app.py"]
Explicación del docker-compose.yml
environment:
  - DISPLAY=${DISPLAY}
Pasa la variable de pantalla del host al contenedor para que Tkinter sepa dónde dibujar la ventana.
volumes:
  - /tmp/.X11-unix:/tmp/.X11-unix
  - ./base_datos.json:/app/base_datos.json
Dos volúmenes montados:
•	El socket X11 permite mostrar la ventana gráfica en el escritorio del host.
•	El archivo base_datos.json se monta desde la carpeta local, lo que permite moodificar la base de datos sin reconstruir la imagen.
network_mode: host
El contenedor comparte la red del host para la comunicación con el servidor X11.

Problemas encontrados y soluciones
Error: cannot open display
xhost +local:
docker-compose up
Error: docker: unknown command: docker compose
La versión de Docker instalada no incluye el plugin Compose. Solución:
sudo apt install docker-compose
Y usar docker-compose (con guión) en lugar de docker compose.
Error: unable to evaluate symlinks in Dockerfile path
Significa que no estás en la carpeta del proyecto. Navega a ella primero:
cd ~/chatbot-docker
docker build -t chatbot-docker .

Organización del proyecto y flujo de ramas
El proyecto sigue un flujo de trabajo basado en ramas por funcionalidad:
main                ← versión estable
├── feature/app     ← código de la aplicación (app.py + base_datos.json)
├── feature/docker  ← contendores (Dockerfile + docker-compose.yml)
└── feature/docs    ← documentación (README.md)
Cada funcionalidad se desarrolla en su propia rama y se integra en main mediante un Pull Request, lo que permite revisar los cambios antes de fusionarlos.
Pasos seguidos:
1.	Se crea la rama con git checkout -b feature/”nombre de la rama”
2.	Se desarrolla la funcionalidad y se hacen commits descriptivos
3.	Se sube la rama con git push origin feature/”nombre de la rama”
4.	Se abre un Pull Request en GitHub y se fusiona en main
5.	Se actualiza main local con git pull origin main
Estructura del proyecto
chatbot-docker/
├── app.py               # Código principal del chatbot
├── base_datos.json      # Base de datos en JSON
├── Dockerfile           # Configuración de la imagen Docker
├── docker-compose.yml   # Orquestación de servicios
└── README.md            # Documentación del proyecto
