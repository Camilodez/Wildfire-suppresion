### Wildfire-suppresion

Como Compilar y Correr el codigo ?

### Instalaciones Necesarias

1. Python 3.x: Asegúrate de tener Python 3.x instalado en todos los PCs.
2. Bibliotecas Python: Necesitarás instalar las siguientes bibliotecas:
  ```
pip install zmq json matplotlib pandas
  ```
  Con ese comando descargaras la librerias necesarias para que todo funcione correctamente:

### Paso a Paso para Configurar y Ejecutar el Sistema

#### Paso 1: Configuración Inicial

1. *Crea un archivo `config.json`* en cada PC con la siguiente configuración:
      ```
    {
        "correcto": 0.6,
        "fuera_de_rango": 0.3,
        "error": 0.1,
        "proxy_ip": "10.43.100.67",
        "proxy_port": 5558,
        "proxy_emergencia_ip": "10.43.100.67",
        "proxy_emergencia_port": 5565,
        "aspersor_ip": "10.43.100.174",
        "aspersor_port": 5560,
        "sistema_calidad_edge_ip": "10.43.100.174",
        "sistema_calidad_edge_port": 5561,
        "sistema_calidad_fog_ip": "10.43.100.67",
        "sistema_calidad_fog_port": 5562,
        "sistema_calidad_cloud_ip": "10.43.103.83",
        "sistema_calidad_cloud_port": 5563,
        "cloud_ip": "10.43.103.83",
        "cloud_port": 5564
    }
      ```

#### Paso 2: Configuración de Archivos Python

Coloca los siguientes archivos en las ubicaciones correspondientes en cada PC.

1. PC 1 (Sensores y Aspersor)**:
    - `IniciarSensores.py`
    - `Aspersor.py`
    - `SistemaCalidadEdge.py`

2. **PC 2 (Proxy, Proxy de Emergencia y Sistema de Calidad Fog)**:
    - `Proxy.py`
    - `ProxyEmergencia.py`
    - `SistemaCalidadFog.py`

3. **PC 3 (Sistema de Calidad Cloud y Cloud)**:
    - `SistemaCalidadCloud.py`
    - `Cloud.py`

#### Paso 3: Ejecución de los Componentes

1. En el PC 1 (Sensores y Aspersor):
    - Abre una terminal y ejecuta:
        ```
        python IniciarSensores.py
         ```
      ```
        python Aspersor.py
       ```
        ```
         python SistemaCalidadEdge.py
        ```

2. En el PC 2 (Proxy, Proxy de Emergencia y Sistema de Calidad Fog):
    - Abre tres terminales y ejecuta en cada una:
        ```
        python Proxy.py
        ```
        ```
        python ProxyEmergencia.py
        ```
        ```
        python SistemaCalidadFog.py
        ```

3. En el PC 3 (Sistema de Calidad Cloud y Cloud):
    - Abre dos terminales y ejecuta en cada una:
        ```bash
        python SistemaCalidadCloud.py
        ```
        ```bash
        python Cloud.py
        ```

### Verificación del Sistema

1. Verifica que todos los componentes estén en funcionamiento:
    - Asegúrate de que no haya errores en los logs de las terminales.
    - Verifica que las alertas y datos de los sensores están siendo recibidos correctamente en los sistemas de calidad.

2. Prueba el sistema de cambio a Proxy de Emergencia:
    - Detén el proceso del `Proxy.py` en el PC 2 y verifica que el `ProxyEmergencia.py` comience a recibir datos correctamente.
    - Reinicia el `Proxy.py` y verifica que el sistema vuelva a usar el proxy principal.

Con estos pasos, deberías tener todo el sistema configurado y funcionando correctamente, con tolerancia a fallos y una arquitectura distribuida eficiente.
