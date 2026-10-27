import pigpio
import time

class DHT11:
    def __init__(self, pi, gpio):
        self.pi = pi
        self.gpio = gpio
        self._humidity = None
        self._temperature = None

    def read(self):
        self.pi.set_mode(self.gpio, pigpio.OUTPUT)
        self.pi.write(self.gpio, 1)
        time.sleep(0.05)

        # Señal de inicio
        self.pi.write(self.gpio, 0)
        time.sleep(0.018)  # Baja por 18ms (según la hoja de datos)
        self.pi.set_mode(self.gpio, pigpio.INPUT)

        # Esperar respuesta del DHT11
        count = 0
        while self.pi.read(self.gpio) == 1:
            count += 1
            if count > 100:
                return False  # No hay respuesta

        # Leer datos del sensor (40 bits)
        data = []
        for i in range(40):
            while self.pi.read(self.gpio) == 0:
                pass  # Espera transición a alto
            count = 0
            while self.pi.read(self.gpio) == 1:
                count += 1
                if count > 100:
                    break
            data.append(count)

        # Procesar los datos
        humidity = sum(data[0:8]) // 8
        temperature = sum(data[16:24]) // 8

        # Validación de datos
        if 0 <= temperature <= 50 and 0 <= humidity <= 100:
            self._humidity = humidity
            self._temperature = temperature
            return True
        else:
            return False  # Datos inválidos

    def humidity(self):
        return self._humidity

    def temperature(self):
        return self._temperature

# Configurar el sensor en GPIO4 (Pin 7)
pi = pigpio.pi()
sensor = DHT11(pi,17)

try:
    while True:
        if sensor.read():
            print(f"🌡 Temperatura: {sensor.temperature()}°C")
            print(f"💧 Humedad: {sensor.humidity()}%")
        else:
            print("⚠ Error en la lectura del DHT11.")
        time.sleep(2)
except KeyboardInterrupt:
    print("Saliendo...")
    pi.stop()
