import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)

canal = AnalogIn(ads, ADS.P1)

voltaje_dividido = canal.voltage
voltaje_real = voltaje_dividido * 2

print(f"Voltaje medido: {voltaje_real:.2f} V")
