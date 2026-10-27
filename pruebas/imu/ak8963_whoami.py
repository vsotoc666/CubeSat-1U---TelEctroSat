from smbus2 import SMBus

MAG_ADDRESS = 0x0C  # Dirección del AK8963
bus = SMBus(1)

try:
    who_am_i = bus.read_byte_data(MAG_ADDRESS, 0x00)
    print(f"Magnetómetro detectado, WHO_AM_I: {who_am_i:#x}")
except OSError:
    print("No se detecta el magnetómetro. Revisa las soldaduras o verifica si tienes un MPU6500.")
