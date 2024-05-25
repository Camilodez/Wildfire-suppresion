import random
from Sensor import Sensor, iniciar_sensor

class SensorTemperatura(Sensor):
    def valor_correcto(self):
        return round(random.uniform(11, 29.4), 2)

    def valor_fuera_de_rango(self):
        return round(random.uniform(30, 40), 2)

    def valor_error(self):
        return round(random.uniform(-10, 10), 2)

if __name__ == "__main__":
    iniciar_sensor(SensorTemperatura, 6)
