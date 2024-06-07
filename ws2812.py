#!/usr/bin/env python

import random
import sys
import time
import serial
random.seed()

STRIP_LEN = 24
BRIGHT = 0.2

def hsvToRgb(h, s, v):
	if s == 0.0:
		return [v, v, v]
	i = int(h*6.0) % 6
	f = h*6.0 - i
	p = int(v*(1.0 - s))
	q = int(v*(1.0 - f*s))
	t = int(v*(1.0 - (1.0 - f)*s))
	v = int(v)
	if i == 0:
		return [v, t, p]
	if i == 1:
		return [q, v, p]
	if i == 2:
		return [p, v, t]
	if i == 3:
		return [p, q, v]
	if i == 4:
		return [t, p, v]
	if i == 5:
		return [v, p, q]


class Cmd:
	def __init__(self, x1, y1, x2, y2, rgbs):
		x1 = int(x1)
		y1 = int(y1)
		x2 = int(x2)
		y2 = int(y2)
		self.xy1 = ((min(x1, x2)&0x07)<<5) | (min(y1, y2)&0x1F)
		self.xy2 = ((max(x1, x2)&0x07)<<5) | (max(y1, y2)&0x1F)
		if len(rgbs)==1:
			self.rgbs = [
				(1)<<15 | ((rgb[0]>>3)&0x1F)<<10 | ((rgb[1]>>3)&0x1F)<<5 | ((rgb[2]>>3)&0x1F)
				for rgb in rgbs
			]
		else:
			if len(rgbs)!=abs(x1-x2)*abs(y1-y2):
				print "ERROR, rgbs length ", len(rgbs), " not", abs(x1-x2)*abs(y1-y2)
				self.xy1 = -1
			self.rgbs = [
				((rgb[0]>>3)&0x1F)<<10 | ((rgb[1]>>3)&0x1F)<<5 | ((rgb[2]>>3)&0x1F)
				for rgb in rgbs
			]
	def serialize(self):
		if self.xy1<0:
			return bytearray()
		data = [self.xy1, self.xy2]
		for rgb in self.rgbs:
			data.append((rgb>>8)&0xFF)
			data.append(rgb&0xFF)
		return bytearray(data)
	@staticmethod
	def flush(x1, x2=None):
		if x2 is None:
			x2 = x1+1
		return Cmd(x1, 0, x2, 0, [])

def mixRgb(rgb1, rgb2, alpha):
	r1, g1, b1 = rgb1
	r2, g2, b2 = rgb2
	return [
		int(r1*(1-alpha) + r2*alpha),
		int(g1*(1-alpha) + g2*alpha),
		int(b1*(1-alpha) + b2*alpha)
	]

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
			return Cmd(self.x, self.y, self.x+1, self.y+1, [rgb])

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
		if rnd < 0.3:
			self.add()
		cmds = []
		for k, obj in self.objs.items():
			cmd = obj.run()
			if cmd is None:
				del self.objs[k]
			else:
				cmds.append(cmd)
		cmds.append(Cmd.flush(0, 5))
		return cmds

# def delay():
# 	time.sleep(0.03)

def waitAck():
	for w in range(1000):
		if ser.inWaiting()>0:
			data = ser.read(ser.inWaiting())
			break

def writeSerial(buff):
	ser.write(buff)
	waitAck()

bgcolor = [0, 34, 34]
def setBg():
	for i in range(5):
		writeSerial(Cmd(i, 0, i+1, STRIP_LEN, [bgcolor]).serialize())
		writeSerial(Cmd.flush(i, i+1).serialize())

runner = RndAge()
while True:
	try:
		ser = serial.Serial("/dev/ttyS0", baudrate=115200, parity="E")
		setBg()
		prev = time.time()
		while True:
			# print("opening tmp file")
			# with open('/tmp/light', 'r') as f:
			cmds = runner.run()
			if not isinstance(cmds, list):
				time.sleep(0.1)
				continue
			print("n cmd="+str(len(cmds)))
			for cmd in cmds:
				# print(str(cmd.strip)+", "+str(cmd.start))
				# print(cmd)
				writeSerial(cmd.serialize())
			now = time.time()
			time.sleep(max(0.1-(now-prev), 0))
			prev = now
	except Exception as ex:
		print(ex)
		time.sleep(5)
