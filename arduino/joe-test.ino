#include <SDPArduino.h>


static const int INPUT_PIN = 0x0;

static int analogPinReading = 0;
static long count = 0;
static bool isSensing = false;


void setup() {
  // put your setup code here, to run once:
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600); // 9600 baud
  Serial.println("test");
}

void loop() {
  // put your main code here, to run repeatedly:
  analogPinReading = analogRead(INPUT_PIN);
  if (analogPinReading > 0)
    isSensing = true;
  else isSensing = false;
  Serial.print("Person active: ");
  Serial.print(isSensing);
  Serial.print(" (Analog reading: ");
  Serial.print(analogPinReading);
  Serial.println(")");

  delay(50);
  count++;  
}
