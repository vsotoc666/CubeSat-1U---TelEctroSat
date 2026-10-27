#!/usr/bin/env python3
import time
import smbus2

# ============================================================================
# DIRECCIONES I2C (ajusta si conectaste AD0/SDO de forma distinta)
# ============================================================================
MPU9250_ADDRESS = 0x68  # o 0x69 si AD0 está a 3.3V
BME280_ADDRESS  = 0x76  # o 0x77 si SDO está a 3.3V

# ============================================================================
# REGISTROS DEL BME280 (solo para temperatura en este ejemplo)
# ============================================================================
BME280_REG_CALIB_START = 0x88  # Comienzo de datos de calibración (T1, T2, T3, etc.)
BME280_REG_ID          = 0xD0
BME280_REG_CTRL_MEAS   = 0xF4
BME280_REG_TEMP_MSB    = 0xFA  # FA, FB, FC = 20 bits para temperatura
BME280_REG_CONFIG      = 0xF5

# ============================================================================
# REGISTROS DEL MPU9250 (solo acelerómetro en este ejemplo)
# ============================================================================
MPU9250_PWR_MGMT_1     = 0x6B
MPU9250_ACCEL_CONFIG   = 0x1C
MPU9250_ACCEL_XOUT_H   = 0x3B  # 3B..40 (X, Y, Z)
MPU9250_WHO_AM_I       = 0x75

# ============================================================================
# INICIALIZACIÓN SMBus
# ============================================================================
bus = smbus2.SMBus(1)  # En Raspberry Pi, el bus I2C suele ser "1"

# ============================================================================
# FUNCIONES PARA EL BME280
# ============================================================================
def bme280_read_calibration_params():
    """
    Lee los parámetros de calibración para la temperatura (T1, T2, T3)
    según el datasheet. Retorna un diccionario con dichos valores.
    """
    calib = {}
    # Leemos 6 bytes a partir de 0x88 (donde están T1, T2, T3)
    data = bus.read_i2c_block_data(BME280_ADDRESS, BME280_REG_CALIB_START, 6)
    
    # Los registros vienen en formato little-endian
    # T1 (2 bytes, unsigned)
    calib['T1'] = data[1] << 8 | data[0]
    # T2 (2 bytes, signed)
    raw_T2 = data[3] << 8 | data[2]
    if raw_T2 & 0x8000:  # signo
        raw_T2 -= 65536
    calib['T2'] = raw_T2
    # T3 (2 bytes, signed)
    raw_T3 = data[5] << 8 | data[4]
    if raw_T3 & 0x8000:
        raw_T3 -= 65536
    calib['T3'] = raw_T3

    return calib

def bme280_init():
    """
    Configura el BME280 en modo normal, oversampling x1 para temperatura.
    """
    # 1) Verificar el ID del BME280 (opcional)
    chip_id = bus.read_byte_data(BME280_ADDRESS, BME280_REG_ID)
    if chip_id != 0x60:
        print("BME280: ¡Atención! ID inesperado: 0x{:02X}".format(chip_id))

    # 2) Configurar ctrl_meas:
    #    - OSRS_T = 001 (x1 oversampling)
    #    - OSRS_P = 001 (x1 oversampling) (aunque no lo usemos ahora)
    #    - mode = 11 (modo normal)
    #    => 0b00100111 = 0x27
    bus.write_byte_data(BME280_ADDRESS, BME280_REG_CTRL_MEAS, 0x27)

    # 3) (Opcional) Configurar "config" (filtro, stand_by, etc.)
    #    Aquí lo dejamos por defecto
    bus.write_byte_data(BME280_ADDRESS, BME280_REG_CONFIG, 0x00)

def bme280_read_temperature(calib_params):
    """
    Lee la temperatura del BME280 (ya configurado) y la compensa
    usando los parámetros de calibración. Retorna la temperatura en °C.
    """
    # Leemos los 3 bytes de temperatura: 0xFA, 0xFB, 0xFC
    data = bus.read_i2c_block_data(BME280_ADDRESS, BME280_REG_TEMP_MSB, 3)
    # 20 bits: data[0]<<12 | data[1]<<4 | data[2]>>4
    adc_T = ((data[0] << 12) | (data[1] << 4) | (data[2] >> 4)) & 0xFFFFF

    # Extraemos calibraciones
    T1 = calib_params['T1']
    T2 = calib_params['T2']
    T3 = calib_params['T3']

    # Fórmula de compensación del datasheet
    var1 = (adc_T/16384.0 - T1/1024.0)*T2
    var2 = (adc_T/131072.0 - T1/8192.0)*(adc_T/131072.0 - T1/8192.0)*T3
    t_fine = var1 + var2
    temperature = t_fine / 5120.0

    return temperature

# ============================================================================
# FUNCIONES PARA EL MPU9250
# ============================================================================
def mpu9250_init():
    """
    Despierta el MPU9250 y configura el rango del acelerómetro en ±2g.
    """
    # 1) Salir del modo sleep: escribir 0x00 en PWR_MGMT_1
    bus.write_byte_data(MPU9250_ADDRESS, MPU9250_PWR_MGMT_1, 0x00)
    time.sleep(0.1)

    # 2) Configurar el rango del acelerómetro en ±2g (ACCEL_CONFIG = 0x1C => 0x00)
    bus.write_byte_data(MPU9250_ADDRESS, MPU9250_ACCEL_CONFIG, 0x00)
    time.sleep(0.1)

    # (Opcional) Verificar WHO_AM_I
    whoami = bus.read_byte_data(MPU9250_ADDRESS, MPU9250_WHO_AM_I)
    # Para MPU9250 suele ser 0x71 o 0x73, depende de la versión
    print("MPU9250 WHO_AM_I = 0x{:02X}".format(whoami))

def mpu9250_read_accel():
    """
    Lee los valores del acelerómetro (X, Y, Z) en ±2g.
    Retorna una tupla (ax, ay, az) en g.
    """
    # Lectura de 6 bytes: ACCEL_XOUT_H..ACCEL_ZOUT_L
    data = bus.read_i2c_block_data(MPU9250_ADDRESS, MPU9250_ACCEL_XOUT_H, 6)
    # Convertir cada par de bytes a entero de 16 bits con signo
    raw_ax = (data[0] << 8) | data[1]
    raw_ay = (data[2] << 8) | data[3]
    raw_az = (data[4] << 8) | data[5]

    # Ajustar signo
    if raw_ax & 0x8000: raw_ax -= 65536
    if raw_ay & 0x8000: raw_ay -= 65536
    if raw_az & 0x8000: raw_az -= 65536

    # Escala para ±2g => 16384 LSB/g
    ax = raw_ax / 16384.0
    ay = raw_ay / 16384.0
    az = raw_az / 16384.0

    return (ax, ay, az)

# ============================================================================
# PROGRAMA PRINCIPAL
# ============================================================================
def main():
    # 1) Inicializar BME280
    bme280_init()
    calib_params = bme280_read_calibration_params()
    
    # 2) Inicializar MPU9250
    mpu9250_init()

    print("Lectura de temperatura (BME280) y aceleración (MPU9250).")
    print("Presiona Ctrl+C para salir.")

    try:
        while True:
            # Leer temperatura del BME280
            temp_c = bme280_read_temperature(calib_params)
            
            # Leer aceleraciones del MPU9250
            ax, ay, az = mpu9250_read_accel()

            print(f"Temp BME280: {temp_c:.2f} °C | Aceleración MPU9250: X={ax:.2f} g, Y={ay:.2f} g, Z={az:.2f} g")

            time.sleep(1.0)

    except KeyboardInterrupt:
        print("\nSaliendo...")

if __name__ == "__main__":
    main()
