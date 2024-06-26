import random
from Sensor import Sensor, iniciar_sensor

class SensorTemperatura(Sensor):
    def __init__(self, tipo, config_file):
        super().__init__(tipo, config_file)

    def valor_correcto(self):
        return round(random.uniform(11, 29.4), 2)

    def valor_fuera_de_rango(self):
        return round(random.uniform(30, 50), 2)

    def valor_error(self):
        return round(random.uniform(-10, 10), 2)

if __name__ == "__main__":
    iniciar_sensor(SensorTemperatura, 6, 'temperatura')
