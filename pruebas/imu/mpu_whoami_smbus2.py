from smbus2 import SMBus

address = 0x68  # I2C address
bus = SMBus(1)

who_am_i = bus.read_byte_data(address, 0x75)  # Read WHO_AM_I register
print(f"WHO_AM_I Register: {hex(who_am_i)}")
