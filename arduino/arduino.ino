String readString;

void setup() {
  // put your setup code here, to run once:
  // Begin collecting information here
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:

}

void serialEvent() {
  while(!Serial.available()){}
  while(Serial.available()){
    if(Serial.available() > 0){
      char c = Serial.read();
      readString += c; 
    }
  }

  if(readString.length() > 0){
    Serial.print(readString);
    readString = "";
  }
}

