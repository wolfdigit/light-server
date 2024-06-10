import bmp
from util import BGCOLOR, STRIP_LEN, Cmd

class Word:
    def __init__(self, words):
        params = words[0].split(",")
        words = ' '.join(words[1:])
        self.map = ["", "", "", "", ""]
        for ch in words:
            chMap = bmp.getMap(ch)
            for i in range(5):
                self.map[i] += chMap[i]
                self.map[i] += " "
        print(self.map)

        self.pos = -STRIP_LEN
        self.FGCOLOR = [255, 255, 0]
        self.BGCOLOR = BGCOLOR
        self.times = -1
        self.duration = 3
        self.counter = 0

        # word color=FF00CC,bgcolor=030303,times=1 asdf
        for param in params:
            if param.startswith("color="):
                self.FGCOLOR = [
                    int(param[6:8], 16),
                    int(param[8:10], 16),
                    int(param[10:12], 16),
                ]
            if param.startswith("bgcolor="):
                self.BGCOLOR = [
                    int(param[8:10], 16),
                    int(param[10:12], 16),
                    int(param[12:14], 16),
                ]
            if param.startswith("times="):
                self.times = int(param[6:], 10)

    def move(self):
        if self.pos >= len(self.map[0]):
            self.pos = -STRIP_LEN
            if self.times > 0:
                self.times -= 1
            return
        self.pos += 1

    def render(self):
        def getPx(x, y):
            if y<0:
                return 0
            if y>=len(self.map[x]):
                return 0
            if self.map[x][y] == " ":
                return 0
            return 1
        if self.times==0:
            return "rndAge"
        cmds = []
        for x in range(5):
            yStart = 0
            while yStart<STRIP_LEN:
                yEnd = yStart+1
                while yEnd<STRIP_LEN and getPx(x, yEnd+self.pos) == getPx(x, yStart+self.pos):
                    yEnd += 1
                cmds.append(Cmd(x, yStart, x+1, yEnd, [self.FGCOLOR if getPx(x,yStart+self.pos)==1 else self.BGCOLOR]))
                yStart = yEnd
            cmds.append(Cmd.flush(x, x+1))
        return cmds

    def run(self):
        if self.counter%self.duration==0:
            self.counter += 1
            self.move()
            return self.render()
        else:
            self.counter += 1
            return []
