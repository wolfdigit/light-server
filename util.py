STRIP_LEN = 24
BRIGHT = 0.2
BGCOLOR = [0, 24, 24]

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
	@staticmethod
	def setBg(rgb=BGCOLOR):
		return Cmd(0, 0, 5, STRIP_LEN, [rgb])

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

def mixRgb(rgb1, rgb2, alpha):
	r1, g1, b1 = rgb1
	r2, g2, b2 = rgb2
	return [
		int(r1*(1-alpha) + r2*alpha),
		int(g1*(1-alpha) + g2*alpha),
		int(b1*(1-alpha) + b2*alpha)
	]
