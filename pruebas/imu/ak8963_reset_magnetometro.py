import time
from mpu9250_jmdev.registers import AK8963_CNTL2
from mpu9250_jmdev.mpu_9250 import MPU9250

# Inicializar el MPU9250
mpu = MPU9250(
    address_mpu_master=0x68,
    address_ak=0x0C,  # Dirección estándar del AK8963
    bus=1
)

# Intentar resetear el magnetómetro
try:
    print("Reseteando el magnetómetro AK8963...")
    mpu.writeAK(AK8963_CNTL2, 0x01)  # Escribir 0x01 en CNTL2 para resetear
    time.sleep(0.1)

    print("Intentando reconfigurar...")
    mpu.configure()
    print("Magnetómetro reseteado y configurado correctamente.")
    
    # Leer datos para probar
    mag = mpu.readMagnetometerMaster()
    print(f"Lectura de prueba del magnetómetro: {mag}")

except Exception as e:
    print(f"Error durante el reset: {e}")
