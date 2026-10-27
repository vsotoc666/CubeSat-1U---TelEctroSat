import time
from mpu9250_jmdev.registers import *
from mpu9250_jmdev.mpu_9250 import MPU9250

GRAVITY_MS2 = 9.80665  # Gravedad estándar en m/s²

# Inicializar solo el MPU6500 (sin magnetómetro)
mpu = MPU9250(
    address_mpu_master=0x68,  # Dirección I2C del MPU9250
    bus=1                     # Bus I2C
)

# Configurar solo giroscopio y acelerómetro
try:
    mpu.configureMPU6500(GFS_500, AFS_4G)  # Configurar rangos
    print("Configuración de MPU6500 completada.\n")

    # Calibrar acelerómetro y giroscopio manualmente
    print("Realizando calibración simple...")
    gyro_offset = mpu.readGyroscopeMaster()
    accel_offset = mpu.readAccelerometerMaster()
    print(f"Offset giroscopio: {gyro_offset}")
    print(f"Offset acelerómetro: {accel_offset}\n")

    # Bucle de lectura
    while True:
        try:
            accel = mpu.readAccelerometerMaster()
            gyro = mpu.readGyroscopeMaster()

            # Ajustar con offset y convertir a m/s²
            accel_ms2 = tuple(round((a - ao) * GRAVITY_MS2, 1) for a, ao in zip(accel, accel_offset))
            gyro_rounded = tuple(round(g - go, 1) for g, go in zip(gyro, gyro_offset))

            # Mostrar datos corregidos
            print(f"Acelerómetro (m/s²): {accel_ms2}")
            print(f"Giroscopio (°/s): {gyro_rounded}")
            print("-" * 40)

            # Muestreo cada 0.25s (4 Hz)
            time.sleep(0.25)

        except KeyboardInterrupt:
            print("\nLectura detenida por el usuario")
            break

except Exception as e:
    print(f"Error al configurar MPU6500: {e}")
