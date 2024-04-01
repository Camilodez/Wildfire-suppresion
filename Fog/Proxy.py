import zmq
import json
from datetime import datetime

class ProxyFog:
    def __init__(self, pull_bind_address, sistema_calidad_address):
        self.context = zmq.Context()
        # Socket PULL para recibir datos de los sensores
        self.pull_socket = self.context.socket(zmq.PULL)
        self.pull_socket.bind(pull_bind_address)
        # Socket PUSH para enviar alertas al sistema de calidad de Fog
        self.push_socket = self.context.socket(zmq.PUSH)
        self.push_socket.connect(sistema_calidad_address)
        # Para almacenar las últimas temperaturas recibidas de los sensores
        self.temperaturas = []

    def iniciar(self):
        print("Proxy de Fog Computing iniciado y esperando datos...")
        while True:
            mensaje = self.pull_socket.recv_string()
            dato = json.loads(mensaje)

            # Validar la muestra
            if self.validar_muestra(dato):
                print(f"Dato recibido: {dato}")
                if dato['tipo'] == 'Temperatura':
                    self.temperaturas.append(dato['valor'])
                    if len(self.temperaturas) == 10:  # Si hay 10 temperaturas, calcular el promedio
                        promedio = sum(self.temperaturas) / len(self.temperaturas)
                        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        print(f"Promedio de temperatura: {promedio} - Fecha: {fecha}")
                        self.temperaturas.pop(0)  # Eliminar la temperatura más antigua
                        # Comprobar si la temperatura está fuera de rango y enviar alerta
                        if promedio > 29.4:  # Valor máximo según la tabla proporcionada
                            self.enviar_alerta(f"Temperatura promedio alta detectada: {promedio}")
            else:
                print(f"Error en los datos recibidos: {dato}")

    def validar_muestra(self, dato):
        # Asumiendo que los valores erróneos están bien definidos como 'None'
        if dato['valor'] is None:
            return False
        return True

    def enviar_alerta(self, mensaje):
        self.push_socket.send_string(mensaje)

def main():
    PULL_BIND_ADDRESS = "tcp://*:5555"
    SISTEMA_CALIDAD_ADDRESS = "tcp://localhost:5556"  # Cambiar si es necesario
    proxy = ProxyFog(PULL_BIND_ADDRESS, SISTEMA_CALIDAD_ADDRESS)
    proxy.iniciar()

if __name__ == "__main__":
    main()
