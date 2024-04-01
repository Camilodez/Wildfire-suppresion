# sensor_de_temperatura.py

from Sensor import Sensor
import random

class SensorDeTemperatura(Sensor):
    def generar_valor_correcto(self):
        return random.uniform(11, 29.4)

    def generar_valor_fuera_de_rango(self):
        if random.random() < 0.5:
            return random.uniform(-10, 10.9)
        else:
            return random.uniform(29.5, 50)

    def generar_valor_erroneo(self):
        return -1
