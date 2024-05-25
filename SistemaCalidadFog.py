import zmq
import json

def cargar_configuracion():
    with open('config.json', 'r') as f:
        return json.load(f)

config = cargar_configuracion()
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind(f"tcp://{config['sistema_calidad_cloud_ip']}:{config['sistema_calidad_cloud_port']}")

while True:
    message = socket.recv_string()
    print(f"Alerta recibida: {message}")
    socket.send_string("ack")
