# sensor_de_humo.py

from Sensor import Sensor
import random
import json
import zmq

class SensorDeHumo(Sensor):
    def __init__(self, id_sensor, fog_address, calidad_edge_address, tipo, config_path, intervalo):
        super().__init__(id_sensor, fog_address, tipo, config_path, intervalo)
        # Configurar conexión al sistema de calidad en Edge
        self.calidad_edge_address = calidad_edge_address
        self.calidad_socket = self.context.socket(zmq.PUSH)
        self.calidad_socket.connect(calidad_edge_address)

    def generar_valor_correcto(self):
        # Humo no detectado
        return False

    def generar_valor_fuera_de_rango(self):
        # Humo detectado
        valor = True
        self.reportar_fallo()
        return valor

    def generar_valor_erroneo(self):
        # Simula un valor de error
        return None

    def reportar_fallo(self):
        mensaje = json.dumps({
            'id_sensor': self.id_sensor,
            'tipo': self.tipo,
            'mensaje': 'Humo detectado'
        })
        self.calidad_socket.send_string(mensaje)
        print(f"Sensor de Humo {self.id_sensor} reportó humo detectado al sistema de calidad en Edge.")
