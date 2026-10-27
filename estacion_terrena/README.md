# Estación terrena

Recibe la telemetría LoRa del CubeSat y la muestra al operador.

## Receptor: Arduino Nano + SX1278

`receptor_arduino_nano/receptor_arduino_nano.ino` recibe paquetes LoRa a 433 MHz y los imprime por el puerto serie
(115200 baudios).

| SX1278 | Arduino Nano |
|--------|--------------|
| NSS    | D10          |
| RST    | D9           |
| DIO0   | D2           |
| SCK / MISO / MOSI | D13 / D12 / D11 |
| VCC    | 3.3 V        |

Necesita la librería **LoRa** de Sandeep Mistry (Gestor de librerías del Arduino IDE).

> ⚠️ **Hay que igualar los parámetros de radio con los del CubeSat.** Después de `LoRa.begin(433E6)`, agrega:
>
> ```cpp
> LoRa.setSpreadingFactor(7);
> LoRa.setSignalBandwidth(250E3);
> LoRa.setCodingRate4(5);
> LoRa.setSyncWord(0x34);
> LoRa.enableCrc();
> ```

## Visualización (`dashboard/`)

| Archivo | Descripción |
|---------|-------------|
| `dashboard_telemetria.py` | Borrador del dashboard en Dash: define las 13 variables de la misión y lee un CSV de datos. |
| `demo_grafico_dash.py` | Demo de gráfico en tiempo real con Dash/Plotly (puerto 5050). |
| `demo_grafico_extendable.py` | Demo con `dash-extendable-graph` para añadir datos sin redibujar el gráfico. |
| `visualizador_orientacion_3d.py` | Cubo 3D con PyGame + OpenGL que rota según los datos del giroscopio. |

`mqtt_cliente_prueba.py` es un cliente MQTT (paho-mqtt) que se usó para probar el envío de datos desde la Raspberry Pi
a un broker de la red local.
