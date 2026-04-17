# Importamos librerías necesarias
import json                       # Permite trabajar con archivos JSON (base de datos)
import tkinter as tk              # Librería para crear la interfaz gráfica
from tkinter import scrolledtext  # Widget de texto con scroll

# ---------------------------------------------------------
# FUNCIÓN: Cargar base de datos desde JSON
# ---------------------------------------------------------
def cargar_base_datos():
    try:
        with open("base_datos.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"preguntas": []}

# ---------------------------------------------------------
# FUNCIÓN: Buscar respuesta en base de datos
# ---------------------------------------------------------
def buscar_respuesta_json(pregunta, base_datos):
    palabras_pregunta = set(pregunta.lower().split())
    mejor_coincidencia = 0
    mejor_item = None

    for item in base_datos.get("preguntas", []):
        palabras_clave = set(item.get("pregunta", "").lower().split())
        coincidencias = len(palabras_clave.intersection(palabras_pregunta))
        if coincidencias > mejor_coincidencia:
            mejor_coincidencia = coincidencias
            mejor_item = item

    if mejor_item and mejor_coincidencia >= 2:
        respuesta = mejor_item.get("respuesta", "Respuesta no disponible")
        url = mejor_item.get("url", "No disponible")
        return f"{respuesta}\nMás información: {url}"

    return "Lo siento, no tengo una respuesta para esa pregunta."

# ---------------------------------------------------------
# FUNCIÓN: Obtener respuesta (cuando el usuario pulsa botón)
# ---------------------------------------------------------
def obtener_respuesta():
    pregunta = entrada_usuario.get()
    if pregunta.strip() == "":
        return
    respuesta = buscar_respuesta_json(pregunta, base_datos)
    historial_texto.insert(
        tk.END,
        f"Tú: {pregunta}\nChatbot: {respuesta}\n\n"
    )
    entrada_usuario.delete(0, tk.END)

# CARGA INICIAL DE DATOS
base_datos = cargar_base_datos()

# ---------------------------------------------------------
# INTERFAZ GRÁFICA (Tkinter)
# ---------------------------------------------------------
root = tk.Tk()
root.title("Chatbot con Tkinter y Base de Datos")

# ÁREA DE TEXTO (historial del chat)
historial_texto = scrolledtext.ScrolledText(
    root, width=50, height=20, wrap=tk.WORD
)
historial_texto.pack(pady=10)

# CAMPO DE ENTRADA DEL USUARIO
entrada_usuario = tk.Entry(root, width=50)
entrada_usuario.pack(pady=5)

# BOTÓN ENVIAR
boton_enviar = tk.Button(
    root, text="Enviar", command=obtener_respuesta
)
boton_enviar.pack(pady=5)

# BUCLE PRINCIPAL
root.mainloop()
