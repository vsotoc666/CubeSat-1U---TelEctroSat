import serial
import time
import pynmea2
import smbus2
import bme280

# Configuración del GPS
SERIAL_PORT = '/dev/ttyUSB0'  # Ajusta esto según tu configuración de puerto
BAUD_RATE = 9600

# Configuración del BME280
I2C_PORT = 1
BME_ADDRESS = 0x76  # Dirección I2C del BME280

# Inicializar GPS
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

# Inicializar sensor BME280
bus = smbus2.SMBus(I2C_PORT)
calibration_params = bme280.load_calibration_params(bus, BME_ADDRESS)

def leer_datos_bme():
    """Lee los datos del BME280: temperatura, presión, y humedad"""
    try:
        data = bme280.sample(bus, BME_ADDRESS, calibration_params)
        return data.temperature, data.pressure, data.humidity
    except Exception as e:
        print(f"Error al leer BME280: {e}")
        return None

def obtener_datos_gps():
    """Lee los datos del GPS, incluyendo latitud, longitud y altitud"""
    while True:
        try:
            # Leer una línea completa del GPS
            line = ser.readline().decode('ascii', errors='ignore').strip()
            if line.startswith('$GPGGA'):
                msg = pynmea2.parse(line)
                lat = msg.latitude
                lon = msg.longitude
                alt = msg.altitude
                return lat, lon, alt
        except pynmea2.ParseError:
            continue

def calcular_altitud_corregida(altitud_gps, presion_atm):
    """Calcula la altitud corregida usando la fórmula barométrica"""
    # Constantes
    PRESION_REF = 1013.25  # Presión a nivel del mar en hPa
    ALTITUD_REF = 0  # Altitud a nivel del mar en metros

    # La fórmula barométrica para ajustar la altitud:
    altitud_corregida = altitud_gps + (PRESION_REF - presion_atm) / 10
    return round(altitud_corregida, 2)

def main():
    while True:
        # Obtener datos del BME280
        temperatura, presion, humedad = leer_datos_bme()

        if temperatura is not None:
            print(f"Temperatura: {temperatura} °C")
            print(f"Presión: {presion} hPa")
            print(f"Humedad: {humedad} %")

        # Obtener datos del GPS
        lat, lon, alt_gps = obtener_datos_gps()
        print(f"Latitud: {lat}, Longitud: {lon}, Altitud GPS: {alt_gps} m")

        # Calcular la altitud corregida
        altitud_corregida = calcular_altitud_corregida(alt_gps, presion)
        print(f"Altitud Corregida: {altitud_corregida} m")
        print("-" * 30)

        time.sleep(1)

if __name__ == "__main__":
    main()
