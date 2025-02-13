////Receiver Code

char str[40];

void setup() {
  Serial.begin(9600);
  Serial1.begin(9600);
  Serial.println("Serial Read");
}

void loop() {
  int i=0;

  if (Serial1.available()) {
    delay(100); //allows all serial sent to be received together
    while(Serial1.available() && str[i]!= '\n') {
      str[i++] = Serial1.read();
    }      
    str[i++]='\0';
  }

//  else{Serial.print("w");}

  if(i>0) {
    Serial.println(str); 
//    Serial.println(i);
    
  }
  
}

//char mystr[10]; //Initialized variable to store recieved data
//
//void setup() {
//  // Begin the Serial at 9600 Baud
//  Serial.begin(9600);
//}
//
//void loop() {
//  Serial.readBytes(mystr,5); //Read the serial data and store in var
//  Serial.println(mystr); //Print data on Serial Monitor
//  delay(1000);
//}
