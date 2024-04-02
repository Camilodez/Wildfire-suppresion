import zmq
import json
from datetime import datetime

class ProxyFog:
    def __init__(self, subscribe_address, publish_calidad_address):
         self.context = zmq.Context()
         self.subscribe_socket = self.context.socket(zmq.SUB)
         self.subscribe_socket.bind(subscribe_address)  # El proxy SUBSCRIBE socket se suele configurar con bind
         self.subscribe_socket.setsockopt_string(zmq.SUBSCRIBE, '')  # Suscribir a todos los mensajes
        # Cambiar de PUSH a PUB para las alertas
         self.publish_socket_calidad = self.context.socket(zmq.PUB)
         self.publish_socket_calidad.bind(publish_calidad_address)
         self.temperaturas = []
         self.humedades = []

    def iniciar(self):
        print("Proxy de Fog Computing iniciado y esperando datos...")
        while True:
            topic, mensaje_json = self.subscribe_socket.recv_multipart()
            dato = json.loads(mensaje_json)
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
        # Envía la alerta como un tema con el mensaje
        self.publish_socket_calidad.send_multipart([b'alerta', json.dumps({
            'alerta': mensaje,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }).encode('utf-8')])

def main():
    SUBSCRIBE_ADDRESS  = "tcp://*:5555"
    PUBLISH_CALIDAD_ADDRESS  = "tcp://localhost:5556"  
    proxy = ProxyFog(SUBSCRIBE_ADDRESS , PUBLISH_CALIDAD_ADDRESS)
    proxy.iniciar()

if __name__ == "__main__":
    main()
