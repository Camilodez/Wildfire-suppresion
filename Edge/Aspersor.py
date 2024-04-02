import zmq

class ActuadorAspersor:
    def __init__(self, subscribe_address):
        self.context = zmq.Context()
        # Cambiar de PULL a SUB
        self.socket = self.context.socket(zmq.SUB)
        # Conectar al publicador, no usar bind en el modelo SUB
        self.socket.connect(subscribe_address)
        # Suscribirse a un tema específico, en este caso "Humo detectado" o similar
        self.socket.setsockopt_string(zmq.SUBSCRIBE, 'Humo')
        self.activado = False

    def escuchar_sensores(self):
        print("Actuador Aspersor esperando señales de los sensores de humo...")
        while True:
            # Recibir mensajes; ahora filtrados por el tema de suscripción
            topic, mensaje = self.socket.recv_multipart()
            print(f"Señal recibida: {mensaje.decode('utf-8')}. Activando aspersor...")
            self.activar_aspersor(mensaje.decode('utf-8'))

    def activar_aspersor(self, mensaje):
        # Procesamiento basado en el mensaje recibido, activa el aspersor si es necesario
        self.activado = True
        print("Aspersor activado.")

def main():
    SUBSCRIBE_ADDRESS = "tcp://*:5556"  
    actuador = ActuadorAspersor(SUBSCRIBE_ADDRESS)
    actuador.escuchar_sensores()

if __name__ == "__main__":
    main()
