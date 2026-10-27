import RPi.GPIO as GPIO
import time

LED_PIN = 17  # GPIO donde está el LED

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

try:
    while True:
        GPIO.output(LED_PIN, GPIO.HIGH)  # Encender LED
        time.sleep(1)  # Esperar 1 segundo
        GPIO.output(LED_PIN, GPIO.LOW)  # Apagar LED
        time.sleep(1)  # Esperar 1 segundo
except KeyboardInterrupt:
    GPIO.cleanup()  # Limpiar configuración al salir

