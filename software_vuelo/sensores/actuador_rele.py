import RPi.GPIO as GPIO
import time

class RelayController:
    def __init__(self, relay_pin=20):
        self.relay_pin = relay_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.relay_pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.output(self.relay_pin, GPIO.LOW)
        time.sleep(2)
        GPIO.cleanup()
    
    def activar_rele(self):
        GPIO.output(self.relay_pin, GPIO.LOW)
        print("Relé activado, estado GPIO:", GPIO.input(self.relay_pin))
        GPIO.cleanup()
        exit()
    
    def limpiar_gpio(self):
        GPIO.cleanup()
        print("GPIO limpiado.")

if __name__ == "__main__":
    rele = RelayController()
    try:
        rele.activar_rele()
        time.sleep(3)
        rele.desactivar_rele()
    except KeyboardInterrupt:
        print("Interrupción detectada. Saliendo...")
    finally:
        rele.limpiar_gpio()
