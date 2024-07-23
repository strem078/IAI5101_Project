const int PWM_CHANNEL = 0;    // ESP32 has 16 channels which can generate 16 independent waveforms
const int PWM_FREQ = 1000;     // Recall that Arduino Uno is ~490 Hz. Official ESP32 example uses 5,000Hz
const int PWM_RESOLUTION = 8; // We'll use same resolution as Uno (8 bits, 0-255) but ESP32 can go up to 16 bits 

// The max duty cycle value based on PWM resolution (will be 255 if resolution is 8 bits)
const int MAX_DUTY_CYCLE = (int)(pow(2, PWM_RESOLUTION) - 1); 

const int PWM_chan0 = 15;
const int PWM_chan1 = 16;
const int PWM_chan2 = 17;
const int PWM_chan3 = 18;

const int DELAY_MS = 10;  // delay between fade increments

void setup() {

  // Sets up a channel (0-15), a PWM duty cycle frequency, and a PWM resolution (1 - 16 bits) 
  // ledcSetup(uint8_t channel, double freq, uint8_t resolution_bits);
  ledcSetup(0, PWM_FREQ, PWM_RESOLUTION);
  ledcSetup(1, PWM_FREQ, PWM_RESOLUTION);
  ledcSetup(2, PWM_FREQ, PWM_RESOLUTION);
  ledcSetup(3, PWM_FREQ, PWM_RESOLUTION);

  // ledcAttachPin(uint8_t pin, uint8_t channel);
  ledcAttachPin(PWM_chan0, 0);
  ledcAttachPin(PWM_chan1, 1);
  ledcAttachPin(PWM_chan2, 2);
  ledcAttachPin(PWM_chan3, 3);
}

void loop() {
  int dutyCycles[] = {0,0,0,0};
  int dirFlags[] = {1,1,1,1}; // Direction of wave, -1 or 1
  
  while (1){
    for(int i = 0; i < 4; i++){
      if(dutyCycles[i] + dirFlags[i]*(i+1)*10 > MAX_DUTY_CYCLE || dutyCycles[i] + dirFlags[i]*(i+1)*10 < 0){ dirFlags[i] *= -1; }
      dutyCycles[i] += dirFlags[i]*(i+1)*10;
      ledcWrite(i, dutyCycles[i]);
    }
    delay(DELAY_MS);
  }
}
