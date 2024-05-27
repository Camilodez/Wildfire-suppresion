import json
import matplotlib.pyplot as plt
import pandas as pd

# Leer los datos del archivo
data_file = 'cloud_data.txt'

# Listas para almacenar los datos
temperatura_data = []
humo_data = []
humedad_data = []
timestamp_data = []

with open(data_file, 'r') as file:
    for line in file:
        try:
            record = json.loads(line.strip().replace("'", '"'))
            if 'tipo' in record:
                if 'timestamp' in record:
                    timestamp_data.append(record['timestamp'])
                if record['tipo'] == 'temperatura':
                    if 'valor' in record and 'timestamp' in record:
                        temperatura_data.append(record)
                elif record['tipo'] == 'humo':
                    if 'valor' in record and 'timestamp' in record:
                        # Convertir valores a booleanos o None explícitamente
                        if record['valor'] is True or record['valor'] == 'True':
                            record['valor'] = True
                        elif record['valor'] is False or record['valor'] == 'False':
                            record['valor'] = False
                        elif record['valor'] == 'ERROR':
                            record['valor'] = 'ERROR'
                        else:
                            record['valor'] = None
                        humo_data.append(record)
            elif 'humedad_media_mensual' in record and 'timestamp' in record:
                humedad_data.append(record)
        except json.JSONDecodeError:
            continue

# Convertir los datos de temperatura a DataFrame
if temperatura_data:
    temperatura_df = pd.DataFrame(temperatura_data)
    # Convertir timestamps
    temperatura_df['timestamp'] = pd.to_datetime(temperatura_df['timestamp'], unit='s')

    # Agrupar cada 20 datos como un mes
    temperatura_df['month_group'] = (temperatura_df.index // 20) + 1
    temperatura_mensual = temperatura_df.groupby('month_group')['valor'].mean().reset_index()
    temperatura_mensual['timestamp'] = pd.date_range(start='2024-01-01', periods=len(temperatura_mensual), freq='M')
    temperatura_mensual.set_index('timestamp', inplace=True)

    print(f"Promedio de Temperatura por Mes:\n{temperatura_mensual}")

    # Calcular promedio de las temperaturas mensuales
    promedio_temperatura_mensual = temperatura_mensual['valor'].mean()
    print(f"Promedio General de Temperatura Mensual: {promedio_temperatura_mensual:.2f}°C")

    # Graficar los datos de temperatura mensual
    plt.figure(figsize=(10, 5))
    temperatura_mensual['valor'].plot(kind='bar', color='orange')
    plt.axhline(promedio_temperatura_mensual, color='r', linestyle='--', label=f'Promedio General: {promedio_temperatura_mensual:.2f}°C')
    plt.xlabel('Mes')
    plt.ylabel('Temperatura Promedio (°C)')
    plt.title('Promedio Mensual de Temperatura')
    plt.legend()
    plt.show()
else:
    print("No se encontraron datos de temperatura.")

# Convertir los datos de humedad a DataFrame
if humedad_data:
    humedad_df = pd.DataFrame(humedad_data)
    # Convertir timestamps
    humedad_df['timestamp'] = pd.to_datetime(humedad_df['timestamp'])
    humedad_df.set_index('timestamp', inplace=True)

    print(f"Valores de Humedad Media Mensual:\n{humedad_df['humedad_media_mensual']}")

    # Calcular promedio de la humedad media mensual
    promedio_humedad_mensual = humedad_df['humedad_media_mensual'].mean()
    print(f"Promedio General de Humedad Media Mensual: {promedio_humedad_mensual:.2f}%")

    # Graficar los valores de humedad media mensual
    plt.figure(figsize=(10, 5))
    humedad_df['humedad_media_mensual'].plot(kind='bar', color='blue')
    plt.axhline(promedio_humedad_mensual, color='r', linestyle='--', label=f'Promedio General: {promedio_humedad_mensual:.2f}%')
    plt.xlabel('Mes')
    plt.ylabel('Humedad Media Mensual (%)')
    plt.title('Valores Mensuales de Humedad Media')
    plt.legend()
    plt.show()
else:
    print("No se encontraron datos de humedad.")

# Calcular el tiempo de respuesta en ms
if timestamp_data:
    timestamp_data = pd.to_datetime(timestamp_data, unit='s')
    tiempo_respuesta = timestamp_data.diff().dropna().total_seconds() * 1000
    tiempo_respuesta = pd.Series(tiempo_respuesta)  # Convertir a Series para usar el método mean()
    promedio_tiempo_respuesta = tiempo_respuesta.mean()
    print(f"Tiempo de respuesta promedio: {promedio_tiempo_respuesta:.2f} ms")

    # Graficar el tiempo de respuesta
    plt.figure(figsize=(10, 5))
    plt.bar(range(len(tiempo_respuesta)), tiempo_respuesta, color='green')
    plt.axhline(promedio_tiempo_respuesta, color='r', linestyle='--', label=f'Promedio: {promedio_tiempo_respuesta:.2f} ms')
    plt.xlabel('Registro')
    plt.ylabel('Tiempo de Respuesta (ms)')
    plt.title('Tiempo de Respuesta entre Registros')
    plt.legend()
    plt.show()
else:
    print("No se encontraron timestamps para calcular el tiempo de respuesta.")
