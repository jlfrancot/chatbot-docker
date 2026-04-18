# Chatbot sobre comandos Docker con Python, Tkinter y Docker

Aplicación de escritorio desarrollada en Python con Tkinter que permite consultar comandos de Docker a través de un chatbot.  
La aplicación está contenerizada con Docker y desplegada mediante Docker Compose, utilizando X11 para mostrar la interfaz gráfica desde el contenedor.

---

## Índice

- Descripción
- Tecnologías
- Requisitos
- Instalación y ejecución
- Dockerfile
- Docker Compose
- Problemas y soluciones
- Flujo de trabajo con Git
- Estructura del proyecto

---

## Descripción

El chatbot se ejecuta en una ventana gráfica creada con Tkinter, donde el usuario puede escribir preguntas relacionadas con comandos de Docker.

Funcionamiento:

- El usuario introduce una consulta  
- El sistema analiza palabras clave (mínimo 2 caracteres)  
- Busca coincidencias en `base_datos.json`  
- Devuelve una respuesta junto con un enlace a la documentación oficial  

---

## Tecnologías

- Python 3.11
- Tkinter (interfaz gráfica)
- JSON (base de datos)
- Docker
- Docker Compose
- X11 (interfaz gráfica desde contenedor)

---

## Requisitos

Antes de ejecutar el proyecto necesitas:

- Sistema Linux con entorno gráfico (recomendado: Ubuntu)
- Docker instalado
- Docker Compose instalado

Instalación en Ubuntu:

```bash
sudo apt update
sudo apt install docker.io docker-compose -y
```

---

## Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/chatbot-docker.git
cd chatbot-docker
```

### 2. Permitir acceso gráfico desde Docker

```bash
xhost +local:docker
```

### 3. Construir la imagen

```bash
docker build -t chatbot-docker .
```

### 4. Ejecutar la aplicación

```bash
docker-compose up
```

Al ejecutar el contenedor, se abrirá automáticamente la ventana del chatbot en el escritorio del host.

---

## Dockerfile

```dockerfile
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
# Puerto estándar del protocolo X11. Tkinter usa display gráfico en lugar de HTTP, por lo que la
# comunicación se realiza a través del socket X11 (/tmp/.X11-unix) y no por un puerto HTTP convencional.
EXPOSE 6000
# Comando que se ejecuta al arrancar el contenedor.
CMD ["python3", "app.py"]

```

---

## Docker Compose

### Variables de entorno

```yaml
environment:
  - DISPLAY=${DISPLAY}
```

### Volúmenes

```yaml
volumes:
  - /tmp/.X11-unix:/tmp/.X11-unix
  - ./base_datos.json:/app/base_datos.json
```

### Red

```yaml
network_mode: host
```

---

## Problemas y soluciones

### Error: cannot open display

```bash
xhost +local:docker
docker-compose up
```

---

### Error: docker: unknown command: docker compose
La versión de Docker instalada no incluye el plugin Compose. 
```bash
sudo apt install docker-compose
```

Usar:

```bash
docker-compose
```

---

### Error: unable to evaluate symlinks in Dockerfile path
Significa que no estás en la carpeta del proyecto, ir a la ruta primero.
```bash
cd ~/chatbot-docker
docker build -t chatbot-docker .
```

---

## Flujo de trabajo con Git

El proyecto sigue un flujo basado en ramas por funcionalidad:

```
main
├── feature/app
├── feature/docker
└── feature/docs
```

### Proceso de trabajo

1. Crear ramas:

```bash
git checkout -b feature/app
git checkout -b feature/docker
```

2. Desarrollar la funcionalidad y hacer commits  
```bash
git add app.py base_datos.json
git commit -m "feat: añadir chatbot con Tkinter y base de datos JSON"

git add Dockerfile docker-compose.yml
git commit -m "feat: añadir Dockerfile y docker-compose.yml"
```
3. Subir la rama:

```bash
git push origin feature/app
git push origin feature/docker
```

4. Crear un Pull Request en GitHub  

5. Fusionar en main  

6. Actualizar en local:

```bash
git pull origin main
```

---

## Estructura del proyecto

```
chatbot-docker/
├── app.py
├── base_datos.json
├── Dockerfile
├── docker-compose.yml
└── README.md
```
