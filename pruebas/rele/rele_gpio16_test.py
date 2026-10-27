import RPi.GPIO as GPIO
import time

# Usamos la numeración BCM para referirnos al GPIO20 (corresponde al pin físico 38)
GPIO.setmode(GPIO.BCM)

# Definir el pin para el relé
RELAY_PIN1 = 16

# Configuramos el pin como salida, iniciando en HIGH (relé desactivado, asumiendo lógica activa en bajo)
GPIO.setup(RELAY_PIN1, GPIO.OUT, initial=GPIO.LOW)

def activar_rele1():
    # Activa el relé (lógica activa en bajo)
    GPIO.output(RELAY_PIN1, GPIO.LOW)
    print("Relé activado, estado GPIO:", GPIO.input(RELAY_PIN1))

def main():
    flag=False
    try:
        while flag != True:
            activar_rele1()
            time.sleep(3)
            print("Terminando el programa, saliendo")
            flag=True
    except KeyboardInterrupt:
        print("Interrupción detectada. Saliendo...")
    finally:
        GPIO.cleanup()  # Limpia la configuración de los pines
        print("GPIO limpiado.")

if __name__ == '__main__':
    main()
