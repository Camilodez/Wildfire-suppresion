import random
from Sensor import Sensor, iniciar_sensor

class SensorHumedad(Sensor):
    def __init__(self, tipo, config_file):
        super().__init__(tipo, config_file)

    def valor_correcto(self):
        return round(random.uniform(70, 100), 2)

    def valor_fuera_de_rango(self):
        return round(random.uniform(0, 69), 2)

    def valor_error(self):
        return round(random.uniform(-10, 10), 2)

if __name__ == "__main__":
    iniciar_sensor(SensorHumedad, 5, 'humedad')
