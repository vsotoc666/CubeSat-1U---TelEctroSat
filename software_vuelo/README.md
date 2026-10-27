# Software de vuelo

Código que se ejecuta en la Raspberry Pi Zero 2 W del CubeSat durante la misión.

```bash
cd software_vuelo
python3 main_vuelo.py
```

| Archivo | Descripción |
|---------|-------------|
| `main_vuelo.py` | Programa principal. Inicializa el enlace LoRa y los sensores, transmite la telemetría en CSV cada ~0.25 s y acciona el relé del paracaídas según la altitud. |
| `sensores/sensor_bme280.py` | Temperatura, presión y humedad (BME280, I²C `0x76`). |
| `sensores/sensor_uv_guva.py` | Radiación UV (GUVA-S12SD a través del ADC ADS1115, canal A0). |
| `sensores/sensor_imu_mpu9250.py` | Acelerómetro y giroscopio (MPU9250, I²C `0x68`), con calibración de offset al arrancar. |
| `sensores/sensor_gps.py` | Latitud, longitud y altitud desde tramas NMEA `$GPGGA` (NEO-6M, `/dev/ttyUSB0`). |
| `sensores/actuador_rele.py` | Control del relé que libera el paracaídas (GPIO 20). |

Cada módulo de `sensores/` puede ejecutarse por separado para probar el sensor, por ejemplo:
`python3 -m sensores.sensor_bme280`.

## Versiones anteriores

`versiones_anteriores/` guarda las iteraciones del transmisor como registro del desarrollo:

| Archivo | Estado |
|---------|--------|
| `transmisor_v0_borrador.py` | Borrador incompleto (no ejecuta). |
| `transmisor_v1.py` | Primera integración BME280 + GUVA + MPU9250 (tiene un error de sintaxis sin corregir). |
| `transmisor_v2_gps.py` | Agrega el GPS. La lógica del relé está comentada. |

`main_vuelo.py` es la versión final (v3).
