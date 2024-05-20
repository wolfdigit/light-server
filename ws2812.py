#!/usr/bin/env python

import random
import sys
import time
import serial

STRIP_LEN = 24
BRIGHT = 0.2

def hsvToRgb(h, s, v):
	if s == 0.0:
		return v, v, v
	i = int(h * 6.0)
	f = (h * 6.0) - i
	p = v * (1.0 - s)
	q = v * (1.0 - s * f)
	t = v * (1.0 - s * (1.0 - f))
	i = i % 6
	if i == 0:
		return v, t, p
	if i == 1:
		return q, v, p
	if i == 2:
		return p, v, t
	if i == 3:
		return p, q, v
	if i == 4:
		return t, p, v
	if i == 5:
		return v, p, q

class Cmd:
	pxSize = 3
	def __init__(self, strip, start, len, rgb):
		self.strip = strip
		self.start = start
		self.len = len
		self.rgb = rgb
	def serialize(self):
		return bytearray([
			self.strip,
			self.start*self.pxSize, 0,
			self.len*self.pxSize, 0,
			int(self.rgb[0]*BRIGHT), int(self.rgb[1]*BRIGHT), int(self.rgb[2]*BRIGHT)
		])
	def __str__(self):
		return str(self.strip)+","+str(self.start)+"-"+str(self.len)+": "+str(self.rgb)
class CmdHsv(Cmd):
	def __init__(self, strip, start, len, h, s, v):
		Cmd.__init__(self, strip, start, len, hsvToRgb(h, s, v))

def mixRgb(rgb1, rgb2, alpha):
	r1, g1, b1 = rgb1
	r2, g2, b2 = rgb2
	return (
		int(r1*(1-alpha) + r2*alpha),
		int(g1*(1-alpha) + g2*alpha),
		int(b1*(1-alpha) + b2*alpha)
	)

class RndAge:
	class Obj:
		maxAge = 30.0
		def __init__(self, x, y, rgb):
			self.age = self.maxAge
			self.x = x
			self.y = y
			self.rgb = rgb
		def run(self):
			self.age -= 1
			if self.age < 0:
				return None
			rgb = mixRgb(bgcolor, self.rgb, self.age/self.maxAge)
			return Cmd(self.x, self.y, 1, rgb)

	def __init__(self):
		self.objs = {}

	def add(self):
		x = int(5*random.random())
		# x = 1
		y = int(STRIP_LEN*random.random())
		h = random.random()
		s = 1.0 # random.random()
		v = 255
		rgb = hsvToRgb(h, s, v)
		self.objs[(x, y)] = self.Obj(x, y, rgb)

	def run(self):
		rnd = random.random()
		#if rnd < 0.05:
		if rnd < 1.0:
			self.add()
		cmds = []
		for k, obj in self.objs.items():
			cmd = obj.run()
			if cmd is None:
				del self.objs[k]
			else:
				cmds.append(cmd)
		return cmds

def delay():
	time.sleep(0.03)

bgcolor = (0, 34, 34)
def setBg():
	with serial.Serial("/dev/ttyS0", 9600) as ser:
		for i in range(5):
			ser.write(Cmd(i, 0, STRIP_LEN, bgcolor).serialize())
			delay()

setBg()
rndAge = RndAge()
while True:
	time.sleep(5)
	try:
		ser = serial.Serial("/dev/ttyS0", 9600)
		while True:
			# print("opening tmp file")
			# with open('/tmp/light', 'r') as f:
			cmds = rndAge.run()
			print("n cmd="+str(len(cmds)))
			for cmd in cmds:
				# print(str(cmd.strip)+", "+str(cmd.start))
				print(cmd)
				ser.write(cmd.serialize())
				delay()
			time.sleep(0.1)
	except Exception as ex:
		print(ex)
		None
