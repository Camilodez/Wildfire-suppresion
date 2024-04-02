import zmq
import threading
import random
import time
import json

class Sensor(threading.Thread):
    def __init__(self, id_sensor, fog_address, tipo, config_path, intervalo):
        super().__init__()
        self.id_sensor = id_sensor
        self.fog_address = fog_address
        self.tipo = tipo
        self.intervalo = intervalo
        self.config = self.cargar_configuracion(config_path)
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)  # Usando PUB para publicar mensajes
        self.socket.connect(fog_address)

    def cargar_configuracion(self, config_path):
        with open(config_path, 'r') as file:
            return json.load(file)

    def run(self):
        while True:
            valor = self.generar_muestra()
            self.enviar_muestra(valor)
            time.sleep(self.intervalo)

    def generar_muestra(self):
        rnd = random.random()
        if rnd < self.config['correcto']:
            return self.generar_valor_correcto()
        elif rnd < self.config['correcto'] + self.config['fuera_de_rango']:
            return self.generar_valor_fuera_de_rango()
        else:
            return self.generar_valor_erroneo()

    def enviar_muestra(self, valor):
        mensaje = json.dumps({
            'id_sensor': self.id_sensor,
            'tipo': self.tipo,
            'valor': valor,
            'timestamp': time.time()
        })
        self.socket.send_string(f"{self.tipo} {mensaje}")
        print(f"Sensor {self.id_sensor} de {self.tipo} envió: {mensaje}")

    def generar_valor_correcto(self):
        raise NotImplementedError

    def generar_valor_fuera_de_rango(self):
        raise NotImplementedError

    def generar_valor_erroneo(self):
        raise NotImplementedError
