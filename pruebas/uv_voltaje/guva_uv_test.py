import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Inicializar I2C
i2c = busio.I2C(board.SCL, board.SDA)

# Inicializar ADS1115
ads = ADS.ADS1115(i2c)
ads.gain = 1

# Crear canal de lectura en A0 (donde está el GUVA)
canal = AnalogIn(ads, ADS.P0)

try:
    while True:
        voltaje = canal.voltage
        print(f"Voltaje: {voltaje:.4f} V")
        time.sleep(0.25)  # Leer cada 0.25 segundos

except KeyboardInterrupt:
    print("Lectura detenida.")
except Exception as e:
    print(f"Error: {e}")
