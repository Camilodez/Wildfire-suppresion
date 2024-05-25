import zmq
import json

def cargar_configuracion():
    with open('config.json', 'r') as f:
        return json.load(f)

def activar_aspersor():
    print("Aspersor activado!")

config = cargar_configuracion()
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind(f"tcp://{config['aspersor_ip']}:{config['aspersor_port']}")

while True:
    message = socket.recv_string()
    if message == "humo_detectado":
        activar_aspersor()
    socket.send_string("ack")
