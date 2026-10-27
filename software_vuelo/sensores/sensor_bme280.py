import smbus2
import bme280
import time

class BME280Sensor:
    def __init__(self, port=1, address=0x76):
        self.bus = smbus2.SMBus(port)
        self.address = address
        self.calibration_params = bme280.load_calibration_params(self.bus, self.address)

    def leer_datos(self):
        try:
            data = bme280.sample(self.bus, self.address, self.calibration_params)
            return {
                "temperatura": round(data.temperature, 2),
                "presion": round(data.pressure, 2),
                "humedad": round(data.humidity, 2)
            }
        except Exception as e:
            print(f"Error al leer datos del BME280: {e}")
            return None

if __name__ == "__main__":
    sensor = BME280Sensor()
    while True:
        datos = sensor.leer_datos()
        if datos:
            print(f"Temperatura: {datos['temperatura']} °C")
            print(f"Presión: {datos['presion']} hPa")
            print(f"Humedad: {datos['humedad']} %")
            print("-" * 30)
        time.sleep(0.25)
