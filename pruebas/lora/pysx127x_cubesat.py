import time
import spidev
import RPi.GPIO as GPIO
from SX127x.LoRa import LoRa
from SX127x.board_config import BOARD

# Configurar la Raspberry para usar SPI
BOARD.setup()
GPIO.setwarnings(False)

class LoRaCubeSat(LoRa):
    def __init__(self, verbose=False):
        super().__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_pa_config(pa_select=1)  # Habilitar amplificación de potencia si es necesario
        self.set_freq(433)  # Configurar frecuencia en MHz (ajustar según la región)
        self.set_bw(125)  # Ancho de banda en kHz
        self.set_spreading_factor(7)  # Factor de expansión LoRa (ajustar según necesidades)
        self.set_coding_rate(5)  # Tasa de corrección de errores
        self.set_rx_crc(True)  # Habilitar CRC

    def on_rx_done(self):
        """ Manejar los datos recibidos """
        self.clear_irq_flags(RxDone=1)
        payload = self.read_payload(nocheck=True)
        received_message = bytes(payload).decode("utf-8", "ignore").strip()

        print(f"[CubeSat] Comando recibido: {received_message}")

        if received_message == "DATA?":
            data = self.get_sensor_data()
            self.send(data)
            print(f"[CubeSat] Enviando datos: {data}")

        self.set_mode(MODE.RXCONT)  # Volver al modo recepción

    def send(self, message):
        """ Enviar datos """
        self.write_payload(list(bytearray(message, "utf-8")))
        self.set_mode(MODE.TX)
        time.sleep(1)  # Esperar para transmisión
        self.set_mode(MODE.RXCONT)

    def get_sensor_data(self):
        """ Simulación de adquisición de datos de sensores """
        import random
        voltaje = round(random.uniform(3.7, 4.2), 2)  # Voltaje de la batería (simulado)
        altitud = round(random.uniform(50, 100), 1)  # Altitud en metros (simulado)
        temperatura = round(random.uniform(-10, 40), 1)  # Temperatura en °C
        return f"V:{voltaje}V, Alt:{altitud}m, Temp:{temperatura}C"

# Instancia del CubeSat LoRa
lora = LoRaCubeSat(verbose=False)

# Modo de recepción continua para recibir comandos
lora.set_mode(MODE.RXCONT)

print("[CubeSat] Esperando comandos de la estación terrena...")
try:
    while True:
        # Transmitir datos cada 5 segundos
        sensor_data = lora.get_sensor_data()
        lora.send(sensor_data)
        print(f"[CubeSat] Transmitiendo: {sensor_data}")
        time.sleep(5)

except KeyboardInterrupt:
    print("[CubeSat] Apagando...")
    GPIO.cleanup()
