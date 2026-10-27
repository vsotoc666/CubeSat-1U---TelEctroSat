import time
import RPi.GPIO as GPIO
from LoRaRF import SX127x
from sensores.sensor_bme280 import BME280Sensor
from sensores.sensor_uv_guva import GUVA_Sensor
from sensores.sensor_imu_mpu9250 import MPU9250Sensor
from sensores.sensor_gps import leer_datos_gps  # Función que retorna lat, lon y altitud
from sensores.actuador_rele import RelayController

# --- Inicialización de LoRa ---
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

# --- Inicialización de sensores ---
sensor_bme = BME280Sensor()
sensor_guva = GUVA_Sensor()
sensor_mpu = MPU9250Sensor()

def obtener_datos():
    """
    Obtiene datos de los sensores BME280, GUVA y MPU9250, 
    y además obtiene la latitud, longitud y altitud del GPS.
    """
    datos_bme = sensor_bme.leer_datos()
    datos_guva = sensor_guva.leer_datos()
    datos_mpu = sensor_mpu.leer_datos()
    lat, lon, alt = leer_datos_gps()
    
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
            "altitud_gps": alt
        }
        return datos
    else:
        return None

# Variables para controlar la activación del relé
primeravez80 = False  # Se pondrá a True cuando se supere 80 m
rele_activado = False  # Para asegurar que el relé se active sólo una vez

# Se instancia el controlador del relé
#relay_controller = RelayController()

try:
    while True:
        datos = obtener_datos()
        if datos:
            # Transmisión de datos vía LoRa
            mensaje = ",".join(map(str, datos.values()))
            LoRa.beginPacket()
            LoRa.write(mensaje.encode('utf-8'))
            LoRa.endPacket()
            print(f"Mensaje enviado: {mensaje}")
            print(f"Tiempo de transmisión: {LoRa.transmitTime():.2f} ms | Tasa de datos: {LoRa.dataRate():.2f} byte/s")
            print(f"GPS -> Latitud: {datos['latitud']}, Longitud: {datos['longitud']}, Altitud: {datos['altitud_gps']} m")
            
            altitud = datos['altitud_gps']
            
            # Si la altitud es mayor o igual a 80 m, se marca que se ha alcanzado esa altura
            if altitud >= 80:
                primeravez80 = True
            
            # Si ya se ha superado 80 m y ahora la altitud cae por debajo de 80 m, se activa el relé
            #if primeravez80 and altitud < 80 and not rele_activado:
                #print("Condición cumplida: Altitud cayó por debajo de 80 m tras haber superado 80 m. Activando relé...")
                #relay_controller.activar_rele()
                #time.sleep(3)
                #rele_activado = True
        else:
            print("No se pudieron obtener datos completos de los sensores.")
        
        time.sleep(0.25)
        
except KeyboardInterrupt:
    print("Interrupción detectada. Saliendo del programa...")

#finally:
    #if not rele_activado:
        #GPIO.cleanup()
