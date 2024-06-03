#include <ArduinoSTL.h>
#include <map>

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

  Serial1.begin(9600);
}

void show() {
    unsigned long now = millis();
    static unsigned long lastRun = 0;
    if (now<lastRun) lastRun = now;
    if (now - lastRun < 100) return;
    lastRun = now;

    for (int i=0; i<5; i++) {
      strips[i].show();
    }
}

uint32_t bgcolor;

typedef struct Obj {
    uint8_t srcXy[2];
    uint8_t srcRgb[3];
    uint8_t dstXy[2];
    uint8_t dstRgb[3];
    uint8_t ttl;
    uint8_t age;
} Obj;
std::map<int, Obj> objs;

void render() {
    unsigned long now = millis();
    static unsigned long lastRun = 0;
    if (now<lastRun) lastRun = now;
    if (now - lastRun < 100) return;
    lastRun = now;

    for (int i=0; i<5; i++) {
        strips[i].fill(bgcolor, 0, NLED);
    }
    for (auto &p: objs) {
        int id = p.first;
        Obj& obj = p.second;
        if (obj.age>obj.ttl) {
            objs.erase(id);
            continue;
        }
        double portion = obj.age/(double)obj.ttl;
        int x = obj.srcXy[0] + (obj.dstXy[0]-obj.srcXy[0])*portion;
        int y = obj.srcXy[1] + (obj.dstXy[1]-obj.srcXy[1])*portion;
        int r = obj.srcRgb[0] + (obj.dstRgb[0]-obj.srcRgb[0])*portion;
        int g = obj.srcRgb[1] + (obj.dstRgb[1]-obj.srcRgb[1])*portion;
        int b = obj.srcRgb[2] + (obj.dstRgb[2]-obj.srcRgb[2])*portion;
        if (x>=0 && x<5 && y>=0 && y<NLED) {
            // strips[x].setPixelColor(y, r, g, b);
            strips[x].fill(strips[x].Color(r, g, b), y*3, 3);
        }
        obj.age++;
    }
}


void loop() {
    render();
    show();

    if (Serial1.available()>0) {
        int nBytes=0;
        int buff[11];
        for (nBytes=0; nBytes<11&&Serial1.available()>0; nBytes++) {
            buff[nBytes] = Serial1.read();
            for (int wait=0; wait<20&&Serial1.available()==0; wait++) {
                delayMicroseconds(100);
            }
        }
        if (nBytes==11) {
            Obj newObj = Obj{
                {buff[0], buff[1]},
                {buff[2], buff[3], buff[4]},
                {buff[5], buff[6]},
                {buff[7], buff[8], buff[9]},
                buff[10],
                0};
            if (newObj.ttl==0 &&
                newObj.srcXy[0]==newObj.dstXy[0] &&
                newObj.srcXy[1]==newObj.dstXy[1] &&
                newObj.srcRgb[0]==newObj.dstRgb[0] &&
                newObj.srcRgb[1]==newObj.dstRgb[1] &&
                newObj.srcRgb[2]==newObj.dstRgb[2]) {
                bgcolor = strips[0].Color(newObj.srcRgb[0], newObj.srcRgb[1], newObj.srcRgb[2]);
            }
            else {
                int id = random(INT32_MAX);
                objs[id] = newObj;
            }
        }
    }
}