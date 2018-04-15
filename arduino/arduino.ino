// Arduino for Auto PCB Maker
// Calvin Gagliano
// arduino.ino

#include <Servo.h>
#include <Stepper.h>

int commands[50];
String xs[50];
String ys[50];

String readString;
int spot = 0;
int loaded = 0;

const int stepsPerRevolution = 200;  // change this to fit the number of steps per revolution
// for your motor

// Servo + Steppers
Servo servo_test; //intialize the server object
int angle = 0; //initialize angle for servo
 
// initialize the stepper library on pins 8 through 11:
Stepper StepperX(stepsPerRevolution, 8, 9, 10, 11);
Stepper StepperY(stepsPerRevolution, 4, 5, 6, 7);

void setup() {
  // put your setup code here, to run once:
  // Begin collecting information here
  Serial.begin(9600);

  StepperX.setSpeed(60);
  StepperY.setSpeed(60);

  // Sets pins for Z Linear Actuator
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);

}

void markerUp(){
  digitalWrite(2, LOW);
  digitalWrite(3, HIGH);
  delay(500);
}

void markerDown() {
  digitalWrite(2, HIGH);
  digitalWrite(3, LOW);
  delay(500);
}

void loop() {
  // put your main code here, to run repeatedly:
  // If loaded, run commands
  if(loaded == 1){
    motion();
  }
}

void movetoposition(int i){
  // Find change in position to be traveled
  int xchange, ychange;
  if(i != 0){
    xchange = xs[i].toInt() - xs[i-1].toInt();
    ychange = ys[i].toInt() - ys[i-1].toInt();
  }else{
    xchange = xs[i].toInt() / 100000;
    ychange = ys[i].toInt() / 100000;
  }

  Serial.print(String(xchange) + " " + String(ychange));
  // Move that far
  StepperX.step(xchange);
  delay(500);
  StepperY.step(ychange);
  delay(500);
}

// Interprets commands to control marker
void motion(){
  // For the # of commands
  for(int i = 0; i < spot; i++){
    // If the command is type D03 (flash)
    if(commands[i] == 3){
      // Marker up
      markerUp();
      movetoposition(i);
      // Marker down
      markerDown();
      markerUp();
      
    }
    // If the command is type D02 (travel pen up)
    if(commands[i] == 2){
      markerUp();
      movetoposition(i);
    }
    // If the command is type D01 (travel pen down)
    if(commands[i] == 1){
      markerDown();
      movetoposition(i);
    }
  }
  // stop
  loaded = 0;
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
    if(readString == "done"){
      loaded = 1;
    }else{
      // Parser
      String placeholder = "";
      
      // Get command type
      commands[spot] = readString.charAt(2) - '0';
  
      // Get Xcoord if it exists
      int idx = 3;
      if(readString.charAt(idx) == 'X'){
        idx++;
        while(isDigit(readString.charAt(idx)) || readString.charAt(idx) == '-'){
          placeholder += readString.charAt(idx);
          idx++;
        }
        xs[spot] = placeholder;
      }
  
      //xs[spot] = readString.charAt(4) - '0'; // Gives 4 which it should
      
      //Reset placeholder
      placeholder = "";
  
      // Get Ycoord if it exists
      if(readString.charAt(idx) == 'Y') {
        idx++;
        while(isDigit(readString.charAt(idx)) || readString.charAt(idx) == '-'){
          placeholder += readString.charAt(idx);
          idx++;
        }
        ys[spot] = placeholder;
      }
      Serial.print(readString);
      readString = "";
      // Up spot
      spot++;
      }
  }


}

