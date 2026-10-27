import RPi.GPIO as GPIO
import time

# Definir los pines GPIO
led_pins = [40, 38, 36]  # Números físicos de los pines

# Configurar GPIO
GPIO.setmode(GPIO.BOARD)  # Usar numeración física de pines
GPIO.setup(led_pins, GPIO.OUT)  # Configurar pines como salida

try:
    while True:
        # Encender los LEDs
        for pin in led_pins:
            GPIO.output(pin, GPIO.HIGH)
        time.sleep(1)

        # Apagar los LEDs
        for pin in led_pins:
            GPIO.output(pin, GPIO.LOW)
        time.sleep(1)

except KeyboardInterrupt:
    print("Saliendo...")
    GPIO.cleanup()  # Limpiar configuración de los pines al salir

