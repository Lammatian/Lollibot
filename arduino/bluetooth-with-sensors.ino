#include <SoftwareSerial.h>
#define Rx 5
#define Tx 6
#define BAUD_RATE 9600

static int pedestrian1Reading = 0;
static int pedestrian2Reading = 0;
static int traffic1Reading = 0;
static int traffic2Reading = 0;
static const int INPUT_PIN = 0x0;
int state = 0;
String pinInfo = "";

SoftwareSerial mySerial(Rx, Tx);

void setup() {
//    pinMode(LED_BUILTIN, OUTPUT);
    /*pinMode(A0, INPUT);
    pinMode(A1, INPUT);
    pinMode(A2, INPUT);
    pinMode(A3, INPUT);*/
    Serial.begin(BAUD_RATE);
    Serial.println("Starting");

    mySerial.begin(BAUD_RATE);
    Serial.println("Starting bluetooth");  
}

void loop() {
    pinInfo = "";
    
    if (mySerial.available()) { // Checks whether data is coming from the serial port
        Serial.println("Available data"); 
        Serial.println(mySerial.readString()); // Reads and prints the data from the serial port
    }

    delay(300);

    pedestrian1Reading = analogRead(0);
    delay(100);
    pedestrian2Reading = analogRead(1);
    delay(100);
    traffic1Reading = analogRead(2);
    delay(100);
    traffic2Reading = analogRead(3);
    delay(100);
    
    if (pedestrian1Reading > 0) {
        pinInfo += String(pedestrian1Reading) + "|";
    } 
    if (pedestrian2Reading > 0) {
        pinInfo += String(pedestrian2Reading) + "|";
    } 
    if (traffic1Reading > 0) {
        pinInfo += String(traffic1Reading) + "|";
    }
    if (traffic2Reading > 0) {
        pinInfo += String(traffic2Reading);
    }

    Serial.println("Pins: " + pinInfo);
    char message[pinInfo.length() + 2];
    int len = pinInfo.length();
    pinInfo.toCharArray(message, pinInfo.length() + 1);
    message[pinInfo.length() + 1] = '\0';
    mySerial.write(message);

    delay(300);
}
