import random
import time
from Sensor import Sensor, iniciar_sensor
import zmq

class SensorHumo(Sensor):
    def __init__(self, tipo, config_file):
        super().__init__(tipo, config_file)
        self.aspersor_socket = self.context.socket(zmq.REQ)
        self.aspersor_socket.connect(f"tcp://{self.config['aspersor_ip']}:{self.config['aspersor_port']}")

    def valor_correcto(self):
        return random.choice([True, False])

    def valor_fuera_de_rango(self):
        return random.choice([True, False])

    def valor_error(self):
        return random.choice([None, "ERROR"])

    def tomar_muestra(self):
        valor = self.generar_valor()
        timestamp = time.time()
        data = {"tipo": self.tipo, "valor": valor, "timestamp": timestamp}
        try:
            self.socket.send_json(data, zmq.NOBLOCK)
            print(f"Enviado al Proxy Principal: {data}")
            if valor:
                self.enviar_aspersor()
        except zmq.Again:
            print(f"Error enviando al Proxy Principal: {data}")
            self.enviar_emergencia(data)
            if valor:
                self.enviar_aspersor()

    def enviar_aspersor(self):
        try:
            self.aspersor_socket.send_string("activar_aspersor")
            self.aspersor_socket.recv_string()
        except zmq.Again:
            print("Error activando el aspersor")

if __name__ == "__main__":
    iniciar_sensor(SensorHumo, 3, 'humo')
