import zmq

class ActuadorAspersor:
    def __init__(self, bind_address):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PULL)
        self.socket.bind(bind_address)
        self.activado = False

    def escuchar_sensores(self):
        print("Actuador Aspersor esperando señales de los sensores de humo...")
        while True:
            # Espera una señal de activación de algún sensor de humo
            mensaje = self.socket.recv_string()
            self.activar_aspersor(mensaje)

    def activar_aspersor(self, mensaje):
        print(f"Señal recibida: {mensaje}. Activando aspersor...")
        self.activado = True
        # Aquí se incluiría el código para activar el aspersor real

def main():
    ACTUADOR_BIND_ADDRESS = "tcp://*:5556"  # Puerto y dirección para el actuador aspersor
    actuador = ActuadorAspersor(ACTUADOR_BIND_ADDRESS)
    actuador.escuchar_sensores()

if __name__ == "__main__":
    main()
