void init_lora() {
  pinMode(RFM95_RST, OUTPUT);
  digitalWrite(RFM95_RST, HIGH);

//  digitalWrite(RFM95_RST, LOW);
//  delay_millis(10);
//  digitalWrite(RFM95_RST, HIGH);
//  delay_millis(10);

  while (!rf95.init()) {
    Serial.println("LoRa radio init failed");
    while (1);
  }
  Serial.println("LoRa radio init OK!");

  if (!rf95.setFrequency(RF95_FREQ)) {
    Serial.println("setFrequency failed");
    while (1);
  }
  Serial.print("Set Freq to: ");
  Serial.println(RF95_FREQ);
  rf95.setTxPower(23, false);
}


//void send_thru_lora(char* radiopacket,int lens){
//    uint8_t payload[RH_RF95_MAX_MESSAGE_LEN];
//    int i=0;
//    
////    Serial.println((char*)radiopacket);
////    payload[0] = (uint8_t)'\0';
//    for(i=0; i<lens; i++){
//      payload[i] = (uint8_t)radiopacket[i];
//    } 
//    payload[i] = (uint8_t)'\0';
//    Serial.println((char*)payload);
//
//    delay(500);
//    
////    if (manager.sendtoWait(payload, sizeof(payload), SERVER_ADDRESS))
////    {
////      uint8_t len = sizeof(buf);
////      uint8_t from;   
////      if (manager.recvfromAckTimeout(buf, &len, 100, &from))
////      {
////          Serial.print("got reply from : 0x");
////          Serial.print(from, HEX);
////          Serial.print(": ");
////          Serial.println((char*)buf);
////      }
////    }    
////    else
////    {
////    Serial.println("No reply, is rf95_reliable_datagram_server running?");
////    }
//}


void send_thru_lora(char* radiopacket){
    rf95.setModemConfig(RH_RF95::Bw500Cr45Sf128);
    uint8_t payload[RH_RF95_MAX_MESSAGE_LEN];
    int len1 = sizeof(payload);
    int len = sizeof(radiopacket);
    int i=0;

//    payload[0] = (uint8_t)'\0';
    for(i=0; i<200; i++){
      payload[i] = (uint8_t)radiopacket[i];
    } 
    Serial.println((char*)payload);
    rf95.send(payload,sizeof(payload));
    rf95.waitPacketSent();
}


//void send_thru_lora(char* radiopacket){
//    rf95.setModemConfig(RH_RF95::Bw125Cr45Sf128);
//    uint8_t payload[RH_RF95_MAX_MESSAGE_LEN];
//    int len1 = sizeof(payload);
//    int len2 = sizeof(radiopacket);
//    int i=0;
//
//    Serial.println("Sending to rf95_server");
////    for(i=0; i<RH_RF95_MAX_MESSAGE_LEN; i++){ 
////      payload[i] = (uint8_t)'0';
////    }
//    
//    for(i=0; i<RH_RF95_MAX_MESSAGE_LEN; i++){
//      payload[i] = (uint8_t)radiopacket[i];
//    }
//
//    payload[i] = (uint8_t)'\0';
//    
//    Serial.println((char*)payload);
//    Serial.println("sending payload!");
//    rf95.send(payload, sizeof(RH_RF95_MAX_MESSAGE_LEN));
//    rf95.waitPacketSent();
////    delay(100);  
//    Serial.println("...sent!...");
//}


//////sending function is working but receive is not --- 03.07.23
//void send_thru_lora(char* radiopacket){
////    rf95.setModemConfig(RH_RF95::Bw125Cr45Sf128);
//    uint8_t payload[RH_RF95_MAX_MESSAGE_LEN];   
//    int len = sizeof(radiopacket);
//    int i=0;
//
//    payload[0] = (uint8_t)'\0';
//    for(i=0; i<RH_RF95_MAX_MESSAGE_LEN; i++){
//      payload[i] = (uint8_t)radiopacket[i];
//    }
//    payload[i] ='\0';
//    int len1 = sizeof(payload);
//    Serial.println((char*)payload);
//    rf95.send(payload,len1);
//    rf95.waitPacketSent();
////    Serial.println("...sent!...");
//}
