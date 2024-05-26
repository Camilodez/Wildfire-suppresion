import zmq
import json
import time
import random

class Sensor:
    def __init__(self, tipo, config_file):
        self.tipo = tipo
        self.cargar_configuracion(config_file)
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUSH)
        self.socket.connect(f"tcp://{self.config['proxy_ip']}:{self.config['proxy_port']}")

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
        self.socket.send_json(data)
        print(f"Enviado: {data}")

    def iniciar(self, intervalo):
        while True:
            self.tomar_muestra()
            time.sleep(intervalo)

def iniciar_sensor(sensor_class, intervalo, tipo):
    sensor = sensor_class(tipo, 'config.json')
    sensor.iniciar(intervalo)

if __name__ == "__main__":
    pass
