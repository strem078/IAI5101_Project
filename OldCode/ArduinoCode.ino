#define Pm1_In A0   //meter 1 reads from A0 (px)
#define Pm2_In A1   //meter 2 reads from A1  (py)
#define Pin1 11     //PWM output on pin 11 to adjust the input voltage
#define Pin2 10     //PWM output on pin 10 to adjust the input voltage

uint16_t outputVoltage1 = 0;
uint16_t outputVoltage2 = 0;

uint16_t Pm1_In_vals[255];    //array to hold the ouput values from the power meter px
uint16_t Pm2_In_vals[255];    //array to hold the ouput values from the power meter py
uint16_t output_vals[255];
uint16_t Pj2_vals[255];
int ref[255];

uint16_t i;
uint16_t j;


void setup() {
  
  pinMode(Pm1_In, INPUT);
  pinMode(Pm2_In, INPUT);
  pinMode(Pin1, OUTPUT);
  pinMode(Pin2, OUTPUT);
  pinMode(11, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(9, OUTPUT);
  pinMode(6, OUTPUT);
  Serial.begin(9600);        //start the serial port to talk to the computer
  

}

void loop() {

  delay(2000);

  analogWrite(10,0);
  analogWrite(11,0);
  analogWrite(9,0);
  analogWrite(6,0);

  for(i=200;i<202;i++) {
    analogWrite(Pin1, outputVoltage1);

    for(j=0;j<255;j++) {
      analogWrite(Pin2, outputVoltage2);

      delay(2000); // Delay for the signal to stabilize
      Pm1_In_vals[j] = analogRead(Pm1_In);
      Pm2_In_vals[j] = analogRead(Pm2_In);
      output_vals[j] = outputVoltage2;
      Pj2_vals[j] = Pm2_In_vals[j];

      
      bool negative;
      float tempTop;
      float tempBot;
      float tempOp;
      int tTop;
    
      if (j == 0)
        tTop = 0;  
      else
        tTop =   Pm1_In_vals[j] - Pm1_In_vals[j-1];

      ref[j]=tTop;
    
      Serial.print(outputVoltage1);
      Serial.print(", ");
      Serial.print(outputVoltage2);
      Serial.print(", ");
      Serial.print(Pm1_In_vals[j]);
      Serial.print(", ");
      Serial.print(Pm2_In_vals[j]);
      Serial.print(", ");
      tempTop = (float)(Pm1_In_vals[j]) - (Pm2_In_vals[j]);
      tempBot = (float)(Pm1_In_vals[j]) + (Pm2_In_vals[j]);
      tempOp = tempTop/tempBot;
      
      Serial.print(tempOp,4); 
      Serial.print(", ");
      Serial.println(ref[j]);
      

      //if  ( ref[j] <= -30 && ref[j] >=-65)
      // { while(1);
      //
      // }
      outputVoltage2=j;
      outputVoltage1=i;
    }
  }

  while(1) {}

}