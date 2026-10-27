"""
TelEctroSat - Programa principal de vuelo (Raspberry Pi Zero 2 W)

Lee BME280, GUVA-S12SD (via ADS1115), MPU9250 y GPS NEO-6M, empaqueta las
lecturas como CSV y las transmite por LoRa (SX1278, 433 MHz) a la estacion
terrena cada ~0.25 s. Cuando la altitud GPS baja de 100 m se acciona el rele
del sistema de despliegue del paracaidas.

Ejecutar desde esta carpeta:  python3 main_vuelo.py
"""
import time
from LoRaRF import SX127x
from sensores.sensor_bme280 import BME280Sensor
from sensores.sensor_uv_guva import GUVA_Sensor
from sensores.sensor_imu_mpu9250 import MPU9250Sensor  
from sensores.sensor_gps import leer_datos_gps  # Se asume que retorna (lat, lon, alt)
from sensores.actuador_rele import RelayController
LoRa = SX127x()

print("Inicializando LoRa...")
if not LoRa.begin():
    raise Exception("No se pudo iniciar el LoRa")
print("LoRa iniciado correctamente")

LoRa.setFrequency(433000000)  
LoRa.setTxPower(18, LoRa.TX_POWER_PA_BOOST)  
LoRa.setSpreadingFactor(7)  
LoRa.setBandwidth(250000)  
LoRa.setCodeRate(5)  
LoRa.setHeaderType(LoRa.HEADER_EXPLICIT)  
LoRa.setPreambleLength(8)  
LoRa.setCrcEnable(True)  
LoRa.setSyncWord(0x34)  

print("\n-- Transmisor LoRa --\n")

sensor_bme = BME280Sensor()
sensor_guva = GUVA_Sensor()
sensor_mpu = MPU9250Sensor()

def obtener_datos():
    datos_bme = sensor_bme.leer_datos()
    datos_guva = sensor_guva.leer_datos()
    datos_mpu = sensor_mpu.leer_datos()
    lat, lon, alt = leer_datos_gps()  # Se obtienen los datos del GPS
    
    if datos_bme and datos_guva and datos_mpu:
        datos = {
            "temperatura": datos_bme['temperatura'],
            "presion": datos_bme['presion'],
            "humedad": datos_bme['humedad'],
            "voltaje": datos_guva['voltaje'],
            "indice_uv": datos_guva['indice_uv'],
            "acelerometro_x": datos_mpu['acelerometro_x'],
            "acelerometro_y": datos_mpu['acelerometro_y'],
            "acelerometro_z": datos_mpu['acelerometro_z'],
            "giroscopio_x": datos_mpu['giroscopio_x'],
            "giroscopio_y": datos_mpu['giroscopio_y'],
            "giroscopio_z": datos_mpu['giroscopio_z'],
            "latitud": lat,
            "longitud": lon,
            "altitud": alt
        }
        return datos
    else:
        return None

primeravez80 = False
rele_activado = False
contador = 0

while True:
    datos = obtener_datos()

    if datos:
        # Construir el mensaje a partir de los valores obtenidos
        mensaje = ",".join(map(str, datos.values()))
        # Convertir la cadena codificada en una lista de enteros
        data_to_send = list(mensaje.encode('utf-8'))
        
        LoRa.beginPacket()
        LoRa.write(data_to_send)  
        LoRa.endPacket()
        lat, lon, alt = leer_datos_gps()
        if rele_activado == False and alt <= 100:
            rele_activado = True
            relay_controller = RelayController()
            

        print(f"Mensaje enviado: {mensaje}")
        LoRa.wait()

        print(f"Tiempo de transmisión: {LoRa.transmitTime():.2f} ms | Tasa de datos: {LoRa.dataRate():.2f} byte/s")
        
        contador += 1
        time.sleep(0.25)
