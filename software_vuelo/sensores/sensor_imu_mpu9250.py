import time
from mpu9250_jmdev.registers import *
from mpu9250_jmdev.mpu_9250 import MPU9250

GRAVITY_MS2 = 9.80665  # Gravedad estándar en m/s²

class MPU9250Sensor:
    def __init__(self, address=0x68, bus=1):
        self.mpu = MPU9250(address_mpu_master=address, bus=bus)
        self.accel_offset = (0, 0, 0)
        self.gyro_offset = (0, 0, 0)
        self._configure()

    def _configure(self):
        try:
            self.mpu.configureMPU6500(GFS_500, AFS_4G)  # Configurar rangos
            print("Configuración de MPU6500 completada.")

            # Calibrar sensores
            print("Calibrando sensores...")
            self.gyro_offset = self.mpu.readGyroscopeMaster()
            self.accel_offset = self.mpu.readAccelerometerMaster()
            print(f"Offset giroscopio: {self.gyro_offset}")
            print(f"Offset acelerómetro: {self.accel_offset}")
        except Exception as e:
            print(f"Error al configurar MPU6500: {e}")

    def leer_datos(self):
        try:
            accel = self.mpu.readAccelerometerMaster()
            gyro = self.mpu.readGyroscopeMaster()

            # Ajustar con offset y convertir aceleración a m/s²
            accel_ms2 = tuple(round((a - ao) * GRAVITY_MS2, 2) for a, ao in zip(accel, self.accel_offset))
            gyro_rounded = tuple(round(g - go, 2) for g, go in zip(gyro, self.gyro_offset))

            return {
                "acelerometro_x": accel_ms2[0],
                "acelerometro_y": accel_ms2[1],
                "acelerometro_z": accel_ms2[2],
                "giroscopio_x": gyro_rounded[0],
                "giroscopio_y": gyro_rounded[1],
                "giroscopio_z": gyro_rounded[2]
            }
        except Exception as e:
            print(f"Error al leer datos del MPU9250: {e}")
            return None

if __name__ == "__main__":
    sensor = MPU9250Sensor()
    while True:
        datos = sensor.leer_datos()
        if datos:
            print(f"Acelerómetro (m/s²): x={datos['acelerometro_x']}, y={datos['acelerometro_y']}, z={datos['acelerometro_z']}")
            print(f"Giroscopio (°/s): x={datos['giroscopio_x']}, y={datos['giroscopio_y']}, z={datos['giroscopio_z']}")
            print("-" * 40)
        time.sleep(0.25)
