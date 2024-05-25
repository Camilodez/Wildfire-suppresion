import zmq
import json
import time

def cargar_configuracion():
    with open('config.json', 'r') as f:
        return json.load(f)

config = cargar_configuracion()
context = zmq.Context()

def recibir_datos():
    socket = context.socket(zmq.PULL)
    socket.bind(f"tcp://{config['proxy_ip']}:{config['proxy_port']}")

    while True:
        try:
            message = socket.recv_json(flags=zmq.NOBLOCK)
            print(f"Recibido: {message}")
            # Aquí se procesarían y reenviarían los datos a la nube
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
