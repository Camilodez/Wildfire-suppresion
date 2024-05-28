import zmq
import json
import time
from threading import Thread

def cargar_configuracion():
    with open('config.json', 'r') as f:
        return json.load(f)

config = cargar_configuracion()
context = zmq.Context()

# Socket para recibir heartbeats del Proxy
heartbeat_socket = context.socket(zmq.PULL)
heartbeat_socket.bind(f"tcp://*:{config['sistema_calidad_fog_port']}")

# Socket para notificar al SistemaCalidadEdge
status_socket = context.socket(zmq.PUSH)
status_socket.connect(f"tcp://{config['sistema_calidad_edge_ip']}:{config['sistema_calidad_edge_port']}")

last_heartbeat_time = time.time()
heartbeat_timeout = 15  # segundos

def recibir_heartbeat():
    global last_heartbeat_time
    while True:
        try:
            message = heartbeat_socket.recv_json(flags=zmq.NOBLOCK)
            if message.get("heartbeat") == 1:
                last_heartbeat_time = time.time()
                print("Recibido heartbeat del Proxy Principal")
        except zmq.Again:
            pass
        time.sleep(1)

def verificar_heartbeat():
    while True:
        if time.time() - last_heartbeat_time > heartbeat_timeout:
            print("No se recibió el heartbeat del Proxy Principal, cambiando a proxy de emergencia")
            status_socket.send_json({"estado": "emergencia"})
        else:
            status_socket.send_json({"estado": "principal"})
        time.sleep(1)

if __name__ == "__main__":
    Thread(target=recibir_heartbeat).start()
    verificar_heartbeat()
