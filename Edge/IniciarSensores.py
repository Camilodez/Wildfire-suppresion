
from SensorTemperatura import SensorDeTemperatura
from SensorHumedad import SensorDeHumedad  
from SensorHumo import SensorDeHumo  

def iniciar_sensores(fog_address, calidad_edge_address, config_path):
    sensores = []

  
    for i in range(10):
        sensor = SensorDeTemperatura(i, fog_address, "Temperatura", config_path, 6)
        sensor.start()
        sensores.append(sensor)

    # Iniciar sensores de humedad
    for i in range(10, 20):
        sensor = SensorDeHumedad(i, fog_address, "Humedad", config_path, 5)
        sensor.start()
        sensores.append(sensor)

    # Iniciar sensores de humo
    for i in range(20, 30):
        sensor = SensorDeHumo(i, fog_address, calidad_edge_address, "Humo", config_path, 3)
        sensor.start()
        sensores.append(sensor)

    for sensor in sensores:
        sensor.join()

if __name__ == "__main__":
    FOG_ADDRESS = "tcp://10.43.100.47:5555"
    CALIDAD_EDGE_ADDRESS = "tcp://localhost:5558"  
    CONFIG_PATH = "config.json"
    iniciar_sensores(FOG_ADDRESS, CALIDAD_EDGE_ADDRESS, CONFIG_PATH)
