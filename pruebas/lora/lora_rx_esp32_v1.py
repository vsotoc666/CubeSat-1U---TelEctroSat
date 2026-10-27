#!/usr/bin/env python3
"""
Receptor LoRa para Raspberry Pi Zero 2 W
Compatible con el ESP32 transmisor de luminosidad
Usando librería LoRaRF
"""

from LoRaRF import SX127x
import time
from datetime import datetime

def setup_lora():
    """Inicializa el módulo LoRa con la misma configuración del ESP32"""
    LoRa = SX127x()
    
    print("🚀 Inicializando LoRa...")
    if not LoRa.begin():
        raise Exception("❌ No se pudo iniciar el LoRa")
    
    print("✅ LoRa iniciado correctamente")
    
    # Configuración que coincide EXACTAMENTE con el ESP32
    LoRa.setFrequency(433000000)                     # 433 MHz
    LoRa.setTxPower(20, LoRa.TX_POWER_PA_BOOST)      # Potencia +20 dBm
    LoRa.setSpreadingFactor(7)                       # SF = 7
    LoRa.setBandwidth(125000)                        # BW = 125 kHz (¡IMPORTANTE!)
    LoRa.setCodeRate(5)                              # CR = 4/5
    LoRa.setHeaderType(LoRa.HEADER_EXPLICIT)         # Encabezado explícito
    LoRa.setPreambleLength(8)                        # Preámbulo = 8
    LoRa.setCrcEnable(True)                          # CRC habilitado
    LoRa.setSyncWord(0x34)                           # SyncWord = 0x34
    
    print("📡 LoRa configurado con:")
    print(f"   Frecuencia: 433 MHz")
    print(f"   SF: 7 | BW: 125 kHz")
    print(f"   CR: 4/5 | Preámbulo: 8")
    print(f"   SyncWord: 0x34 | CRC: Habilitado")
    print(f"   RSSI: {LoRa.rssi():.1f} dBm")
    print("-" * 50)
    
    return LoRa

def parse_esp32_message(message):
    """
    Parsea mensajes del ESP32
    Formato esperado: "MSG:X,Lux:Y.YY" o "Lux:Y.YY"
    """
    try:
        message = message.strip()
        
        if "," in message:
            # Formato con contador: "MSG:X,Lux:Y.YY"
            parts = message.split(',')
            if len(parts) >= 2:
                msg_part = parts[0]  # MSG:X
                lux_part = parts[1]  # Lux:Y.YY
                
                msg_num = msg_part.split(':')[1] if ':' in msg_part else "?"
                lux_value = lux_part.split(':')[1] if ':' in lux_part else "?"
                
                return msg_num, lux_value
        else:
            # Formato simple: "Lux:Y.YY"
            if ":" in message:
                parts = message.split(':')
                if len(parts) >= 2:
                    return "?", parts[1]
        
        # Si no coincide con ningún formato esperado
        return "?", message
        
    except Exception as e:
        print(f"⚠️ Error parseando mensaje: {e}")
        return "?", message

def main():
    """Función principal del receptor"""
    print("🛰️ Receptor LoRa - CubeSat")
    print("📡 Esperando mensajes de luminosidad del ESP32...")
    print("=" * 60)
    
    # Inicializar LoRa
    try:
        LoRa = setup_lora()
    except Exception as e:
        print(f"❌ Error inicializando LoRa: {e}")
        return
    
    message_count = 0
    last_status_time = time.time()
    
    print("👂 Escuchando mensajes...")
    print("   (Presiona Ctrl+C para salir)")
    print("-" * 50)
    
    try:
        while True:
            # Verificar si hay mensajes disponibles
            if LoRa.available():
                message_count += 1
                timestamp = datetime.now().strftime("%H:%M:%S")
                
                # Leer el mensaje
                message_bytes = []
                while LoRa.available():
                    message_bytes.append(LoRa.read())
                
                try:
                    # Convertir bytes a string
                    message = bytes(message_bytes).decode('utf-8')
                    
                    # Parsear mensaje del ESP32
                    msg_num, lux_value = parse_esp32_message(message)
                    
                    # Obtener información de la señal
                    rssi = LoRa.rssi()
                    snr = LoRa.snr()
                    freq_error = LoRa.frequencyError()
                    
                    # Mostrar información del mensaje
                    print(f"📨 [{timestamp}] Mensaje #{message_count}")
                    print(f"   🔢 ESP32 Msg: #{msg_num}")
                    print(f"   💡 Luminosidad: {lux_value} lx")
                    print(f"   📶 RSSI: {rssi:.1f} dBm")
                    print(f"   📊 SNR: {snr:.1f} dB")
                    print(f"   🎯 Freq Error: {freq_error:.0f} Hz")
                    print(f"   📝 Mensaje completo: '{message}'")
                    print("-" * 40)
                    
                except UnicodeDecodeError:
                    print(f"⚠️ [{timestamp}] Mensaje con codificación inválida")
                    print(f"   📶 RSSI: {LoRa.rssi():.1f} dBm")
                    print(f"   📝 Bytes: {message_bytes}")
                    print("-" * 40)
                    
                except Exception as e:
                    print(f"❌ [{timestamp}] Error procesando mensaje: {e}")
                    print(f"   📶 RSSI: {LoRa.rssi():.1f} dBm")
                    print("-" * 40)
            
            else:
                # Sin mensajes, mostrar estado cada 30 segundos
                current_time = time.time()
                if current_time - last_status_time >= 30:
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    print(f"⏳ [{timestamp}] Esperando... | RSSI: {LoRa.rssi():.1f} dBm | Msgs: {message_count}")
                    last_status_time = current_time
                
                # Pequeña pausa para no saturar la CPU
                time.sleep(0.1)
                
    except KeyboardInterrupt:
        print("\n🛑 Deteniendo receptor...")
        print(f"📊 Estadísticas finales:")
        print(f"   Total mensajes recibidos: {message_count}")
        print(f"   RSSI final: {LoRa.rssi():.1f} dBm")
        print("👋 ¡Hasta luego!")
        
    except Exception as e:
        print(f"❌ Error en el bucle principal: {e}")
        
    finally:
        # Limpiar recursos
        try:
            LoRa.end()
        except:
            pass

if __name__ == "__main__":
    main()
