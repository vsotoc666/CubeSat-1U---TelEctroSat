import smbus
import time
import numpy as np

MPU9250_ADDR = 0x68
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H = 0x43

bus = smbus.SMBus(1)
bus.write_byte_data(MPU9250_ADDR, PWR_MGMT_1, 0)  # Despierta el sensor

def read_word(reg):
    high = bus.read_byte_data(MPU9250_ADDR, reg)
    low = bus.read_byte_data(MPU9250_ADDR, reg + 1)
    value = (high << 8) | low
    if value > 32767:
        value -= 65536
    return value

def calibrate(samples=500):
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

    # Promediar
    accel_offsets /= samples
    gyro_offsets /= samples

    print(f"Offsets Acelerómetro: {accel_offsets}")
    print(f"Offsets Giroscopio: {gyro_offsets}")

    return accel_offsets, gyro_offsets

accel_bias, gyro_bias = calibrate()

print(read_word(ACCEL_XOUT_H) - accel_bias[0])
