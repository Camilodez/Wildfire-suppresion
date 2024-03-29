# proxy.py
import socket
import threading
import json

def handle_sensor_data(conn, addr):
    print(f"Connected to {addr}")
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            sensor_data = json.loads(data.decode('utf-8'))
            print(f"Received {sensor_data} from {addr}")

def main():
    host = ''
    port = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Proxy listening on port {port}")
        
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_sensor_data, args=(conn, addr))
            thread.start()

if __name__ == '__main__':
    main()
