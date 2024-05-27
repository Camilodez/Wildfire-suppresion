import subprocess

def iniciar_sensores():
    sensores = [
        ("SensorHumo.py", 3, 'humo'),
        ("SensorTemperatura.py", 6, 'temperatura'),
        ("SensorHumedad.py", 5, 'humedad')
    ]
    for sensor, intervalo, tipo in sensores:
        for i in range(10):
            subprocess.Popen(["python", sensor])

if __name__ == "__main__":
    iniciar_sensores()
    print("Sensores iniciados")
