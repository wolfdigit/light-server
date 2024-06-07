#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif

#define NLED 72

// Parameter 1 = number of pixels in strip
// Parameter 2 = Arduino pin number (most are valid)
// Parameter 3 = pixel type flags, add together as needed:
//   NEO_KHZ800  800 KHz bitstream (most NeoPixel products w/WS2812 LEDs)
//   NEO_KHZ400  400 KHz (classic 'v1' (not v2) FLORA pixels, WS2811 drivers)
//   NEO_GRB     Pixels are wired for GRB bitstream (most NeoPixel products)
//   NEO_RGB     Pixels are wired for RGB bitstream (v1 FLORA pixels, not v2)
//   NEO_RGBW    Pixels are wired for RGBW bitstream (NeoPixel RGBW products)
Adafruit_NeoPixel strips[] = {
  Adafruit_NeoPixel(NLED,  8, NEO_GRB + NEO_KHZ800),
  Adafruit_NeoPixel(NLED,  9, NEO_GRB + NEO_KHZ800),
  Adafruit_NeoPixel(NLED, 10, NEO_GRB + NEO_KHZ800),
  Adafruit_NeoPixel(NLED, 11, NEO_GRB + NEO_KHZ800),
  Adafruit_NeoPixel(NLED, 12, NEO_GRB + NEO_KHZ800)
};

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

  for (int i=0; i<5; i++) {
    strips[i].begin();
    strips[i].setBrightness(100);
    strips[i].show(); // Initialize all pixels to 'off'
  }

  Serial1.begin(115200, SERIAL_8E1);
}

inline void waitRx() {
  for (int wait=0; wait<20&&Serial1.available()==0; wait++) {
    delayMicroseconds(100);
  }
}

inline void sendAck() {
  Serial1.write(0x06);
}

inline void drain() {
  digitalWrite(13, HIGH);
  while (Serial1.available()>0) {
    Serial1.read();
    waitRx();
  }
  sendAck();
  digitalWrite(13, LOW);
}

unsigned long cnt=0;
unsigned long lastRecv=0;
void loop() {
  cnt++;

  if (Serial1.available()>0) {
    lastRecv = cnt;
    int nBytes=0;
    int xys[2];
    for (nBytes=0; nBytes<2&&Serial1.available()>0; nBytes++) {
      xys[nBytes] = Serial1.read();
      waitRx();
    }
    if (nBytes==2) {
      int x1 = xys[0]>>5;
      int y1 = xys[0]&0x1f;
      int x2 = xys[1]>>5;
      int y2 = xys[1]&0x1f;
      if (x1<0 || x1>=5 || x2<0 || x2>5 || y1<0 || y1>=NLED || y2<0 || y2>NLED || x2<=x1 || y2<y1) {
        drain();
        return;
      }
      int len = (x2-x1)*(y2-y1);
      int buff[len*2];
      for (int i=0; i<len*2; i++) {
        if (i>=2&&buff[0]>=128) {
          buff[i] = buff[i%2];
          continue;
        }
        waitRx();
        buff[i] = Serial1.read();
        if (buff[i]==EOF) {
          drain();
          return;
        }
      }
      if (y2==y1) {
        for (int x=x1; x<x2; x++) {
          if (x>=0 && x<5) {
            strips[x].show();
          }
        }
      }
      else {
        int i=0;
        for (int x=x1; x<x2; x++) {
          for (int y=y1; y<y2; y++) {
            int rgb = ((buff[i]&0xFF)<<8) | (buff[i+1]&0xFF);
            int r = (rgb>>10)&0x1F;
            int g = (rgb>>5)&0x1F;
            int b = rgb&0x1F;
            if (x>=0 && x<5) {
              strips[x].fill(strips[x].Color(r<<1,g<<1,b<<1), y*3, 3);
            }
            i+=2;
          }
        }
      }
      sendAck();
    }
  }

  if (lastRecv>cnt) {
    lastRecv = cnt;
  }
}