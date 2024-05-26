import zmq
import json

def cargar_configuracion():
    with open('config.json', 'r') as f:
        return json.load(f)

config = cargar_configuracion()
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind(f"tcp://*:{config['aspersor_port']}")

while True:
    message = socket.recv_string()
    if message == "activar_aspersor":
        print("Aspersor activado!")
        socket.send_string("ack")
    else:
        socket.send_string("unknown_command")
