import zmq
import json

class ProxyFog:
    def __init__(self, bind_address):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PULL)
        self.socket.bind(bind_address)

    def iniciar(self):
        print("Proxy de Fog Computing iniciado y esperando datos...")
        while True:
            mensaje = self.socket.recv_string()
            datos = json.loads(mensaje)
            
            # Validar la muestra
            if self.validar_muestra(datos):
                print(f"Dato válido recibido: {datos}")
            else:
                print(f"Error en los datos recibidos: {datos}")

    def validar_muestra(self, datos):
        # Aquí se realiza la validación de los datos
        # Por ejemplo, verifica que el valor no sea erróneo
        if datos['valor'] in [-1, None]:  # Asumiendo que -1 y None representan valores erróneos
            return False
        return True

def main():
    BIND_ADDRESS = "tcp://*:5555"  # El puerto debe coincidir con el configurado en los sensores
    proxy = ProxyFog(BIND_ADDRESS)
    proxy.iniciar()

if __name__ == "__main__":
    main()
