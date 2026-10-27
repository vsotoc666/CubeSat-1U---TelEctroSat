import serial

SERIAL_PORT = '/dev/ttyUSB0'  # Ajusta según tu configuración
BAUD_RATE = 9600

# Inicializar el puerto serial del GPS
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

def obtener_altitud():
    """
    Lee la línea NMEA $GPGGA y extrae la altitud.
    Se evita el uso de la librería pynmea2 realizando un parseo simple.
    """
    while True:
        try:
            line = ser.readline().decode('ascii', errors='ignore').strip()
            if line.startswith('$GPGGA'):
                campos = line.split(',')
                # Verificar que existan suficientes campos y que el campo de altitud no esté vacío
                if len(campos) > 9 and campos[9] != '':
                    altitud = float(campos[9])
                    return altitud
        except Exception as e:
            print("Error leyendo GPS:", e)
            continue
