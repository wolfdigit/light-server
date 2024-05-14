#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif

#define PIN 12
#define NLED 100

// Parameter 1 = number of pixels in strip
// Parameter 2 = Arduino pin number (most are valid)
// Parameter 3 = pixel type flags, add together as needed:
//   NEO_KHZ800  800 KHz bitstream (most NeoPixel products w/WS2812 LEDs)
//   NEO_KHZ400  400 KHz (classic 'v1' (not v2) FLORA pixels, WS2811 drivers)
//   NEO_GRB     Pixels are wired for GRB bitstream (most NeoPixel products)
//   NEO_RGB     Pixels are wired for RGB bitstream (v1 FLORA pixels, not v2)
//   NEO_RGBW    Pixels are wired for RGBW bitstream (NeoPixel RGBW products)
Adafruit_NeoPixel strip = Adafruit_NeoPixel(NLED, PIN, NEO_GRB + NEO_KHZ800);

// IMPORTANT: To reduce NeoPixel burnout risk, add 1000 uF capacitor across
// pixel power leads, add 300 - 500 Ohm resistor on first pixel's data input
// and minimize distance between Arduino and first pixel.  Avoid connecting
// on a live circuit...if you must, connect GND first.

void setup() {
  // This is for Trinket 5V 16MHz, you can remove these three lines if you are not using a Trinket
  #if defined (__AVR_ATtiny85__)
    if (F_CPU == 16000000) clock_prescale_set(clock_div_1);
  #endif
  // End of trinket special code

  strip.begin();
  strip.setBrightness(100);
  strip.show(); // Initialize all pixels to 'off'

  Serial1.begin(9600);
}

int cnt=0;
void loop() {
  // Some example procedures showing how to display to the pixels:
  //colorWipe(strip.Color(255, 0, 0), 50); // Red
  //for (int i=0; i<strip.numPixels(); i++) {
  //  strip.setPixelColor(i, strip.ColorHSV(i*6553.5));
  //}
  //strip.setPixelColor(0, strip.ColorHSV(cnt*13107));
  //strip.setPixelColor(strip.numPixels()-1, strip.Color(255,0,0,(cnt*51)&255));
  //strip.fill(strip.ColorHSV(cnt*300));
  //strip.setPixelColor(0, strip.ColorHSV(cnt*30));
  //strip.show();
  //cnt++;
  //delay(30);

  if (Serial1.available()>0) {
    int nBytes;
    int buff[7];
    for (nBytes=0; nBytes<7&&Serial1.available()>0; nBytes++) {
      buff[nBytes] = Serial1.read();
      delayMicroseconds(1500);
    }
    //for (int i=0; i<4; i++) {
    //  if (i<nBytes) strip.setPixelColor(i*2+1, strip.ColorHSV(i*20000));
    //  else          strip.setPixelColor(i*2+1, 0);
    //}
    /*
    if (nBytes==4) {
      strip.setPixelColor(4, 0, 255, 0);
    }
    else {
      strip.setPixelColor(4, 255, 0, 0);
    }
    strip.show();
    */

    // 2B:first, 2B:count, 3B:RGB
    if (nBytes==7) {
      uint16_t first = (buff[0]&0xFF) | ((buff[1]&0xFF)<<8);
      uint16_t count = (buff[2]&0xFF) | ((buff[3]&0xFF)<<8);
      if (first>=NLED) return;
      if (first+count>NLED) count=NLED-first;
      /*
      if (buff[0]==255) {
        strip.fill(strip.Color(buff[1], buff[2], buff[3]));
      }
      else {
        strip.setPixelColor(buff[0], buff[1], buff[2], buff[3]);
      }
      */
      strip.fill(strip.Color(buff[4], buff[6], buff[5]), first, count);
      strip.show();
    }
    
  }
  //delay(4);
  
}
