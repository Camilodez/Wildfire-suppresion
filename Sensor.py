# sensor.py
import socket
import time
import random
import json

def generate_sensor_data():
    return {
        'temperature': round(random.uniform(11, 29.4), 2),
        'humidity': random.randint(70, 100),
        'smoke': random.choice([True, False])
    }

def main():
    host = 'localhost'
    port = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        while True:
            data = generate_sensor_data()
            message = json.dumps(data)
            s.sendall(message.encode('utf-8'))
            time.sleep(random.randint(1, 3))  # Simulate sensor data capture interval

if __name__ == '__main__':
    main()
