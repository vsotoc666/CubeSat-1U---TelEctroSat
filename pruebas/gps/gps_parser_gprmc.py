import serial
import time

# Configura el puerto serial donde está conectado el GPS
port = "/dev/serial0"  # Ajusta el puerto si es necesario
baudrate = 9600         # Configuración común para muchos módulos GPS

# Abre la conexión serial con el GPS
gps = serial.Serial(port, baudrate, timeout=1)

def parse_nmea(nmea_string):
    # Busca los datos GPRMC que contienen la información importante
    if nmea_string.startswith('$GPRMC'):
        parts = nmea_string.split(',')
        if parts[2] == 'A':  # 'A' significa "Fix" (fix válido)
            lat = parts[3]
            lat_dir = parts[4]
            lon = parts[5]
            lon_dir = parts[6]
            time = parts[1]
            date = parts[9]

            # Muestra la latitud y longitud con dirección
            print(f"Hora: {time}")
            print(f"Fecha: {date}")
            print(f"Latitud: {lat} {lat_dir}")
            print(f"Longitud: {lon} {lon_dir}")
        else:
            print("Fix no disponible")
    else:
        return

try:
    while True:
        # Lee una línea de datos del GPS
        nmea_data = gps.readline().decode('ascii', errors='replace')
        if nmea_data:
            parse_nmea(nmea_data)
        time.sleep(0.009)

except KeyboardInterrupt:
    print("Interrumpido por el usuario")
    gps.close()

