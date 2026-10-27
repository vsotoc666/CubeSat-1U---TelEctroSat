import RPi.GPIO as GPIO
import time

# Define el número del pin (ajústalo según tu conexión)
DIO0 = 7  # Ejemplo: pin 7 en modo BOARD o BCM según tu configuración

# Configuración inicial de GPIO
GPIO.setwarnings(False)
# Elige el modo: BOARD (números físicos) o BCM (números GPIO)
GPIO.setmode(GPIO.BOARD)  # Cambia a GPIO.setmode(GPIO.BCM) si usas números BCM

# Configura el pin DIO0 como entrada
GPIO.setup(DIO0, GPIO.IN)

# Intenta eliminar cualquier detección de borde previamente configurada
try:
    GPIO.remove_event_detect(DIO0)
    print("Detección de borde previa removida.")
except RuntimeError as e:
    # Si no había ninguna, simplemente muestra un mensaje
    print("No había detección previa o ya fue removida:", e)

# Ahora, agrega la detección de borde en flanco ascendente (RISING)
try:
    GPIO.add_event_detect(DIO0, GPIO.RISING, callback=lambda pin: print(f"Evento detectado en pin {pin}"))
    print("Detección de borde añadida exitosamente.")
except RuntimeError as e:
    print("Error al agregar la detección de borde:", e)

# Mantén el programa en ejecución para poder detectar eventos
print("Esperando eventos en el pin DIO0. Presiona Ctrl+C para salir.")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Terminando...")
finally:
    GPIO.cleanup()
