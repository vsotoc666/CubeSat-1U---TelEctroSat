import serial
import time

def parse_nmea(sentence):
    """Extraer latitud, longitud y hora de una sentencia GPGGA."""
    parts = sentence.split(",")
    
    if parts[0] == "$GPGGA" or parts[0] == "$GNGGA":
        try:
            time_utc = parts[1]
            latitude = parts[2]
            lat_dir = parts[3]
            longitude = parts[4]
            lon_dir = parts[5]
            sat_count = parts[7]
            altitude = parts[9]
            alt_units = parts[10]

            # Formatear los datos
            formatted_time = f"{time_utc[:2]}:{time_utc[2:4]}:{time_utc[4:6]}"
            formatted_lat = f"{latitude[:2]}° {latitude[2:]} {lat_dir}"
            formatted_lon = f"{longitude[:3]}° {longitude[3:]} {lon_dir}"
            
            # Imprimir los datos
            print(f"Hora UTC: {formatted_time}")
            print(f"Latitud: {formatted_lat}")
            print(f"Longitud: {formatted_lon}")
            print(f"Número de satélites: {sat_count}")
            print(f"Altitud: {altitude} {alt_units}")
            print("=" * 40)

        except IndexError:
            print("Error al analizar la sentencia NMEA.")

def read_gps():
    """Leer datos del GPS desde la Raspberry Pi."""
    try:
        # Configurar la conexión UART
        ser = serial.Serial('/dev/serial0', baudrate=9600, timeout=1)
        
        print("Leyendo datos del GPS...")
        
        while True:
            # Leer una línea completa del GPS
            data = ser.readline().decode('utf-8', errors='ignore').strip()
            
            if data.startswith("$GPGGA") or data.startswith("$GNGGA"):
                parse_nmea(data)
            
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\nLectura GPS detenida.")
    finally:
        ser.close()

if __name__ == "__main__":
    read_gps()
