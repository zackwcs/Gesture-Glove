#include <SoftwareSerial.h>

//Constants:
const int flexPin1 = A0; //pin A0 to read analog input Index Finger
const int flexPin2 = A1; //pin A1 to read analog input Middle finger
const int flexPin3 = A2; //pin A2 to read analog input Ring finger 
const int indexpin = 2; 
const int middlepin = 3;
const int ringpin = 4;
const int pinkypin = 5;
const int touchpin1 = 12;

const int RXD = 6;
const int TXD = 7;

//Variables:
int value1, value2, value3;

//Gesture Conditions
bool idleGesture, resetGesture, reset, indexGesture, middleGesture, ringGesture, pinkyGesture, allFingersDownGesture, fingerGunGesture, indexDownGesture, middleDownGesture, ringDownGesture;
bool gestureActivated = false;

//Gesture Wait Time to Execute
unsigned long gestureDelay = 1000; 
unsigned long gestureTimer = 0;  
String gesture;


// Bluetooth Variables
String BT_data = "";

int bluetoothData;

SoftwareSerial HC05(RXD, TXD);

void setup(){
  Serial.begin(9600);       
  pinMode(indexpin, OUTPUT);
  pinMode(middlepin, OUTPUT);
  pinMode(ringpin, OUTPUT);
  pinMode(pinkypin, OUTPUT);
  pinMode(touchpin1, INPUT);
  pinMode(RXD, INPUT);
  pinMode(TXD, OUTPUT);

  HC05.begin(9600);

  
}

void loop(){

  value1 = analogRead(flexPin1);         //Read and save analog value from potentiometer
  value2 = analogRead(flexPin2);         //Read and save analog value from potentiometer
  value3 = analogRead(flexPin3);         //Read and save analog value from potentiometer
  int indexState = digitalRead(indexpin);
  int middleState = digitalRead(middlepin);
  int ringState = digitalRead(ringpin);
  int pinkyState = digitalRead(pinkypin);

  value1 = map(value1, 700, 900, 0, 200);
  value2 = map(value2, 700, 900, 0, 200);
  value3 = map(value3, 700, 900, 0, 200);
  Serial.print(value3); 
  Serial.print("\n");

  // Idle, No gestures
  idleGesture           = !indexState && !middleState && !ringState && !pinkyState && (value1 < 100) && (value2 < 100) && (value3 < 100)  && !gestureActivated;  // Idle, No gesture performed 
  
  // All gestures that executed but not released yet, Gesture Events should execute only once then stay in this state till released
  resetGesture          = (indexState || middleState || ringState || pinkyState || (value1 > 100) || (value2 > 100) && (value3 > 100)) && gestureActivated;  // Waiting for reset to Idle after a gesture
  reset                 = !indexState && !middleState && !ringState && !pinkyState && (value1 < 100) && (value2 < 100) && (value3 < 100);                     // No gestures

  // All Touch gestures with Thumb, These take precedence over all Flex Gestures
  indexGesture          = indexState  && !middleState && !ringState && !pinkyState  && !gestureActivated;                                                        // Index Finger & Thumb Touching
  middleGesture         = !indexState &&  middleState && !ringState && !pinkyState  && !gestureActivated;                                                        // Middle Finger & Thumb Touching
  ringGesture           = !indexState && !middleState &&  ringState && !pinkyState  && !gestureActivated;                                                        // Ring Finger & Thumb Touching
  pinkyGesture          = !indexState && !middleState && !ringState &&  pinkyState  && !gestureActivated;                                                        // Pinky Finger & Thumb Touching

  // ALL Flex Gestures, Only activate if No Touch gestures active 
  allFingersDownGesture = !indexState && !middleState && !ringState && !pinkyState && (value1 > 100) && (value2 > 100) && (value3 > 100)  && !gestureActivated;   // All Fingers Flexed, No fingers touching
  fingerGunGesture      = !indexState && !middleState && !ringState && !pinkyState && (value1 < 100) && (value2 > 100) && (value3 > 100)  && !gestureActivated;
  indexDownGesture      = !indexState && !middleState && !ringState && !pinkyState && (value1 > 100) && (value2 < 100) && (value3 < 100)  && !gestureActivated;   // Only Index Finger Flexed
  middleDownGesture     = !indexState && !middleState && !ringState && !pinkyState && (value1 < 100) && (value2 > 100) && (value3 < 100)  && !gestureActivated;   // Only Middle Finger Flexed
  ringDownGesture       = !indexState && !middleState && !ringState && !pinkyState && (value1 < 100) && (value2 < 100) && (value3 > 100)  && !gestureActivated;   // Only Ring Finger Flexed


  if(idleGesture) {
     //Serial.print("Idle\n");
     gestureTimer = millis();
  }
  else if(millis() - gestureTimer > 250 && !gestureActivated) {
    gestureActivated = true;
    HC05.print(gesture);
  }
  else if(gestureActivated) {
     //Serial.print("Waiting\n");
     if(reset) {
        gestureActivated = false;
     }
  }
  else if(indexGesture) {
     gesture = "Index Gesture\n";
//     gestureActivated = true;
//     HC05.print("Index Gesture\n");
  }
  else if(middleGesture) {
     gesture = "Middle Gesture\n";
//     gestureActivated = true;
//     HC05.print("Middle Gesture\n");
  }
  else if(ringGesture) {
     gesture = "Ring Gesture\n";
//     gestureActivated = true;
//     HC05.print("Ring Gesture\n");
  }
  else if(pinkyGesture) {
     gesture = "Pinky Gesture\n";
//     gestureActivated = true;
//     HC05.print("Pinky Gesture\n");
  }
    else if (fingerGunGesture) {
     gesture = "Finger Gun\n";
//     gestureActivated = true;
//     HC05.print("ALL FLEXED\n");
  }
  else if (allFingersDownGesture) {
     gesture = "ALL FLEXED\n";
//     gestureActivated = true;
//     HC05.print("ALL FLEXED\n");
  }
  else if(indexDownGesture) {
     gesture = "IndexFlexed Gesture\n";
//     gestureActivated = true;
//     HC05.print("IndexFlexed Gesture\n");
  }
  else if(middleDownGesture) {
     gesture = "MiddleFlexed Gesture\n";
//     gestureActivated = true;
//     HC05.print("MiddleFlexed Gesture\n");
  }
  else if(ringDownGesture) {
     gesture = "RingFlexed Gesture\n";
//     gestureActivated = true;
//     HC05.print("RingFlexed Gesture\n");
  }

  // bluetooth
  if (Serial.available() > 0) {
        BT_data = Serial.readStringUntil('\n');
        if (BT_data.startsWith("B:")) {
          BT_data.replace("B:", "");
          int data = BT_data.toInt();
          Serial.println(data);
        }
  }
  delay(100);                  

}
