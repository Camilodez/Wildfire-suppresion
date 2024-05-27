import zmq
import json
import time
import random
from threading import Thread

class Sensor:
    def __init__(self, tipo, config_file):
        self.tipo = tipo
        self.cargar_configuracion(config_file)
        self.context = zmq.Context()
        self.proxy_socket = self.context.socket(zmq.PUSH)
        self.proxy_socket.connect(f"tcp://{self.config['proxy_ip']}:{self.config['proxy_port']}")
        self.emergency_socket = self.context.socket(zmq.PUSH)
        self.emergency_socket.connect(f"tcp://{self.config['proxy_emergencia_ip']}:{self.config['proxy_emergencia_port']}")
        self.status_socket = self.context.socket(zmq.SUB)
        self.status_socket.connect(f"tcp://{self.config['sistema_calidad_edge_ip']}:{self.config['sistema_calidad_edge_port'] + 1}")
        self.status_socket.setsockopt_string(zmq.SUBSCRIBE, "")
        self.use_emergency = False

    def cargar_configuracion(self, config_file):
        with open(config_file, 'r') as f:
            self.config = json.load(f)
            self.prob_correcto = self.config['correcto']
            self.prob_fuera_de_rango = self.config['fuera_de_rango']
            self.prob_error = self.config['error']

    def generar_valor(self):
        r = random.random()
        if r < self.prob_correcto:
            return self.valor_correcto()
        elif r < self.prob_correcto + self.prob_fuera_de_rango:
            return self.valor_fuera_de_rango()
        else:
            return self.valor_error()

    def valor_correcto(self):
        raise NotImplementedError

    def valor_fuera_de_rango(self):
        raise NotImplementedError

    def valor_error(self):
        raise NotImplementedError

    def tomar_muestra(self):
        valor = self.generar_valor()
        timestamp = time.time()
        data = {"tipo": self.tipo, "valor": valor, "timestamp": timestamp}
        try:
            if self.use_emergency:
                self.emergency_socket.send_json(data, zmq.NOBLOCK)
                print(f"Enviado al Proxy de Emergencia: {data}")
            else:
                self.proxy_socket.send_json(data, zmq.NOBLOCK)
                print(f"Enviado al Proxy Principal: {data}")
        except zmq.ZMQError as e:
            print(f"Error enviando datos: {e}")

    def recibir_estado(self):
        while True:
            try:
                message = self.status_socket.recv_string(flags=zmq.NOBLOCK)
                if message == "estado: emergencia":
                    self.use_emergency = True
                else:
                    self.use_emergency = False
            except zmq.Again:
                pass
            time.sleep(1)

    def iniciar(self, intervalo):
        Thread(target=self.recibir_estado).start()
        while True:
            self.tomar_muestra()
            time.sleep(intervalo)

def iniciar_sensor(sensor_class, intervalo, tipo):
    sensor = sensor_class(tipo, 'config.json')
    sensor.iniciar(intervalo)

if __name__ == "__main__":
    pass
