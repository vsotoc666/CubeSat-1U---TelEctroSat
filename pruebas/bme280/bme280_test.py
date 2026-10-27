import smbus2
import bme280
import time

port = 1  # En Raspberry Pi, el bus I2C suele ser 1
address = 0x76  # Dirección por defecto del BME280

# Inicializar el sensor
bus = smbus2.SMBus(port)
calibration_params = bme280.load_calibration_params(bus, address)

while True:
	# Leer datos del sensor
	data = bme280.sample(bus, address, calibration_params)

	# Imprimir los valores
	print(f"Temperatura: {data.temperature:.2f} °C")
	print(f"Presión: {data.pressure:.2f} hPa")
	print(f"Humedad: {data.humidity:.2f} %")
	print(f"-" * 30)
	time.sleep(0.25)
