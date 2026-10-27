import smbus
import time
import numpy as np

# Dirección I2C del MPU9250
MPU9250_ADDR = 0x68  # Puede ser 0x69 si AD0 está en alto

# Registros
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H = 0x43

# Inicializa I2C
bus = smbus.SMBus(1)

# Despierta el sensor (quita el modo de suspensión)
bus.write_byte_data(MPU9250_ADDR, PWR_MGMT_1, 0)

def read_word(reg):
    """ Lee dos bytes desde un registro y los combina en un valor de 16 bits """
    high = bus.read_byte_data(MPU9250_ADDR, reg)
    low = bus.read_byte_data(MPU9250_ADDR, reg + 1)
    value = (high << 8) | low
    if value > 32767:  # Convierte a complemento a dos si es negativo
        value -= 65536
    return value

def calibrate(samples=500):
    """ Calcula los offsets del acelerómetro y giroscopio tomando muestras en reposo """
    accel_offsets = np.array([0.0, 0.0, 0.0])
    gyro_offsets = np.array([0.0, 0.0, 0.0])

    print("Coloca el sensor en una superficie estable...")
    time.sleep(2)

    for _ in range(samples):
        accel_x = read_word(ACCEL_XOUT_H)
        accel_y = read_word(ACCEL_XOUT_H + 2)
        accel_z = read_word(ACCEL_XOUT_H + 4)
        
        gyro_x = read_word(GYRO_XOUT_H)
        gyro_y = read_word(GYRO_XOUT_H + 2)
        gyro_z = read_word(GYRO_XOUT_H + 4)

        accel_offsets += np.array([accel_x, accel_y, accel_z])
        gyro_offsets += np.array([gyro_x, gyro_y, gyro_z])

        time.sleep(0.002)  # Pequeño retraso para evitar sobrecarga

    # Promediar las muestras
    accel_offsets /= samples
    gyro_offsets /= samples

    print(f"Offsets Acelerómetro: {accel_offsets}")
    print(f"Offsets Giroscopio: {gyro_offsets}")

    return accel_offsets, gyro_offsets

# Calibración
accel_bias, gyro_bias = calibrate()

# Bucle principal para mostrar valores calibrados
print("\nLeyendo valores calibrados... Presiona Ctrl+C para salir.")
try:
    while True:
        # Leer aceleración en el eje X, Y, Z
        accel_x = read_word(ACCEL_XOUT_H) - accel_bias[0]
        accel_y = read_word(ACCEL_XOUT_H + 2) - accel_bias[1]
        accel_z = read_word(ACCEL_XOUT_H + 4) - accel_bias[2]

        # Leer giroscopio en el eje X, Y, Z
        gyro_x = read_word(GYRO_XOUT_H) - gyro_bias[0]
        gyro_y = read_word(GYRO_XOUT_H + 2) - gyro_bias[1]
        gyro_z = read_word(GYRO_XOUT_H + 4) - gyro_bias[2]

        # Mostrar datos corregidos
        print(f"X={accel_x:.2f}, Y={accel_y:.2f}, Z={accel_z:.2f}")
        time.sleep(0.125)

except KeyboardInterrupt:
    print("\nLectura detenida por el usuario.")
