import zmq
import json

class SistemaCalidadEdge:
    def __init__(self, subscribe_address):
        self.context = zmq.Context()
        # Cambia de PULL a SUB
        self.socket = self.context.socket(zmq.SUB)
        # Conecta al publicador, no usa bind en el modelo SUB
        self.socket.connect(subscribe_address)
        # Suscríbete a todos los mensajes. Puede ser más específico si es necesario
        self.socket.setsockopt_string(zmq.SUBSCRIBE, '')

    def iniciar(self):
        print("Sistema de Calidad en Edge iniciado y esperando reportes de fallos...")
        while True:
            mensaje_json = self.socket.recv_string()
            mensaje = json.loads(mensaje_json)
            
            print(f"ALERTA DE FALLO: {mensaje['mensaje']} en el sensor {mensaje['id_sensor']}")

def main():
    # Asume que el publicador está en localhost y usa el puerto 5558
    SUBSCRIBE_ADDRESS = "tcp://localhost:5558"
    sistema_calidad_edge = SistemaCalidadEdge(SUBSCRIBE_ADDRESS)
    sistema_calidad_edge.iniciar()

if __name__ == "__main__":
    main()
