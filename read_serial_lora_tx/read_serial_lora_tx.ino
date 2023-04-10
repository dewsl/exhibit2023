#include <Wire.h>
#include <LowPower.h>
#include "Sodaq_DS3231.h"
#include <SPI.h>
#include <RH_RF95.h>
#include <avr/dtostrf.h>      // dtostrf missing in Arduino Zero/Due
#include <EnableInterrupt.h>
#include <FlashStorage.h>
#include <Arduino.h>         // required before wiring_private.h
#include "wiring_private.h"  // pinPeripheral() function
#include <string.h>
#include <Adafruit_SleepyDog.h>
#include <RHReliableDatagram.h>

#define BAUDRATE 115200
#define DUEBAUD 9600
#define DUESerial Serial1
#define DUETRIG 5

// for m0
#define RFM95_CS 8
#define RFM95_RST 4
#define RFM95_INT 3
#define RF95_FREQ 433.0 

//#define CLIENT_ADDRESS 1
//#define SERVER_ADDRESS 2

// Singleton instance of the radio driver
RH_RF95 rf95(RFM95_CS, RFM95_INT);
//RHReliableDatagram manager(rf95, SERVER_ADDRESS);
//uint8_t buf[RH_RF95_MAX_MESSAGE_LEN];

///* Pin 11-Rx ; 10-Tx (GSM comms) */
//Uart Serial2(&sercom1, 11, 10, SERCOM_RX_PAD_0, UART_TX_PAD_2);
//void SERCOM1_Handler() {
//  Serial2.IrqHandler();
//}
  
void setup()
{
  Serial.begin(BAUDRATE);
  Serial1.begin(DUEBAUD);
  DUESerial.begin(DUEBAUD);

  /* Assign pins 10 & 11 UART SERCOM functionality */
  pinPeripheral(10, PIO_SERCOM);
  pinPeripheral(11, PIO_SERCOM);

  Wire.begin();
  init_lora();
//  if (!manager.init())
//    Serial.println("init manager failed");

  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(DUETRIG, OUTPUT);

  digitalWrite(LED_BUILTIN, HIGH);
  digitalWrite(DUETRIG, HIGH);
  turn_ON_due();
}

void turn_ON_due()
{
  Serial.println("Turning ON Custom Due. . .");
  digitalWrite(DUETRIG, HIGH);
}

//void turn_OFF_due()
//{
//  Serial.println("Turning OFF Custom Due. . .");
//  digitalWrite(DUETRIG, LOW);
//}

void delay_millis(int _delay) {
  uint8_t delay_turn_on_flag = 0;
  unsigned long _delayStart = millis();
  do {
    if ((millis() - _delayStart) > _delay) {
      _delayStart = millis();
      delay_turn_on_flag = 1;
    }
  } while (delay_turn_on_flag == 0);
}

//char dataToSend[150];
//char sensorData[107];
//char sitename[] = "BADTA:";

//void loop(){
//    
//    while(Serial1.available()){
//      char inByte = Serial1.read();
//      
//      if (inByte == '>'){
//        Serial.println("Found >");
//        Serial1.readBytesUntil('<', sensorData, sizeof(sensorData));
//        strncpy(dataToSend,sitename,7);
//        strncat(dataToSend, sensorData, sizeof(sensorData));
//        send_thru_lora(dataToSend,strlen(dataToSend));
//      }
//    }
//}
//
//void clear_data(){
//  for(int i = 0; i<150; i++){
//    dataToSend[i] = '\0';
//  }
//}



bool started = false;
bool ended = false;
byte ind;
char dataToSend[150];
char sensorData[107];
char sitename[] = "PADTA:";

void loop(){

    while(Serial1.available()) {
      char inByte = Serial1.read();
      
      if (inByte == '>') {
//        Serial.println("> start found");
        ind = 0;
        sensorData[ind] = '\0';
        started = true;
        ended = false;
      }
      else if (inByte == '<') {
//        Serial.println("< end found");
        ended = true;
        break;
      }
      else {
        if (ind < 105) {
          sensorData[ind] = inByte;
          strncpy(dataToSend,sitename,7);
          strncat(dataToSend, sensorData, sizeof(sensorData));
          ind++;
          sensorData[ind] = '\0';
//          dataToSend[ind] = '\0';
        }
      }
    }

    if(started && ended){  
      started = false;
      ended = false;
      ind = 0;
//      sensorData[ind] = '\0';
//      Serial.println(dataToSend); 
      send_thru_lora(dataToSend);
      dataToSend[ind] = '\0';  
    }  
} 
