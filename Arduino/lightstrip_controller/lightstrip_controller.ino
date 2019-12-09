#include "FastLED.h"
 
#define PIN    13
#define N_LEDS 60
CRGB leds[N_LEDS];
 
char conf[N_LEDS * 3];
int ctr = 0;

void applyConfig()
{
  for(int i = 0; i < N_LEDS; i++)
  {
    leds[i] = CRGB(conf[i*3], conf[i*3+1], conf[i*3+2]);
  }
  //strip.show();
  FastLED.show();
}

void readConfig()
{
  int available_bytes = Serial.available();
  if(available_bytes)
  {
    if(Serial.read() == 255)
    {
      // wait until full config was received
      while(Serial.available() < N_LEDS*3);
      Serial.readBytes(conf, N_LEDS*3); 
    }
  }
  /*if(!available_bytes|| available_bytes > N_LEDS*3)
  {
    Serial.flush();
    return;
  }
  if(available_bytes < N_LEDS*3)
  {
    return;
  }
  Serial.readBytes(conf, N_LEDS*3);
  Serial.println(conf);*/

  applyConfig();
}
 
void setup() {
  memset(conf, 0, sizeof(conf));
  FastLED.addLeds<NEOPIXEL, PIN>(leds, N_LEDS);
  Serial.begin(115200);
} 

void loop() {
  readConfig();
  delay(10);
}
