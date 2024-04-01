import zmq
import json

class SistemaCalidadEdge:
    def __init__(self, bind_address):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PULL)
        self.socket.bind(bind_address)

    def iniciar(self):
        print("Sistema de Calidad en Edge iniciado y esperando reportes de fallos...")
        while True:
            mensaje_json = self.socket.recv_string()
            mensaje = json.loads(mensaje_json)
            # Suponiendo que el mensaje contiene un campo 'mensaje' que describe el fallo
            print(f"ALERTA DE FALLO: {mensaje['mensaje']} en el sensor {mensaje['id_sensor']}")

def main():
    # Asumiendo que usamos el puerto 5558 para el sistema de calidad en Edge
    BIND_ADDRESS = "tcp://*:5558"
    sistema_calidad_edge = SistemaCalidadEdge(BIND_ADDRESS)
    sistema_calidad_edge.iniciar()

if __name__ == "__main__":
    main()