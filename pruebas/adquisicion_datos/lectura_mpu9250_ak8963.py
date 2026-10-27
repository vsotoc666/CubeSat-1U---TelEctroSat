import time
import smbus2

MPU9250_ADDRESS = 0x68  # o 0x69 si AD0 está a 3.3V

MPU9250_PWR_MGMT_1     = 0x6B
MPU9250_ACCEL_CONFIG   = 0x1C
MPU9250_ACCEL_XOUT_H   = 0x3B  # 3B..40 (X, Y, Z)
MPU9250_WHO_AM_I       = 0x75

bus = smbus2.SMBus(1)  # En Raspberry Pi, el bus I2C suele ser "1"

def mpu9250_init():
    """
    Inicializa el MPU9250:
      - Sale de modo sleep.
      - Configura acelerómetro (±2g) y giroscopio (±250°/s).
      - Activa el modo bypass para acceder al magnetómetro.
    """
    # Salir del modo sleep
    bus.write_byte_data(MPU9250_ADDRESS, MPU9250_PWR_MGMT_1, 0x00)
    time.sleep(0.1)
    # Configurar acelerómetro en ±2g (0x00)
    bus.write_byte_data(MPU9250_ADDRESS, MPU9250_ACCEL_CONFIG, 0x00)
    # Configurar giroscopio en ±250°/s (0x00)
    bus.write_byte_data(MPU9250_ADDRESS, MPU9250_GYRO_CONFIG, 0x00)
    time.sleep(0.1)
    # Activar modo bypass para acceder al AK8963 directamente
    bus.write_byte_data(MPU9250_ADDRESS, MPU9250_INT_PIN_CFG, 0x02)
    time.sleep(0.1)
    # (Opcional) Verificar WHO_AM_I
    whoami = bus.read_byte_data(MPU9250_ADDRESS, MPU9250_WHO_AM_I)
    print("MPU9250 WHO_AM_I = 0x{:02X}".format(whoami))
    # Inicializar el magnetómetro
    ak8963_init()

def mpu9250_read_accel():
    """
    Lee la aceleración (X, Y, Z) en g (±2g)
    """
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
    """
    Lee la velocidad angular (X, Y, Z) en °/s (±250°/s)
    """
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

# ============================================================================
# Funciones para el magnetómetro (AK8963)
# ============================================================================
def ak8963_init():
    """
    Inicializa el magnetómetro AK8963 en modo de medición continua a 16 bits.
    """
    # 0x16: 16 bits, modo de medición continua 2 (100 Hz)
    bus.write_byte_data(AK8963_ADDRESS, AK8963_CNTL1, 0x16)
    time.sleep(0.1)

def ak8963_read_mag():
    """
    Lee los valores del magnetómetro en microTesla.
    Retorna una tupla (mx, my, mz). Si no hay datos listos, retorna (None, None, None).
    """
    status = bus.read_byte_data(AK8963_ADDRESS, AK8963_ST1)
    if status & 0x01:  # Bit DRDY: datos listos
        # Leer 7 bytes: 6 de datos y 1 de ST2 (para descartar)
        data = bus.read_i2c_block_data(AK8963_ADDRESS, 0x03, 7)
        raw_mx = data[1] << 8 | data[0]
        raw_my = data[3] << 8 | data[2]
        raw_mz = data[5] << 8 | data[4]
        if raw_mx > 32767: raw_mx -= 65536
        if raw_my > 32767: raw_my -= 65536
        if raw_mz > 32767: raw_mz -= 65536
        # Factor de escala aproximado: 0.15 µT/LSB
        mx = raw_mx * 0.15
        my = raw_my * 0.15
        mz = raw_mz * 0.15
        return (mx, my, mz)
    else:
        return (None, None, None)

# ============================================================================
# Función para inicializar el archivo CSV (en formato .txt)
# ============================================================================
def init_csv(filename):
    if not os.path.exists(filename):
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            header = ["timestamp","ax_g", "ay_g", "az_g", "gx_dps", "gy_dps", "gz_dps", "mx_uT", "my_uT", "mz_uT"]
            writer.writerow(header)

def main():
    csv_filename = "sensor_data.txt"
    init_csv(csv_filename)

    mpu9250_init()

    try:
        while True:
            # Leer temperatura (BME280)
            # Leer aceleración (MPU9250)
            ax, ay, az = mpu9250_read_accel()
            # Leer velocidad angular (giroscopio, MPU9250)
            gx, gy, gz = mpu9250_read_gyro()
            # Leer campo magnético (AK8963)
            mx, my, mz = ak8963_read_mag()

            # Crear timestamp legible
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            # Mostrar en consola
            print(f"{timestamp} | Accel: X={ax:.2f}g Y={ay:.2f}g Z={az:.2f}g | "
                  f"Giro: X={gx:.2f}°/s Y={gy:.2f}°/s Z={gz:.2f}°/s | Mag: X={mx if mx is not None else 'NA'} "
                  f"µT, Y={my if my is not None else 'NA'} µT, Z={mz if mz is not None else 'NA'} µT")
            
            # Guardar en archivo CSV
            with open(csv_filename, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([timestamp, f"{ax:.2f}", f"{ay:.2f}", f"{az:.2f}",
                                 f"{gx:.2f}", f"{gy:.2f}", f"{gz:.2f}",
                                 f"{mx:.2f}" if mx is not None else "NA",
                                 f"{my:.2f}" if my is not None else "NA",
                                 f"{mz:.2f}" if mz is not None else "NA"])
            time.sleep(1.0)
    except KeyboardInterrupt:
        print("\nDeteniendo la lectura de sensores.")

if __name__ == "__main__":
    main()
