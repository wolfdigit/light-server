#!/usr/bin/env python

import sys

r = 0
g = 0
b = 0

if len(sys.argv)<4:
	print("usage: "+sys.argv[0]+" r g b")
	quit()

try:
	r = int(sys.argv[1])
	g = int(sys.argv[2])
	b = int(sys.argv[3])

	import serial
	ser = serial.Serial("/dev/ttyS0", 9600)
	ser.write(bytearray([0,0, 100,0, r, g, b]))
finally:
	ser.close()
