import zmq

class SistemaCalidadFog:
    def __init__(self, bind_address):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PULL)
        self.socket.bind(bind_address)

    def iniciar(self):
        print("Sistema de Calidad de Fog iniciado y esperando alertas...")
        while True:
            alerta = self.socket.recv_string()
            print(f"ALERTA: {alerta}")

def main():
    BIND_ADDRESS = "tcp://*:5556"  # Asegúrate de que este puerto esté libre y disponible
    sistema_calidad_fog = SistemaCalidadFog(BIND_ADDRESS)
    sistema_calidad_fog.iniciar()

if __name__ == "__main__":
    main()
