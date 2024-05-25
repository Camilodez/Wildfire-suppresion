import subprocess

def iniciar_sensores():
    sensores = [
        "SensorHumo.py",
        "SensorTemperatura.py",
        "SensorHumedad.py"
    ]
    for sensor in sensores:
        for i in range(10):
            subprocess.Popen(["python", sensor])

if __name__ == "__main__":
    iniciar_sensores()
