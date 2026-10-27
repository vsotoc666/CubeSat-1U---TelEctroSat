import time
from LoRaRF import SX127x
from sensores.sensor_bme280 import BME280Sensor
from sensores.sensor_uv_guva import GUVA_Sensor
from sensores.sensor_imu_mpu9250 import MPU9250Sensor  

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
            "giroscopio_z": datos_mpu['giroscopio_z']
        }
        return datos
    else:
        return None


contador = 0
while True:
    datos = obtener_datos()

    if datos:
        mensaje = f"Temperatura: {datos['temperatura']} C, Presion: {datos['presion']} hPa, Humedad: {datos['humedad']} %, " 
                  f"Voltaje: {datos['voltaje']} V, UV: {datos['indice_uv']}, " 
                  f"Acelerometro: ({datos['acelerometro_x']}, {datos['acelerometro_y']}, {datos['acelerometro_z']}), " 
                  f"Giroscopio: ({datos['giroscopio_x']}, {datos['giroscopio_y']}, {datos['giroscopio_z']})"
	mensaje = datos['temperatura'],{datos['presion']},{datos['humedad']},  f"{datos['voltaje']},{datos['indice_uv']}, " f"({datos['acelerometro_x']}, {datos['acelerometro_y']}, {datos['acelerometro_z']}), " \                  f"({datos['giroscopio_x']}, {datos['giroscopio_y']}, {datos['giroscopio_z']})"
        mensaje=",".join(map(str, datos.values()))
        LoRa.beginPacket()
        LoRa.write(mensaje.encode('utf-8'))  
        LoRa.endPacket()

        print(f"Mensaje enviado: {mensaje}")
        LoRa.wait()

        print(f"Tiempo de transmisión: {LoRa.transmitTime():.2f} ms | Tasa de datos: {LoRa.dataRate():.2f} byte/s")
        
        contador += 1
        time.sleep(0.25)  
