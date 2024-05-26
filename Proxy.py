import zmq
import json
import time
from threading import Thread

def cargar_configuracion():
    with open('config.json', 'r') as f:
        return json.load(f)

config = cargar_configuracion()
context = zmq.Context()

# Socket para recibir datos de sensores
sensor_socket = context.socket(zmq.PULL)
sensor_socket.bind(f"tcp://*:{config['proxy_port']}")

# Socket para enviar datos a Cloud
cloud_socket = context.socket(zmq.PUSH)
cloud_socket.connect(f"tcp://{config['cloud_ip']}:{config['cloud_port']}")

# Socket para enviar heartbeats al sistema de calidad edge
heartbeat_socket = context.socket(zmq.PUSH)
heartbeat_socket.connect(f"tcp://{config['sistema_calidad_edge_ip']}:{config['sistema_calidad_edge_port']}")

def enviar_heartbeat():
    while True:
        heartbeat_socket.send_json({"heartbeat": 1})
        print("Enviado heartbeat al Sistema de Calidad Edge")
        time.sleep(10)

def recibir_datos():
    while True:
        try:
            message = sensor_socket.recv_json(flags=zmq.NOBLOCK)
            print(f"Recibido en Proxy Principal: {message}")
            cloud_socket.send_json(message)
        except zmq.Again:
            pass
        time.sleep(1)

if __name__ == "__main__":
    Thread(target=enviar_heartbeat).start()
    recibir_datos()
