#include <SPI.h>
#include <LoRa.h>

#define SS 10      // LoRa Chip Select
#define RST 9      // LoRa Reset
#define DIO0 2     // LoRa DIO0

void setup() {
    Serial.begin(115200);
    while (!Serial);

    Serial.println("Initializing LoRa Receiver...");
    LoRa.setPins(SS, RST, DIO0);
    
    if (!LoRa.begin(433E6)) {
        Serial.println("LoRa initialization failed! Check connections.");
        while (1);
    }

    LoRa.setSpreadingFactor(7);
    LoRa.setSignalBandwidth(125E3);
    LoRa.setCodingRate4(5);
    LoRa.enableCrc();

    Serial.println("LoRa Receiver Initialized");
}

void loop() {
    int packetSize = LoRa.parsePacket();
    if (packetSize) {
        //Serial.print("Received GPS Coordinates: ");

        String receivedData = LoRa.readString();
        Serial.println(receivedData);

        // Serial.println(receivedData);
    }
    delay(2000);
}
