#!/usr/bin/env python

import sys
import time
import serial

r0, g0, b0 = (255, 255, 255)
while True:
	time.sleep(5)
	try:
		ser = serial.Serial("/dev/ttyS0", 9600)
		while True:
			with open('/tmp/rgb', 'r') as f:
				r, g, b = [int(x) for x in f.read().split()]
				with open('/tmp/rgb_out', 'w') as f2:
					f2.write(str([r,g,b]))
				if r!=r0 or g!=g0 or b!=b0:
					ser.write(bytearray([0,0, 100,0, r, g, b]))
					r0, g0, b0 = (r, g, b)
				time.sleep(0.5)
	except:
		None
