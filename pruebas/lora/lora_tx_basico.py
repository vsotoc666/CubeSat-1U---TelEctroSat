from LoRaRF import SX127x
import time

LoRa = SX127x()

print("Inicializando LoRa...")
if not LoRa.begin():
    raise Exception("No se pudo iniciar el LoRa")

print("LoRa iniciado correctamente")

# Configuración básica
LoRa.setFrequency(433000000)                     # Frecuencia a 433 MHz
LoRa.setTxPower(18, LoRa.TX_POWER_PA_BOOST)      # Potencia de transmisión de +17 dBm
LoRa.setSpreadingFactor(7)                       # Factor de expansión 7
LoRa.setBandwidth(250000)                        # Ancho de banda de 125 kHz
LoRa.setCodeRate(5)                              # Tasa de codificación 4/5
LoRa.setHeaderType(LoRa.HEADER_EXPLICIT)         # Modo de encabezado explícito
LoRa.setPreambleLength(8)                       # Longitud de preámbulo 12
#LoRa.setPayloadLength(15)                        # Longitud del payload 15
LoRa.setCrcEnable(True)                          # Habilitar CRC
LoRa.setSyncWord(0x34)                           # Palabra de sincronización

print("\n-- Transmisor LoRa --\n")

mensaje = "TelEctroSat beacon #"
contador = 0

# Transmitir mensaje en un bucle
while True:
    LoRa.beginPacket()
    mensaje=mensaje+str(contador)
    LoRa.write(list(mensaje.encode('utf-8')))  # Codificar mensaje a bytes
    #LoRa.write([contador])               # Añadir contador
    LoRa.endPacket()

    print(f"Mensaje enviado: {mensaje} {contador}")
    LoRa.wait()

    print("Tiempo de transmisión: {0:.2f} ms | Tasa de datos: {1:.2f} byte/s".format(LoRa.transmitTime(), LoRa.dataRate()))
    
    contador = (contador + 1) % 256
    time.sleep(5)


