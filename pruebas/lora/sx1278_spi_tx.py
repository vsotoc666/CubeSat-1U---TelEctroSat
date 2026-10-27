import spidev
import time

# Definiciones de registros y modos básicos del SX1278
REG_FIFO = 0x00
REG_OPMODE = 0x01
REG_PAYLOAD_LENGTH = 0x22

MODE_SLEEP = 0x80
MODE_TX = 0x83
MODE_STDBY = 0x81

# Inicialización del bus SPI
spi = spidev.SpiDev()
spi.open(0, 0)            # Bus SPI 0, dispositivo 0
spi.max_speed_hz = 500000   # 500 kHz
spi.mode = 0b00

def write_register(addr, value):
    """Escribe un valor en un registro del SX1278."""
    spi.xfer2([addr | 0x80, value])
    time.sleep(0.005)

def read_register(addr):
    """Lee un registro del SX1278."""
    ret = spi.xfer2([addr & 0x7F, 0x00])
    return ret[1]

def send_message(message):
    """
    Envía un mensaje a través del SX1278.
    Escribe la carga útil en el FIFO, establece la longitud, cambia a modo TX,
    espera un tiempo para la transmisión y regresa a modo standby.
    """
    # Convierte el mensaje a bytes
    payload = list(message.encode('utf-8'))
    payload_length = len(payload)
    
    # Establece la longitud del payload
    write_register(REG_PAYLOAD_LENGTH, payload_length)
    
    # Escribe cada byte en el FIFO
    for byte in payload:
        write_register(REG_FIFO, byte)
    
    # Cambia a modo TX
    write_register(REG_OPMODE, MODE_TX)
    
    # Espera (este delay es aproximado; en un sistema real se debería leer el flag de TX done)
    time.sleep(1)
    
    # Vuelve a modo standby (o a RX, según lo que necesites)
    write_register(REG_OPMODE, MODE_STDBY)

if __name__ == '__main__':
    msg_counter = 1
    try:
        while True:
            # Crea el mensaje con etiqueta de número de mensaje
            message = f"MSG #{msg_counter}: Hola, CubeSat!"
            print("Enviando:", message)
            send_message(message)
            msg_counter += 1
            # Espera 5 segundos entre mensajes
            time.sleep(5)
    except KeyboardInterrupt:
        print("Terminando transmisión...")
    finally:
        spi.close()
