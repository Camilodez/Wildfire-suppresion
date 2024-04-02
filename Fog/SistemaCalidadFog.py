import zmq

class SistemaCalidadFog:
    def __init__(self, subscribe_address):
        self.context = zmq.Context()
        # Cambiar de PULL a SUB
        self.socket = self.context.socket(zmq.SUB)
        # Conectar al publicador
        self.socket.connect(subscribe_address)
        # Suscribirse a todas las alertas o puedes especificar un tema específico
        self.socket.setsockopt_string(zmq.SUBSCRIBE, '')

    def iniciar(self):
        print("Sistema de Calidad de Fog iniciado y esperando alertas...")
        while True:
            # Recibir y desempaquetar el tema y el mensaje
            topic, alerta = self.socket.recv_multipart()
            print(f"ALERTA: {alerta.decode('utf-8')}")

def main():
    # Asume que el publicador está en la misma máquina y usa el puerto 5556
    SUBSCRIBE_ADDRESS = "tcp://localhost:5556"
    sistema_calidad_fog = SistemaCalidadFog(SUBSCRIBE_ADDRESS)
    sistema_calidad_fog.iniciar()

if __name__ == "__main__":
    main()
