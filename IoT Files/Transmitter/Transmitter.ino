#include <SPI.h>
#include <LoRa.h>
#include <SoftwareSerial.h>
#include <TinyGPS++.h>

#define SS 10      // LoRa Chip Select
#define RST 9      // LoRa Reset
#define DIO0 2     // LoRa DIO0

static const int RXPin = 4, TXPin = 3;  // GPS TX -> Pin 4, RX -> Pin 3
static const uint32_t GPSBaud = 9600;

TinyGPSPlus gps;
SoftwareSerial gpsSerial(RXPin, TXPin);

void setup() {
    Serial.begin(115200);
    gpsSerial.begin(GPSBaud);

    Serial.println("Initializing LoRa Transmitter...");
    LoRa.setPins(SS, RST, DIO0);
    
    if (!LoRa.begin(433E6)) {
        Serial.println("LoRa initialization failed! Check connections.");
        while (1);
    }

    LoRa.setSpreadingFactor(7);
    LoRa.setSignalBandwidth(125E3);
    LoRa.setCodingRate4(5);
    LoRa.enableCrc();

    Serial.println("LoRa Transmitter Initialized");
}

void loop() {

    while (gpsSerial.available()) {
        gps.encode(gpsSerial.read());

        if (gps.location.isUpdated()) {
            float latitude = gps.location.lat();
            float longitude = gps.location.lng();

            LoRa.beginPacket();
            LoRa.print(latitude, 6);
            LoRa.print(",");
            LoRa.print(longitude, 6);
            LoRa.endPacket();

            delay(2000);
        }
    }
}