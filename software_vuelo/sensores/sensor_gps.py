import serial
import time

SERIAL_PORT = '/dev/ttyUSB0'  # Ajusta según tu configuración
BAUD_RATE = 9600

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
except Exception as e:
    print("Error al abrir el puerto serial del GPS:", e)
    ser = None

def convertir_a_decimal(valor, direccion):
    """
    Convierte coordenadas en formato NMEA a decimal.
    """
    try:
        if direccion in ['N', 'S']:
            grados = float(valor[:2])
            minutos = float(valor[2:])
        else:  # Para longitudes (3 dígitos en grados)
            grados = float(valor[:3])
            minutos = float(valor[3:])
        dec = grados + minutos / 60.0
        if direccion in ['S', 'W']:
            dec *= -1
        return dec
    except Exception as e:
        print("Error en convertir_a_decimal:", e)
        return 0.0

def leer_datos_gps(timeout=10):
    """
    Lee el puerto serial buscando una línea que comience con '$GPGGA'. 
    Si no se obtiene un dato válido en 'timeout' segundos, retorna (0, 0, 95).
    """
    if ser is None:
        print("Puerto serial del GPS no está disponible.")
        return 0.0, 0.0, 95.0  # Altitud por defecto: 95 metros

    start_time = time.time()
    while True:
        if time.time() - start_time > timeout:
            print("Timeout en la lectura de GPS, retornando valores por defecto")
            return 0.0, 0.0, 95.0  # Altitud por defecto

        try:
            line = ser.readline().decode('ascii', errors='ignore').strip()
            if line.startswith('$GPGGA'):
                campos = line.split(',')
                # Verificar que existan los campos necesarios
                if len(campos) >= 10 and campos[2] and campos[3] and campos[4] and campos[5]:
                    lat = convertir_a_decimal(campos[2], campos[3])
                    lon = convertir_a_decimal(campos[4], campos[5])
                    alt = float(campos[9]) if campos[9] else 95.0  # Si la altitud es vacía, usar 95
                    return lat, lon, alt
        except Exception as e:
            print("Error leyendo datos del GPS:", e)
            continue
