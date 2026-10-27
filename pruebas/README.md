# Pruebas de componentes

Scripts exploratorios que se usaron para validar cada componente por separado antes de integrarlo al software de
vuelo. Se conservan como registro del proceso de desarrollo. Varios son variantes de la misma prueba.

| Carpeta | Qué se probó |
|---------|--------------|
| `lora/` | Módulo SX1278: acceso directo por SPI a los registros, librerías **LoRaRF** y **pySX127x**, transmisión de beacons, recepción desde un ESP32 y diagnóstico del enlace (`lora_diagnostico.py`). |
| `imu/` | MPU9250/MPU6500: lectura con `smbus` y con `mpu9250-jmdev`, verificación del registro `WHO_AM_I`, calibración de offsets y diagnóstico del magnetómetro AK8963. |
| `bme280/` | Lectura del BME280 con la librería `bme280` y a nivel de registros. |
| `gps/` | NEO-6M: lectura NMEA en crudo, parsers de `$GPGGA`/`$GPRMC` y altitud corregida con presión barométrica. |
| `uv_voltaje/` | GUVA-S12SD y medición de voltaje de batería con el ADS1115. |
| `rele/` | Activación del relé del paracaídas (GPIO 20 y GPIO 16). |
| `gpio/` | Parpadeo de LEDs para verificar los GPIO. |
| `dht11/` | Sensor DHT11 con `pigpio` (alternativa evaluada al inicio). |
| `adquisicion_datos/` | Registradores que guardan IMU + temperatura en CSV (los datos resultantes están en `../datos/`). |

## Librerías LoRa

- **LoRaRF** (`pip install LoRaRF`): la usa el software de vuelo.
- **pySX127x** ([rpsreal/pySX127x](https://github.com/rpsreal/pySX127x)): la usan los scripts `pysx127x_*.py`. Hay
  que clonar el repositorio y ejecutar los scripts con la carpeta `SX127x/` en el `PYTHONPATH`.
