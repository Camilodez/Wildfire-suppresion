from Sensor import Sensor
import random
import json
import zmq

class SensorDeHumo(Sensor):
    def __init__(self, id_sensor, fog_address, calidad_edge_address, tipo, config_path, intervalo):
        super().__init__(id_sensor, fog_address, tipo, config_path, intervalo)
        
        self.calidad_edge_address = calidad_edge_address
        # Cambia de PUSH a PUB para el socket
        self.calidad_socket = self.context.socket(zmq.PUB)
        self.calidad_socket.connect(calidad_edge_address)

    def generar_valor_correcto(self):
        return False

    def generar_valor_fuera_de_rango(self):
        valor = True
        self.reportar_fallo()
        return valor

    def generar_valor_erroneo(self):
        return None

    def reportar_fallo(self):
        mensaje = json.dumps({
            'id_sensor': self.id_sensor,
            'tipo': self.tipo,
            'mensaje': 'Humo detectado'
        })
        # Publicar el mensaje. Podrías agregar un tema aquí si es necesario
        self.calidad_socket.send_string(f"{self.tipo} {mensaje}")
        print(f"Sensor de Humo {self.id_sensor} reportó humo detectado al sistema de calidad en Edge.")
