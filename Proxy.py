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
socket.bind(f"tcp://{config['proxy_ip']}:{config['proxy_port']}")

# Socket para enviar datos a Cloud
cloud_socket = context.socket(zmq.PUSH)
cloud_socket.connect(f"tcp://{config['cloud_ip']}:{config['cloud_port']}")

# Socket para responder a las verificaciones de salud
health_socket = context.socket(zmq.REP)
health_socket.bind(f"tcp://{config['proxy_ip']}:{config['proxy_port'] + 1}")

def recibir_datos():
    while True:
        try:
            message = socket.recv_json(flags=zmq.NOBLOCK)
            print(f"Recibido: {message}")
            cloud_socket.send_json(message)
        except zmq.Again:
            pass

        try:
            health_message = health_socket.recv_string(flags=zmq.NOBLOCK)
            if health_message == "health_check":
                health_socket.send_string("ok")
        except zmq.Again:
            pass

        time.sleep(1)

def health_check():
    # Simulación de un chequeo de salud del proxy
    return True

if __name__ == "__main__":
    while health_check():
        recibir_datos()
    print("El proxy principal ha fallado, iniciando proxy de respaldo...")
    # Aquí se debería iniciar el proxy de respaldo
