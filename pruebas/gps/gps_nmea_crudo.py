import serial
import time

# Configura la conexión serial
port = "/dev/serial0"  # Asegúrate de que sea el correcto
baudrate = 9600

gps = serial.Serial(port, baudrate, timeout=1)

try:
    while True:
        nmea_data = gps.readline().decode('ascii', errors='replace').strip()
        if nmea_data:
            print(nmea_data)  # Muestra la línea NMEA recibida
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nInterrumpido por el usuario")
    gps.close()
