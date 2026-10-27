
import time
import board
import busio
from adafruit_ads1x15.adafruit_ads1115 import ADS1115

i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS1115(i2c)

# Leer el valor en el canal 0
while True:
    voltaje = ads.read_adc(0, gain=1)  # canal 0, ganancia 1
    print("Voltaje: ", voltaje)
    time.sleep(1)
