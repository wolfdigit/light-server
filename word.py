from util import BGCOLOR, STRIP_LEN, Cmd

picUpper = [
"000,000,000,00 ,000,000,000,0 0,000,  0,"+"0 0,0  ,000,000,000,000,000,000, 00,000,"+"0 0,0 0,0 0,0 0,0 0,000,",
"0 0,0 0,0  ,0 0,0  ,0  ,0  ,0 0, 0 ,  0,"+"0 0,0  ,000,0 0,0 0,0 0,0 0,0 0,0  , 0 ,"+"0 0,0 0,0 0,0 0,0 0,  0,",
"000,00 ,0  ,0 0,00 ,00 ,0 0,000, 0 ,  0,"+"00 ,0  ,0 0,0 0,0 0,000,0 0,00 , 0 , 0 ,"+"0 0,0 0,0 0, 0 ,000, 0 ,",
"0 0,0 0,0  ,0 0,0  ,0  ,0 0,0 0, 0 ,0 0,"+"0 0,0  ,0 0,0 0,0 0,0  ,000,0 0,  0, 0 ,"+"0 0,0 0,000,0 0, 0 ,0  ,",
"0 0,000,000,00 ,000,0  ,000,0 0,000,000,"+"0 0,000,0 0,0 0,000,0  ,000,0 0,00 , 0 ,"+"000, 0 ,000,0 0, 0 ,000,",
]
picLower = [
"   ,0  ,   ,  0,   ,  0,   ,0  , 0 ,  0,"+"0  , 0 ,   ,   ,   ,   ,   ,   ,   , 0 ,"+"   ,   ,   ,   ,   ,   ,",
"   ,0  ,   ,  0,   , 0 ,000,0  ,   ,   ,"+"0  , 0 ,   ,   ,   ,000,000,   ,   ,000,"+"   ,   ,   ,   ,0 0,   ,",
" 00,00 ,000, 00, 0 ,000,000,000, 0 ,  0,"+"0 0, 0 ,00 ,00 ,000,0 0,0 0,000, 00, 0 ,"+"0 0,0 0,0 0,0 0,000,00 ,",
"0 0,0 0,0  ,0 0,000, 0 ,  0,0 0, 0 ,0 0,"+"00 , 0 ,000,0 0,0 0,000,000,0  , 0 , 0 ,"+"0 0,0 0,000, 0 ,  0, 0 ,",
" 00,00 ,000, 00,00 , 0 ,00 ,0 0, 0 , 00,"+"0 0, 0 ,0 0,0 0,000,0  ,  0,0  ,00 ,  0,"+" 00, 0 ,000,0 0,00 , 00,",
]
picNumber = [
"000, 00,000,000,0 0,000,000,000,000,000,",
"0 0,  0,  0,  0,0 0,0  ,0  ,  0,0 0,0 0,",
"0 0,  0,000,000,000,000,000,  0,000,000,",
"0 0,  0,0  ,  0,  0,  0,0 0,  0,0 0,  0,",
"000,  0,000,000,  0,000,000,  0,000,000,",
]
#  !"#$%&'()*+,-./
picSym0 = [
    "   , 0 ,0 0,0 0, 0 ,0 0,   , 0 ,  0,0  , 0 ,   ,   ,   ,   ,  0,",
    "   , 0 ,0 0,000, 00,  0,00 , 0 , 0 , 0 ,000, 0 ,   ,   ,   ,  0,",
    "   , 0 ,0 0,0 0, 0 , 0 ,000, 0 , 0 , 0 , 0 ,000,   ,000,   , 0 ,",
    "   ,   ,   ,000,00 ,0  ,00 ,   , 0 , 0 ,0 0, 0 ,00 ,   ,   ,0  ,",
    "   , 0 ,   ,0 0, 0 ,0 0,000,   ,  0,0  ,   ,   , 0 ,   , 0 ,0  ,",
]
# 0123456789
# :;<=>?@
picSym1 = [
    "   ,   ,  0,   ,0  ,000, 0 ,",
    " 0 , 0 , 0 ,000, 0 ,  0,0 0,",
    "   ,   ,0  ,   ,  0, 00,000,",
    " 0 , 0 , 0 ,000, 0 ,   ,000,",
    "   , 0 ,  0,   ,0  , 0 , 0 ,",
]
# ABCDEFGHIJKLMNOPQRSTUVWXYZ
# [\]^_`
picSym2 = [
    "000,0  ,000, 0 ,   , 0 ,",
    "0  ,0  ,  0,0 0,   , 0 ,",
    "0  , 0 ,  0,   ,   ,  0,",
    "0  ,  0,  0,   ,   ,   ,",
    "000,  0,000,   ,000,   ,",
]
# abcdefghijklmnopqrstuvwxyz
# {|}~
picSym3 = [
    " 00, 0 ,00 ,   ,",
    " 0 , 0 , 0 ,   ,",
    "0  , 0 ,  0, 00,",
    " 0 , 0 , 0 ,0  ,",
    " 00, 0 ,00 ,   ,",
]

def getMap(ch):
    def getCh(arr, idx):
        return [
            arr[x][idx*4:idx*4+3] for x in range(5)
        ]
    idx = 0
    if ch.islower():
        idx = ord(ch) - ord('a')
        return getCh(picLower, idx)
    elif ch.isupper():
        idx = ord(ch) - ord('A')
        return getCh(picUpper, idx)
    elif ch.isdigit():
        idx = ord(ch) - ord('0')
        return getCh(picNumber, idx)
    elif ch in " !\"#$%&'()*+,-./":
        idx = ord(ch) - ord(' ')
        return getCh(picSym0, idx)
    elif ch in ":;<=>?@":
        idx = ord(ch) - ord(':')
        return getCh(picSym1, idx)
    elif ch in "[\]^_`":
        idx = ord(ch) - ord('[')
        return getCh(picSym2, idx)
    elif ch in "{|}~":
        idx = ord(ch) - ord('{')
        return getCh(picSym3, idx)
    else:
        return [
            "   ", "   ", "   ", "   ", "   "
        ]

class Word:
    def __init__(self, words):
        params = words[0].split(",")
        words = ' '.join(words[1:])
        self.map = ["", "", "", "", ""]
        for ch in words:
            chMap = getMap(ch)
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
