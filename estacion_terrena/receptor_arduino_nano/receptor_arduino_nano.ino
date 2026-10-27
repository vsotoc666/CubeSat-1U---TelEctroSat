#include <SPI.h>
#include <LoRa.h>

// Pines LoRa en Arduino Nano
#define SS 10
#define RST 9
#define DIO0 2

void setup() {
    Serial.begin(115200);
    while (!Serial);
    Serial.println("Arduino Nano - Receptor LoRa");

    LoRa.setPins(SS, RST, DIO0);

    if (!LoRa.begin(433E6)) {  // Ajusta la frecuencia según la región
        Serial.println("❌ Error al iniciar LoRa!");
        while (1);
    }

    Serial.println("LoRa listo para recibir!");
}

void loop() {
    int packetSize = LoRa.parsePacket();
    if (packetSize) {
        Serial.print("📩 Mensaje recibido: ");
        while (LoRa.available()) {
            Serial.print((char)LoRa.read());
        }
        Serial.println();
    }
}