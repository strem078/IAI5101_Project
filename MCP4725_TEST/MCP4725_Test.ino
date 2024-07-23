#include <Wire.h>
#include <Adafruit_MCP4725.h>

Adafruit_MCP4725 dac;

void setup(void) {

  pinMode(0, OUTPUT);
  pinMode(1, OUTPUT);
  pinMode(2, OUTPUT);
  
  // For Adafruit MCP4725A1 the address is 0x62 (default) or 0x63 (ADDR pin tied to VCC)
  // For MCP4725A0 the address is 0x60 or 0x61
  // For MCP4725A2 the address is 0x64 or 0x65
  dac.begin(0x62);
}


void loop() {
  // put your main code here, to run repeatedly:
  int i;
  int j;
  
  for (i=0; i < 4096; i += 32){
    for (j=0; j<3; j++){
      digitalWrite(j, LOW);
      dac.setVoltage(4096*(sin(float(i-j*1365)*.001538867)+1.0)/2, false);
      digitalWrite(j, HIGH);
    }
  }
}
