import spidev
import time

# Definición de algunos registros del SX1278
REG_OPMODE = 0x01       # Modo de operación
REG_VERSION = 0x42      # Versión del chip

# Modos de operación (ejemplo)
MODE_SLEEP = 0x80       # Modo sueño
MODE_STDBY = 0x81       # Modo standby
MODE_TX    = 0x83       # Modo transmisión
MODE_RXCONT= 0x85       # Modo recepción continua

# Inicializar SPI
spi = spidev.SpiDev()
spi.open(0, 0)             # Abre el bus SPI 0, dispositivo 0 (ajusta según tu conexión)
spi.max_speed_hz = 500000    # Velocidad del reloj SPI: 500 kHz
spi.mode = 0b00              # Modo SPI (CPOL=0, CPHA=0)

def write_register(addr, value):
    """
    Escribe en un registro del SX1278.
    Se debe enviar la dirección con el bit MSB en 1 (addr | 0x80).
    """
    spi.xfer2([addr | 0x80, value])
    time.sleep(0.01)  # Pequeño retardo para asegurar la estabilidad

def read_register(addr):
    """
    Lee un registro del SX1278.
    Se envía la dirección con el bit MSB en 0 (addr & 0x7F) y se lee el byte de respuesta.
    """
    ret = spi.xfer2([addr & 0x7F, 0x00])
    return ret[1]

def setup_lora():
    """
    Configura el SX1278 para ponerlo en modo Sleep y lee su versión.
    """
    # Poner el SX1278 en modo Sleep
    write_register(REG_OPMODE, MODE_SLEEP)
    time.sleep(0.1)
    
    # Leer el registro de versión
    version = read_register(REG_VERSION)
    print("Versión del SX1278: 0x{:02X}".format(version))
    
    # Aquí podrías agregar más configuraciones (frecuencia, SF, BW, etc.)

if __name__ == '__main__':
    try:
        setup_lora()
        # Aquí iría el resto del código, por ejemplo, un bucle para transmitir o recibir datos.
        while True:
            # Ejemplo: Leer y mostrar periódicamente el registro de versión
            version = read_register(REG_VERSION)
            print("Versión actual: 0x{:02X}".format(version))
            time.sleep(5)
    except KeyboardInterrupt:
        print("Terminando...")
    finally:
        spi.close()
