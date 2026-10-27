import spidev
import time
import RPi.GPIO as GPIO

# Configuración de pines
NSS_PIN = 8   # GPIO8 (Chip Select)
RST_PIN = 22  # GPIO22 (Reset)
DIO0_PIN = 23 # GPIO23 (Interrupción)

# Inicializar GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(NSS_PIN, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(RST_PIN, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(DIO0_PIN, GPIO.IN)

# Inicializar SPI
spi = spidev.SpiDev()
spi.open(0, 0)  # Bus 0, Dispositivo 0
spi.max_speed_hz = 5000000  # Velocidad SPI

# Función para escribir en un registro
def write_register(reg, value):
    GPIO.output(NSS_PIN, GPIO.LOW)
    spi.xfer2([reg | 0x80, value])
    GPIO.output(NSS_PIN, GPIO.HIGH)

# Función para leer un registro
def read_register(reg):
    GPIO.output(NSS_PIN, GPIO.LOW)
    response = spi.xfer2([reg & 0x7F, 0x00])
    GPIO.output(NSS_PIN, GPIO.HIGH)
    return response[1]

# Reiniciar el SX1278
def reset_lora():
    GPIO.output(RST_PIN, GPIO.LOW)
    time.sleep(0.01)
    GPIO.output(RST_PIN, GPIO.HIGH)
    time.sleep(0.01)

# Configuración del LoRa SX1278
def setup_lora():
    reset_lora()
    time.sleep(0.1)

    # Modo Sleep
    write_register(0x01, 0x00)
    time.sleep(0.1)

    # Configurar modo LoRa
    write_register(0x01, 0x80)
    time.sleep(0.1)

    # Configuración de frecuencia (433 MHz o 915 MHz según la región)
    write_register(0x06, 0x6C)  # MHz parte alta
    write_register(0x07, 0x80)  # MHz parte media
    write_register(0x08, 0x00)  # MHz parte baja

    # Configuración de parámetros de modulación
    write_register(0x1D, 0x72)  # Ancho de banda y codificación
    write_register(0x1E, 0x74)  # Spreading factor y CRC

    # Potencia de transmisión
    write_register(0x09, 0xFF)  # Máxima potencia

    # Modo de espera
    write_register(0x01, 0x81)
    print("LoRa SX1278 configurado correctamente")

# Enviar un mensaje
def send_message(message):
    write_register(0x01, 0x83)  # Modo Standby
    write_register(0x0E, 0x00)  # Dirección FIFO TX

    for byte in message.encode():
        write_register(0x00, byte)

    write_register(0x22, len(message))  # Longitud del mensaje
    write_register(0x01, 0x83)  # Modo TX
    time.sleep(0.1)

    while (read_register(0x12) & 0x08) == 0:
        time.sleep(0.01)

    write_register(0x12, 0x08)  # Limpiar flag de TX
    print(f"Mensaje enviado: {message}")

# Recibir un mensaje
def receive_message():
    write_register(0x01, 0x85)  # Modo RX continuo
    while GPIO.input(DIO0_PIN) == 0:
        time.sleep(0.01)

    irq_flags = read_register(0x12)
    if irq_flags & 0x40:
        print("Mensaje recibido!")

        # Leer longitud del mensaje
        packet_length = read_register(0x13)
        write_register(0x0D, 0x00)

        message = ""
        for _ in range(packet_length):
            message += chr(read_register(0x00))

        write_register(0x12, 0x40)  # Limpiar flag de RX
        return message
    else:
        return None

# Prueba de transmisión y recepción
setup_lora()
time.sleep(2)

# Enviar mensaje de prueba
send_message("Hola LoRa!")

# Intentar recibir mensaje
time.sleep(1)
mensaje_recibido = receive_message()
if mensaje_recibido:
    print(f"Mensaje recibido: {mensaje_recibido}")

# Cerrar SPI al final
spi.close()
GPIO.cleanup()
