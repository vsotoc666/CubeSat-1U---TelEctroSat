import time
from mpu9250_jmdev.registers import *
from mpu9250_jmdev.mpu_9250 import MPU9250

# Inicializar el MPU9250
mpu = MPU9250(
    address_ak=AK8963_ADDRESS,  # Dirección del magnetómetro
    address_mpu_master=0x68,  # Dirección I2C del MPU9250 (0x69 si AD0 está en alto)
    address_mpu_slave=None,
    bus=1,  # Bus I2C (usualmente 1 en Raspberry Pi)
    gfs=GFS_500,  # Sensibilidad giroscopio (500°/s)
    afs=AFS_4G,   # Sensibilidad acelerómetro (±4g)
    mfs=AK8963_BIT_16,  # Resolución del magnetómetro
    mode=AK8963_MODE_C100HZ  # Frecuencia de muestreo del magnetómetro
)

# Configurar el sensor
mpu.calibrate()
mpu.configure()

# Bucle de lectura
while True:
    accel = mpu.readAccelerometerMaster()  # Acelerómetro (x, y, z) en g
    gyro = mpu.readGyroscopeMaster()  # Giroscopio (x, y, z) en °/s
    mag = mpu.readMagnetometerMaster()  # Magnetómetro (x, y, z) en µT

    # Mostrar datos
    print(f"Acelerómetro: {accel}")
    print(f"Giroscopio: {gyro}")
    print(f"Magnetómetro: {mag}")
    print("-" * 40)

    # Muestreo 4 veces por segundo (cada 0.25s)
    time.sleep(0.25)
