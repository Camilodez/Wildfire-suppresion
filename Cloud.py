import zmq
import json
import time
from datetime import datetime

def cargar_configuracion():
    with open('config.json', 'r') as f:
        return json.load(f)

config = cargar_configuracion()

context = zmq.Context()

# Socket para recibir datos del Proxy
socket = context.socket(zmq.PULL)
socket.bind(f"tcp://*:{config['cloud_port']}")

# Socket para enviar alertas al Sistema de Calidad Cloud
alert_socket = context.socket(zmq.REQ)
alert_socket.connect(f"tcp://{config['sistema_calidad_cloud_ip']}:{config['sistema_calidad_cloud_port']}")

humedad_mensual = []

def calcular_humedad_media_mensual():
    if len(humedad_mensual) > 0:
        humedad_media = sum(humedad_mensual) / len(humedad_mensual)
        humedad_mensual.clear()
        return humedad_media
    return None

def almacenar_datos(data):
    with open("cloud_data.txt", "a") as file:
        file.write(f"{data}\n")

while True:
    try:
        message = socket.recv_json(flags=zmq.NOBLOCK)
        print(f"Recibido en Cloud: {message}")
        tipo = message.get("tipo")
        valor = message.get("valor")
        timestamp = message.get("timestamp")
        
        if tipo == "humedad":
            humedad_mensual.append(valor)
            if len(humedad_mensual) % 4 == 0:  # Cada 20 segundos (4 medidas diarias)
                humedad_media_mensual = calcular_humedad_media_mensual()
                if humedad_media_mensual is not None:
                    almacenar_datos({
                        "timestamp": datetime.fromtimestamp(timestamp).isoformat(),
                        "humedad_media_mensual": humedad_media_mensual
                    })
                    if humedad_media_mensual < 70:  # Límite inferior de humedad
                        alert_socket.send_string("Alerta: Humedad mensual baja")
                        alert_socket.recv_string()
        else:
            almacenar_datos(message)

    except zmq.Again:
        pass

    time.sleep(1)
