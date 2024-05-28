import zmq
import json
import time
from threading import Thread

def cargar_configuracion():
    with open('config.json', 'r') as f:
        return json.load(f)

config = cargar_configuracion()
context = zmq.Context()

# Socket para recibir estado del SistemaCalidadFog
status_socket = context.socket(zmq.PULL)
status_socket.bind(f"tcp://*:{config['sistema_calidad_edge_port']}")

# Socket para enviar datos al Proxy
data_socket = context.socket(zmq.PUSH)
data_socket.connect(f"tcp://{config['proxy_ip']}:{config['proxy_port']}")

# Socket para enviar datos al Proxy de Emergencia
emergency_data_socket = context.socket(zmq.PUSH)
emergency_data_socket.connect(f"tcp://{config['proxy_emergencia_ip']}:{config['proxy_emergencia_port']}")

proxy_estado = "principal"

def recibir_estado():
    global proxy_estado
    while True:
        try:
            message = status_socket.recv_json(flags=zmq.NOBLOCK)
            if message.get("estado") == "emergencia":
                proxy_estado = "emergencia"
                print("Cambiando a proxy de emergencia")
            elif message.get("estado") == "principal":
                proxy_estado = "principal"
                print("Cambiando a proxy principal")
        except zmq.Again:
            pass
        time.sleep(1)

def enviar_datos(data):
    global proxy_estado
    if proxy_estado == "principal":
        data_socket.send_json(data)
    else:
        emergency_data_socket.send_json(data)

if __name__ == "__main__":
    Thread(target=recibir_estado).start()
    while True:
        # Simulación de datos de sensores
        data = {"tipo": "humo", "valor": True, "timestamp": time.time()}
        enviar_datos(data)
        time.sleep(3)
