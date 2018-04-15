// Arduino for Auto PCB Maker
// Calvin Gagliano
// arduino.ino

int commands[100];
int xs[100];
int ys[100];

String readString;
int spot = 0;

void setup() {
  // put your setup code here, to run once:
  // Begin collecting information here
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:

}

void serialEvent() {
  // Get information from Python script. 
  while(!Serial.available()){}
  while(Serial.available()){
    if(Serial.available() > 0){
      readString = Serial.readString();
    }
  }
  readString += '\0';

  if(readString.length() > 0){
    // Parser
    String placeholder = "";
    
    // Get command type
    commands[spot] = readString.charAt(2) - '0';

    // Get Xcoord if it exists
    int idx = 3;
    if(readString.charAt(idx) == 'X'){
      idx++;
      while(isDigit(readString.charAt(idx)) || readString.charAt(idx) == '-'){
        placeholder = placeholder + String(readString.charAt(idx));
        idx++;
      }
      xs[spot] = placeholder.toInt();
    }

    xs[spot] = readString.charAt(4) - '0'; // Gives 4 which it should
    
    // Reset placeholder
    placeholder = "";

    // Get Ycoord if it exists
    /*if(readString.charAt(idx) == 'Y') {
      idx++;
      while(isDigit(readString.charAt(idx)) || readString.charAt(idx) == '-'){
        placeholder = placeholder + String(readString.charAt(idx));
        idx++;
      }
      ys[spot] = placeholder.toInt();
    }*/
    
    Serial.print(readString);
    Serial.print(xs[spot]);
    spot++;
    readString = "";
  }
}

