import random
random.seed()

from util import BGCOLOR, STRIP_LEN, Cmd, hsvToRgb, mixRgb

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
			rgb = mixRgb(BGCOLOR, self.rgb, self.age/self.maxAge)
			return Cmd(self.x, self.y, self.x+1, self.y+1, [rgb])

	def __init__(self):
		self.objs = {}
		self.resume()

	def add(self):
		x = int(5*random.random())
		# x = 1
		y = int(STRIP_LEN*random.random())
		h = random.random()
		s = 1.0 # random.random()
		v = 255
		rgb = hsvToRgb(h, s, v)
		self.objs[(x, y)] = self.Obj(x, y, rgb)

	def resume(self):
		self.cleared = False

	def run(self):
		rnd = random.random()
		if rnd < 0.5:
			self.add()
		cmds = []
		if not self.cleared:
			self.cleared = True
			cmds.append(Cmd.setBg(BGCOLOR))
		for k, obj in self.objs.items():
			cmd = obj.run()
			if cmd is None:
				del self.objs[k]
			else:
				cmds.append(cmd)
		cmds.append(Cmd.flush(0, 5))
		return cmds
