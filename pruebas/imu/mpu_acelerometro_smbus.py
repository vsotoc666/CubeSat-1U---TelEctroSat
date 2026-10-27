import smbus
import time

MPU9250_ADDR = 0x68

ACCEL_XOUT_H = 0x3B
ACCEL_CONFIG = 0x1C
PWR_MGMT_1 = 0x6B

ACCEL_SENSITIVITY = 16384.0

bus = smbus.SMBus(1)

def init_mpu9250():

    bus.write_byte_data(MPU9250_ADDR, PWR_MGMT_1, 0x00)
    time.sleep(0.1)

    bus.write_byte_data(MPU9250_ADDR, ACCEL_CONFIG, 0x00)

def read_accel():
    data = bus.read_i2c_block_data(MPU9250_ADDR, ACCEL_XOUT_H, 6)

    accel_x = (data[0] << 8 | data[1])
    accel_y = (data[2] << 8 | data[3])
    accel_z = (data[4] << 8 | data[5])

    accel_x = accel_x - 65536 if accel_x > 32767 else accel_x
    accel_y = accel_y - 65536 if accel_y > 32767 else accel_y
    accel_z = accel_z - 65536 if accel_z > 32767 else accel_z

    accel_x /= ACCEL_SENSITIVITY
    accel_y /= ACCEL_SENSITIVITY
    accel_z /= ACCEL_SENSITIVITY

    return accel_x, accel_y, accel_z

init_mpu9250()

while True:
    ax, ay, az = read_accel()
    print(f"X={ax:.2f} g, Y={ay:.2f} g, Z={az:.2f} g")
    time.sleep(0.125)
