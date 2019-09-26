#include <dht.h>

#define DHT11_PIN 7
#define temperaturePin A0
#define luminosityPin A1
dht DHT;

// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
}

// the loop routine runs over and over again forever:
void loop() {
  int chk = DHT.read11(DHT11_PIN);
  int temperatureValue = analogRead(temperaturePin);
  float cels = ((temperatureValue * 0.00488) - 0.5) / 0.01;
  int luminosityValue = analogRead(luminosityPin);
  
  Serial.print("temp=");
  Serial.print(cels);
  Serial.print(" ");
  Serial.print("lum=");
  Serial.print(luminosityValue);
  Serial.print(" ");
  Serial.print("tempDTH=");
  Serial.print(DHT.temperature);
  Serial.print(" ");
  Serial.print("humDTH=");
  Serial.print(DHT.humidity);
  Serial.println("");
  
  delay(300000);
}
