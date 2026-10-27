#!/usr/bin/env python3
"""
Diagnóstico LoRa - Verifica configuración y conexión
"""

from LoRaRF import SX127x
import time

def test_lora_config():
    """Prueba la configuración del módulo LoRa"""
    print("🔍 DIAGNÓSTICO LORA")
    print("=" * 50)
    
    try:
        LoRa = SX127x()
        
        print("1️⃣ Inicializando módulo...")
        if not LoRa.begin():
            print("❌ FALLO: No se pudo inicializar el módulo")
            print("   Verifica las conexiones físicas:")
            print("   - VCC -> 3.3V")
            print("   - GND -> GND") 
            print("   - SCK, MISO, MOSI, CS, RST")
            return False
        
        print("✅ Módulo inicializado correctamente")
        
        print("\n2️⃣ Configurando parámetros...")
        LoRa.setFrequency(433000000)
        LoRa.setSpreadingFactor(7)
        LoRa.setBandwidth(125000)
        LoRa.setCodeRate(5)
        LoRa.setPreambleLength(8)
        LoRa.setCrcEnable(True)
        LoRa.setSyncWord(0x34)
        
        print("✅ Configuración aplicada")
        
        print("\n3️⃣ Verificando configuración actual...")
        print(f"   Frecuencia: {LoRa.getFrequency()/1000000:.1f} MHz")
        print(f"   SF: {LoRa.getSpreadingFactor()}")
        print(f"   BW: {LoRa.getBandwidth()/1000:.0f} kHz")
        print(f"   CR: 4/{LoRa.getCodeRate()}")
        print(f"   Preámbulo: {LoRa.getPreambleLength()}")
        print(f"   SyncWord: 0x{LoRa.getSyncWord():02X}")
        print(f"   CRC: {'Habilitado' if LoRa.getCrcEnable() else 'Deshabilitado'}")
        
        print("\n4️⃣ Probando recepción durante 30 segundos...")
        print("   (Enciende tu ESP32 ahora)")
        
        start_time = time.time()
        message_count = 0
        valid_messages = 0
        
        while time.time() - start_time < 30:
            if LoRa.available():
                message_count += 1
                rssi = LoRa.rssi()
                snr = LoRa.snr()
                
                # Leer mensaje
                message_bytes = []
                while LoRa.available():
                    message_bytes.append(LoRa.read())
                
                print(f"\n📡 Mensaje #{message_count}")
                print(f"   📶 RSSI: {rssi:.1f} dBm")
                print(f"   📊 SNR: {snr:.1f} dB")
                print(f"   📏 Longitud: {len(message_bytes)} bytes")
                
                if rssi > -120:  # Señal razonable
                    try:
                        message = bytes(message_bytes).decode('utf-8')
                        if message.isprintable():
                            valid_messages += 1
                            print(f"   ✅ Mensaje válido: '{message}'")
                        else:
                            print(f"   ⚠️ Caracteres no imprimibles")
                    except:
                        print(f"   ⚠️ Error de decodificación")
                        print(f"   📝 Hex: {' '.join(f'{b:02x}' for b in message_bytes[:10])}...")
                else:
                    print(f"   🔇 Señal muy débil (ruido)")
            
            time.sleep(0.1)
        
        print(f"\n📊 RESUMEN DE PRUEBA:")
        print(f"   Total mensajes detectados: {message_count}")
        print(f"   Mensajes válidos: {valid_messages}")
        print(f"   RSSI actual: {LoRa.rssi():.1f} dBm")
        
        if valid_messages > 0:
            print("✅ COMUNICACIÓN EXITOSA")
        elif message_count > 0:
            print("⚠️ DETECTA SEÑALES PERO HAY INTERFERENCIA/RUIDO")
            print("   Sugerencias:")
            print("   - Verifica que ESP32 y RPi tengan la misma configuración")
            print("   - Acerca los dispositivos")
            print("   - Verifica las antenas")
        else:
            print("❌ NO SE DETECTAN SEÑALES")
            print("   Sugerencias:")
            print("   - Verifica que el ESP32 esté transmitiendo")
            print("   - Acerca los dispositivos")
            print("   - Verifica frecuencia (433 MHz)")
            print("   - Revisa conexiones físicas")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False
    
    finally:
        try:
            LoRa.end()
        except:
            pass

if __name__ == "__main__":
    test_lora_config()
