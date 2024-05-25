import random
from Sensor import Sensor, iniciar_sensor

class SensorHumo(Sensor):
    def valor_correcto(self):
        return random.choice([True, False])

    def valor_fuera_de_rango(self):
        return random.choice([True, False])

    def valor_error(self):
        return random.choice([True, False, None])

if __name__ == "__main__":
    iniciar_sensor(SensorHumo, 3)
