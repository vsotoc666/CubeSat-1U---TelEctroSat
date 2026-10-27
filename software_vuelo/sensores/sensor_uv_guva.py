import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

class GUVA_Sensor:
    def __init__(self, channel=ADS.P0, gain=1):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.ads = ADS.ADS1115(self.i2c)
        self.ads.gain = gain
        self.channel = AnalogIn(self.ads, channel)
    
    def leer_datos(self):
        try:
            voltaje = self.channel.voltage
            indice_uv = round((voltaje / 3.3) * 7, 2)  # Escalar a rango 0-7
            return {
                "voltaje": round(voltaje, 4),
                "indice_uv": indice_uv
            }
        except Exception as e:
            print(f"Error al leer datos del GUVA: {e}")
            return None

if __name__ == "__main__":
    sensor = GUVA_Sensor()
    while True:
        datos = sensor.leer_datos()
        if datos:
            print(f"Voltaje: {datos['voltaje']} V")
            print(f"Índice UV: {datos['indice_uv']}")
            print("-" * 30)
        time.sleep(0.25)
