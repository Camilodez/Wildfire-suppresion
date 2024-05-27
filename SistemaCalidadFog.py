import zmq
import json
import time

def cargar_configuracion():
    with open('config.json', 'r') as f:
        return json.load(f)

config = cargar_configuracion()
context = zmq.Context()

# Socket para recibir alertas del proxy
socket = context.socket(zmq.PULL)
socket.bind(f"tcp://{config['sistema_calidad_fog_ip']}:{config['sistema_calidad_fog_port']}")

def recibir_alertas():
    while True:
        try:
            mensaje = socket.recv_json(flags=zmq.NOBLOCK)
            print(f"Alerta recibida en Sistema de Calidad Fog: {mensaje}")
        except zmq.Again:
            pass
        time.sleep(1)

if __name__ == "__main__":
    recibir_alertas()
