import zmq
import json
import time

def cargar_configuracion():
    with open('config.json', 'r') as f:
        return json.load(f)

config = cargar_configuracion()
context = zmq.Context()

# Socket para recibir datos de sensores
socket = context.socket(zmq.PULL)
socket.bind(f"tcp://*:{config['proxy_emergencia_port']}")

# Socket para enviar datos a Cloud
cloud_socket = context.socket(zmq.PUSH)
cloud_socket.connect(f"tcp://{config['cloud_ip']}:{config['cloud_port']}")

def recibir_datos():
    while True:
        try:
            message = socket.recv_json(flags=zmq.NOBLOCK)
            print(f"Recibido en Proxy de Emergencia: {message}")
            cloud_socket.send_json(message)
        except zmq.Again:
            pass
        time.sleep(1)

if __name__ == "__main__":
    recibir_datos()
