#!/usr/bin/env python3
import time
import smbus2
import csv
import os

MPU9250_ADDRESS = 0x68
BME280_ADDRESS  = 0x76
#AK8963_ADDRESS  = 0x0C

BME280_REG_CALIB_START = 0x88
BME280_REG_ID          = 0xD0
BME280_REG_CTRL_MEAS   = 0xF4
BME280_REG_CONFIG      = 0xF5
BME280_REG_TEMP_MSB    = 0xFA



MPU9250_PWR_MGMT_1   = 0x6B
MPU9250_ACCEL_CONFIG = 0x1C
MPU9250_ACCEL_XOUT_H = 0x3B
MPU9250_GYRO_CONFIG  = 0x1B
MPU9250_GYRO_XOUT_H  = 0x43
MPU9250_WHO_AM_I     = 0x75
MPU9250_INT_PIN_CFG  = 0x37

#AK8963_CNTL1 = 0x0A
#AK8963_ST1   = 0x02




bus = smbus2.SMBus(1)




def bme280_read_calibration_params():



    calib = {}
    data = bus.read_i2c_block_data(BME280_ADDRESS, BME280_REG_CALIB_START, 6)
    # T1 (unsigned 16 bits)
    calib['T1'] = data[1] << 8 | data[0]
    # T2 (signed 16 bits)
    raw_T2 = data[3] << 8 | data[2]
    if raw_T2 & 0x8000:
        raw_T2 -= 65536
    calib['T2'] = raw_T2
    # T3 (signed 16 bits)
    raw_T3 = data[5] << 8 | data[4]
    if raw_T3 & 0x8000:
        raw_T3 -= 65536
    calib['T3'] = raw_T3
    return calib

def bme280_init():
    chip_id = bus.read_byte_data(BME280_ADDRESS, BME280_REG_ID)
    if chip_id != 0x60:
        print("BME280: unexpected ID: 0x{:02X}".format(chip_id))
    bus.write_byte_data(BME280_ADDRESS, BME280_REG_CTRL_MEAS, 0x27)
    bus.write_byte_data(BME280_ADDRESS, BME280_REG_CONFIG, 0x00)

def bme280_read_temperature(calib_params):
    data = bus.read_i2c_block_data(BME280_ADDRESS, BME280_REG_TEMP_MSB, 3)
    adc_T = ((data[0] << 12) | (data[1] << 4) | (data[2] >> 4)) & 0xFFFFF
    T1 = calib_params['T1']
    T2 = calib_params['T2']
    T3 = calib_params['T3']
    var1 = (adc_T / 16384.0 - T1 / 1024.0) * T2
    var2 = (adc_T / 131072.0 - T1 / 8192.0) ** 2 * T3
    t_fine = var1 + var2
    temperature = t_fine / 5120.0
    return temperature

def mpu9250_init():
    bus.write_byte_data(MPU9250_ADDRESS, MPU9250_PWR_MGMT_1, 0x00)
    time.sleep(0.1)
    bus.write_byte_data(MPU9250_ADDRESS, MPU9250_ACCEL_CONFIG, 0x00)
    bus.write_byte_data(MPU9250_ADDRESS, MPU9250_GYRO_CONFIG, 0x00)
    time.sleep(0.1)
    whoami = bus.read_byte_data(MPU9250_ADDRESS, MPU9250_WHO_AM_I)
    print("MPU9250 WHO_AM_I = 0x{:02X}".format(whoami))

def mpu9250_read_accel():
    data = bus.read_i2c_block_data(MPU9250_ADDRESS, MPU9250_ACCEL_XOUT_H, 6)
    raw_ax = (data[0] << 8) | data[1]
    raw_ay = (data[2] << 8) | data[3]
    raw_az = (data[4] << 8) | data[5]
    if raw_ax & 0x8000: raw_ax -= 65536
    if raw_ay & 0x8000: raw_ay -= 65536
    if raw_az & 0x8000: raw_az -= 65536
    ax = raw_ax / 16384.0
    ay = raw_ay / 16384.0
    az = raw_az / 16384.0
    return (ax, ay, az)

def mpu9250_read_gyro():
    data = bus.read_i2c_block_data(MPU9250_ADDRESS, MPU9250_GYRO_XOUT_H, 6)
    raw_gx = (data[0] << 8) | data[1]
    raw_gy = (data[2] << 8) | data[3]
    raw_gz = (data[4] << 8) | data[5]
    if raw_gx & 0x8000: raw_gx -= 65536
    if raw_gy & 0x8000: raw_gy -= 65536
    if raw_gz & 0x8000: raw_gz -= 65536
    gx = raw_gx / 131.0
    gy = raw_gy / 131.0
    gz = raw_gz / 131.0
    return (gx, gy, gz)
"""
def ak8963_init():
   bus.write_byte_data(AK8963_ADDRESS, AK8963_CNTL1, 0x16)
   time.sleep(0.1)

def ak8963_read_mag():
    status = bus.read_byte_data(AK8963_ADDRESS, AK8963_ST1)
    if status & 0x01:
        data = bus.read_i2c_block_data(AK8963_ADDRESS, 0x03, 7)
        raw_mx = data[1] << 8 | data[0]
        raw_my = data[3] << 8 | data[2]
        raw_mz = data[5] << 8 | data[4]
        if raw_mx > 32767: raw_mx -= 65536
        if raw_my > 32767: raw_my -= 65536
        if raw_mz > 32767: raw_mz -= 65536
        mx = raw_mx * 0.15
        my = raw_my * 0.15
        mz = raw_mz * 0.15
        return (mx, my, mz)
    else:
        return (None, None, None)
"""
def init_csv(filename):
    if not os.path.exists(filename):
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            header = ["timestamp", "temp_C", "ax_g", "ay_g", "az_g", "gx_dps", "gy_dps", "gz_dps", "mx_uT", "my_uT", "mz_uT"]
            writer.writerow(header)

def poto():
    csv_filename = "i2c_data.txt"
    init_csv(csv_filename)

    bme280_init()
    calib_params = bme280_read_calibration_params()

    mpu9250_init()

    print("Cancelalo con ctr c")

    try:
        while True:
            temp_c = bme280_read_temperature(calib_params)
            ax, ay, az = mpu9250_read_accel()
            gx, gy, gz = mpu9250_read_gyro()
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"{timestamp} | Temp: {temp_c:.2f}°C | Accel: X={ax:.2f}g Y={ay:.2f}g Z={az:.2f}g | "
                  f"Giro: X={gx:.2f}°/s Y={gy:.2f}°/s Z={gz:.2f}°/s")
            with open(csv_filename, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([timestamp, f"{temp_c:.2f}", f"{ax:.2f}", f"{ay:.2f}", f"{az:.2f}",
                                 f"{gx:.2f}", f"{gy:.2f}", f"{gz:.2f}"
                                 ])
            time.sleep(1.0)
    except KeyboardInterrupt:
        print("\ndeteniendo la lectura de sensores.")

if __name__ == "__main__":
    poto()
