import smbus

bus = smbus.SMBus(1)
MPU_ADDR = 0x68
WHO_AM_I_REG = 0x75  # Registro WHO_AM_I

try:
    who_am_i = bus.read_byte_data(MPU_ADDR, WHO_AM_I_REG)
    print(f"ID del IMU: 0x{who_am_i:02X}")
except Exception as e:
    print(f"Error al leer el IMU: {e}")

