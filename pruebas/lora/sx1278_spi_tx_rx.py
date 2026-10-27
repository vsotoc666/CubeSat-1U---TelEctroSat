import spidev
import RPi.GPIO as GPIO
import time

# ==============================
# Configuración de pines y SPI
# ==============================
RESET_PIN = 17        # Pin GPIO utilizado para resetear el módulo (ajusta según tu conexión)
SPI_BUS = 0
SPI_DEVICE = 0

# ==============================
# Definición de registros SX1278
# (Consulta el datasheet para más detalles)
# ==============================
REG_FIFO             = 0x00
REG_OP_MODE          = 0x01
REG_FRF_MSB          = 0x06
REG_FRF_MID          = 0x07
REG_FRF_LSB          = 0x08
REG_FIFO_ADDR_PTR    = 0x0D
REG_PAYLOAD_LENGTH   = 0x22
REG_IRQ_FLAGS        = 0x12

# Modos de operación (modo LoRa + TX, standby, etc.)
MODE_SLEEP  = 0x80  # LoRa Sleep (bit 7 activado)
MODE_STDBY  = 0x81  # LoRa Standby (modo LoRa + sleep desactivado)
MODE_TX     = 0x83  # LoRa TX

# ==============================
# Funciones para manejar el SX1278
# ==============================

def init_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RESET_PIN, GPIO.OUT)

def reset_module():
    GPIO.output(RESET_PIN, GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(RESET_PIN, GPIO.HIGH)
    time.sleep(0.1)

def write_register(spi, address, value):
    """
    Para el SX1278 se escribe enviando el byte de dirección con el MSB en 1.
    """
    spi.xfer2([address | 0x80, value])

def read_register(spi, address):
    """
    Se lee enviando el byte de dirección con el MSB en 0.
    """
    resp = spi.xfer2([address & 0x7F, 0x00])
    return resp[1]

def set_frequency(spi, frequency):
    """
    Configura la frecuencia de operación.
    La fórmula es: FRF = frequency / Fstep,
    donde Fstep ≈ 61.035 Hz (para un cristal de 32 MHz y 2^19 divisiones).
    """
    frf = int(frequency / 61.035)
    msb = (frf >> 16) & 0xFF
    mid = (frf >> 8) & 0xFF
    lsb = frf & 0xFF
    write_register(spi, REG_FRF_MSB, msb)
    write_register(spi, REG_FRF_MID, mid)
    write_register(spi, REG_FRF_LSB, lsb)

def init_lora(spi):
    """
    Inicializa el módulo en modo LoRa para transmitir.
    Es necesario configurar otros parámetros (como el ancho de banda, factor de propagación, etc.),
    pero aquí se muestra una configuración mínima.
    """
    reset_module()
    # Poner el módulo en modo Sleep para configuración
    write_register(spi, REG_OP_MODE, MODE_SLEEP)
    time.sleep(0.1)
    
    # Configurar en modo LoRa Standby
    write_register(spi, REG_OP_MODE, MODE_STDBY)
    time.sleep(0.1)
    
    # Configurar la frecuencia a 433 MHz
    set_frequency(spi, 433e6)
    
    # Aquí podrías configurar otros registros:
    # - Ancho de banda (RegModemConfig1)
    # - Factor de propagación (RegModemConfig2)
    # - Preámbulo, entre otros.
    # Consulta el datasheet para una configuración óptima.

def send_packet(spi, data):
    """
    Envía un paquete de datos.
    data: lista de enteros (cada uno entre 0 y 255)
    """
    # Establecer el puntero FIFO al inicio (FIFO TX base address)
    write_register(spi, REG_FIFO_ADDR_PTR, 0x00)
    
    # Escribir los datos en el FIFO
    for b in data:
        write_register(spi, REG_FIFO, b)
    
    # Configurar la longitud del payload
    write_register(spi, REG_PAYLOAD_LENGTH, len(data))
    
    # Poner el módulo en modo TX
    write_register(spi, REG_OP_MODE, MODE_TX)
    
    # Esperar a que se complete la transmisión (verificando la bandera TX Done en REG_IRQ_FLAGS)
    while True:
        irq_flags = read_register(spi, REG_IRQ_FLAGS)
        if irq_flags & 0x08:  # Bit TX Done
            break
        time.sleep(0.1)
    # Limpiar las banderas de interrupción
    write_register(spi, REG_IRQ_FLAGS, 0xFF)

# ==============================
# Programa Principal
# ==============================

def main():
    init_gpio()
    spi = spidev.SpiDev()
    spi.open(SPI_BUS, SPI_DEVICE)
    spi.max_speed_hz = 5000000  # Configura la velocidad del SPI
    
    try:
        init_lora(spi)
        while True:
            mensaje = "Hola desde Raspberry Pi"
            print("Enviando:", mensaje)
            # Convertir el mensaje a una lista de bytes
            data = [ord(c) for c in mensaje]
            send_packet(spi, data)
            time.sleep(5)
    except KeyboardInterrupt:
        print("Saliendo...")
    finally:
        spi.close()
        GPIO.cleanup()

if __name__ == '__main__':
    main()
