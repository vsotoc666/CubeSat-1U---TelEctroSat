import smbus
import time

# Dirección I2C del MPU9250
MPU9250_ADDR = 0x68  # Puede ser 0x69 si AD0 está en alto

# Registros clave
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H = 0x43

# Inicializa I2C
bus = smbus.SMBus(1)

# Despierta el sensor (quita del modo de suspensión)
bus.write_byte_data(MPU9250_ADDR, PWR_MGMT_1, 0)

def read_word(reg):
    """ Lee dos bytes desde un registro y los combina en un valor de 16 bits """
    high = bus.read_byte_data(MPU9250_ADDR, reg)
    low = bus.read_byte_data(MPU9250_ADDR, reg + 1)
    value = (high << 8) | low
    if value > 32767:  # Convierte a complemento a dos si es negativo
        value -= 65536
    return value

while True:
    # Leer aceleración en el eje X, Y, Z
    accel_x = read_word(ACCEL_XOUT_H)
    accel_y = read_word(ACCEL_XOUT_H + 2)
    accel_z = read_word(ACCEL_XOUT_H + 4)
    
    # Leer giroscopio en el eje X, Y, Z
    gyro_x = read_word(GYRO_XOUT_H)
    gyro_y = read_word(GYRO_XOUT_H + 2)
    gyro_z = read_word(GYRO_XOUT_H + 4)

    # Mostrar datos
    print(f"Aceleración: X={accel_x}, Y={accel_y}, Z={accel_z}")
    print(f"Giroscopio: X={gyro_x}, Y={gyro_y}, Z={gyro_z}")

    time.sleep(1)

