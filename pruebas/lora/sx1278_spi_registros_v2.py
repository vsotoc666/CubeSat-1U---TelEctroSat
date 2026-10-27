import spidev
import RPi.GPIO as GPIO
import time

# Pines LoRa
LORA_NSS = 8   # Chip Select (CS)
LORA_RST = 25  # Reset
LORA_DIO0 = 7  # Interrupt (No usado aquí)

# Inicializar SPI
spi = spidev.SpiDev()
spi.open(0, 0)  # Bus 0, Dispositivo 0
spi.max_speed_hz = 5000000

# Configurar GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(LORA_NSS, GPIO.OUT)
GPIO.setup(LORA_RST, GPIO.OUT)

def write_register(addr, value):
    GPIO.output(LORA_NSS, 0)  # Seleccionar LoRa
    spi.xfer2([addr | 0x80, value])
    GPIO.output(LORA_NSS, 1)  # Desactivar LoRa

def read_register(addr):
    GPIO.output(LORA_NSS, 0)
    response = spi.xfer2([addr & 0x7F, 0x00])
    GPIO.output(LORA_NSS, 1)
    return response[1]

def setup_lora():
    GPIO.output(LORA_RST, 1)
    time.sleep(0.1)
    GPIO.output(LORA_RST, 0)
    time.sleep(0.1)

    # Verificar el registro de versión del SX1278
    version = read_register(0x42)
    if version != 0x12:
        print("Error: No se detecta el módulo LoRa")
        return False

    # Configurar en modo sleep antes de cambiar ajustes
    write_register(0x01, 0x00)  # Modo Sleep
    time.sleep(0.1)

    # Configuración básica LoRa
    write_register(0x01, 0x80)  # Modo LoRa
    write_register(0x1D, 0x72)  # BW=125kHz, CR=4/5
    write_register(0x1E, 0x74)  # SF=7, CRC activado
    write_register(0x26, 0x04)  # Modo de bajo consumo
    write_register(0x09, 0xFF)  # Potencia máxima

    print("SX1278 Configurado Correctamente")
    return True

def send_message(msg):
    write_register(0x0E, 0x00)  # Dirección de FIFO TX
    write_register(0x0D, 0x00)

    for byte in msg.encode():
        write_register(0x00, byte)

    write_register(0x22, len(msg))  # Longitud del paquete
    write_register(0x01, 0x83)  # Modo transmisión

    while (read_register(0x12) & 0x08) == 0:
        time.sleep(0.01)

    write_register(0x12, 0x08)  # Limpiar bandera de transmisión
    print(f"Enviado: {msg}")

# Iniciar LoRa y enviar datos
if setup_lora():
    while True:
        send_message("AccelX:0.98,AccelY:-0.02,AccelZ:9.81")
        time.sleep(2)
