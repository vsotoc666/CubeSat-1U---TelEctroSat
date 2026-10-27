import serial
import time

class GPSSensor:
    def __init__(self, port="/dev/serial0", baudrate=9600, timeout=1):
        self.gps = serial.Serial(port, baudrate, timeout=timeout)
    
    def parse_nmea(self, nmea_string):
        if nmea_string.startswith('$GPRMC'):
            parts = nmea_string.split(',')
            if parts[2] == 'A':  # 'A' significa que el fix es válido
                return {
                    "hora": parts[1],
                    "fecha": parts[9],
                    "latitud": f"{parts[3]} {parts[4]}",
                    "longitud": f"{parts[5]} {parts[6]}",
                }
        return None
    
    def leer_datos(self):
        try:
            nmea_data = self.gps.readline().decode('ascii', errors='replace')
            return self.parse_nmea(nmea_data)
        except Exception as e:
            print(f"Error al leer datos del GPS: {e}")
            return None
    
    def cerrar(self):
        self.gps.close()

if __name__ == "__main__":
    gps_sensor = GPSSensor()
    try:
        while True:
            datos = gps_sensor.leer_datos()
            if datos:
                print(f"Hora: {datos['hora']}")
                print(f"Fecha: {datos['fecha']}")
                print(f"Latitud: {datos['latitud']}")
                print(f"Longitud: {datos['longitud']}")
                print("-" * 30)
            time.sleep(0.009)
    except KeyboardInterrupt:
        print("Interrumpido por el usuario")
        gps_sensor.cerrar()

