# sensor_de_humo.py

from Sensor import Sensor
import random

class SensorDeHumo(Sensor):
    def generar_valor_correcto(self):
        return False

    def generar_valor_fuera_de_rango(self):
        return True

    def generar_valor_erroneo(self):
        return None
