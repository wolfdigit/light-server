#!/usr/bin/env python

import sys

r = 0
g = 0
b = 0
l = 1

if len(sys.argv)<7:
	print("usage: "+sys.argv[0]+" x y l r g b")
	quit()

try:
	x = int(sys.argv[1])
	y = int(sys.argv[2])
	r = int(sys.argv[3])
	g = int(sys.argv[4])
	b = int(sys.argv[5])
	xx = int(sys.argv[6])
	yy = int(sys.argv[7])
	rr = int(sys.argv[8])
	gg = int(sys.argv[9])
	bb = int(sys.argv[10])
	l = int(sys.argv[11])

	import serial
	ser = serial.Serial("/dev/ttyS0", 9600)
	data = bytearray([x, y, r, g, b, xx, yy, rr, gg, bb, l])
	# ser.write(bytearray([x, y, l, r, g, b]))
	ser.write(data)
	print([hex(b) for b in data])
	# ser.write(bytearray([x, 0, 0, 0, 0, 0]))
except Exception as ex:
	print(ex)
finally:
	ser.close()
