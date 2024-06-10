import time
from util import BGCOLOR, Cmd
import bmp

class Clock:
    def __init__(self):
        self.BGCOLOR = BGCOLOR
        self.FGCOLOR = [255, 255, 0]
        self.resume()

    def resume(self):
        self.cleared = False
        self.start = time.time()
        self.lastHr = ""
        self.lastMn = ""
        self.lastCol = ""

    def run(self):
        if time.time() - self.start > 5.0:
            return "next"
        cmds = []
        if not self.cleared:
            self.cleared = True
            cmds.append(Cmd.setBg(self.BGCOLOR))

        now = time.localtime()
        hour = now.tm_hour
        minute = now.tm_min
        second = now.tm_sec
        colon = ":" if second%2 == 0 else " "
        if hour < 10:
            hour = "0" + str(hour)
        else:
            hour = str(hour)
        if minute < 10:
            minute = "0" + str(minute)
        else:
            minute = str(minute)
        if hour != self.lastHr:
            for cmd in bmp.getCmds(0, 3, hour[0], self.FGCOLOR, self.BGCOLOR):
                cmds.append(cmd)
            for cmd in bmp.getCmds(0, 7, hour[1], self.FGCOLOR, self.BGCOLOR):
                cmds.append(cmd)
            self.lastHr = hour
        if colon != self.lastCol:
            for cmd in bmp.getCmds(0, 11, colon, self.FGCOLOR, self.BGCOLOR):
                cmds.append(cmd)
            self.lastCol = colon
        if minute != self.lastMn:
            for cmd in bmp.getCmds(0, 15, minute[0], self.FGCOLOR, self.BGCOLOR):
                cmds.append(cmd)
            for cmd in bmp.getCmds(0, 19, minute[1], self.FGCOLOR, self.BGCOLOR):
                cmds.append(cmd)
            self.lastMn = minute
        if len(cmds)>0:
            cmds.append(Cmd.flush(0, 5))
        return cmds