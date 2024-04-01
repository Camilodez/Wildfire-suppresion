# sensor_de_humedad.py

from sensor import Sensor
import random

class SensorDeHumedad(Sensor):
    def generar_valor_correcto(self):
        return random.uniform(70, 100)

    def generar_valor_fuera_de_rango(self):
        return random.uniform(0, 69.9)

    def generar_valor_erroneo(self):
        return -1
