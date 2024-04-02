import zmq
import json
from datetime import datetime

class ProxyFog:
    def __init__(self, pull_bind_address, sistema_calidad_address):
        self.context = zmq.Context()
        self.pull_socket = self.context.socket(zmq.PULL)
        self.pull_socket.bind(pull_bind_address)
        self.push_socket_calidad = self.context.socket(zmq.PUSH)
        self.push_socket_calidad.connect(sistema_calidad_address)
        self.temperaturas = []
        self.humedades = []

    def iniciar(self):
        print("Proxy de Fog Computing iniciado y esperando datos...")
        while True:
            mensaje = self.pull_socket.recv_string()
            dato = json.loads(mensaje)
            if self.validar_muestra(dato):
                if dato['tipo'] == 'Temperatura':
                    self.procesar_temperatura(dato)
                elif dato['tipo'] == 'Humedad':
                    self.procesar_humedad(dato)

    def validar_muestra(self, dato):
        if dato['valor'] is None:
            return False
        return True

    def procesar_temperatura(self, dato):
        self.temperaturas.append(dato['valor'])
        if len(self.temperaturas) == 10:  
            promedio_temp = sum(self.temperaturas) / len(self.temperaturas)
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"Promedio de temperatura: {promedio_temp} - Fecha: {fecha}")
            self.temperaturas.pop(0)  
            if promedio_temp > 29.4:  
                self.enviar_alerta_calidad(f"Temperatura promedio alta detectada: {promedio_temp}")



    def procesar_humedad(self, dato):
        self.humedades.append(dato['valor'])
        if len(self.humedades) == 10:  
            promedio_hum = sum(self.humedades) / len(self.humedades)
            if not (70 <= promedio_hum <= 100): 
                self.enviar_alerta_calidad(f"Humedad fuera de rango: {promedio_hum}%")
            self.humedades.pop(0) 

    def enviar_alerta_calidad(self, mensaje):
        self.push_socket_calidad.send_string(json.dumps({
            'alerta': mensaje,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }))

def main():
    PULL_BIND_ADDRESS = "tcp://*:5555"
    SISTEMA_CALIDAD_ADDRESS = "tcp://localhost:5556"  # Cambiar si es necesario
    proxy = ProxyFog(PULL_BIND_ADDRESS, SISTEMA_CALIDAD_ADDRESS)
    proxy.iniciar()

if __name__ == "__main__":
    main()
