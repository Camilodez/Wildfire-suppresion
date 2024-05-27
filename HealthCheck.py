import zmq
import json
import time
import subprocess

def cargar_configuracion():
    with open('config.json', 'r') as f:
        return json.load(f)

config = cargar_configuracion()
context = zmq.Context()

# Socket para verificar la salud del proxy principal
health_socket = context.socket(zmq.REQ)
health_socket.connect(f"tcp://{config['proxy_ip']}:{config['proxy_port'] + 1}")

def verificar_salud():
    try:
        health_socket.send_string("health_check")
        health_socket.recv_string(flags=zmq.NOBLOCK)
        return True
    except zmq.Again:
        return False

def iniciar_proxy_emergencia():
    subprocess.Popen(["python", "ProxyEmergencia.py"])

if __name__ == "__main__":
    while True:
        if not verificar_salud():
            print("El proxy principal ha fallado, iniciando proxy de emergencia...")
            iniciar_proxy_emergencia()
            break
        time.sleep(5)
