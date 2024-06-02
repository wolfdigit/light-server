const U = require('./utils');

const picUpper = [
"000,000,000,00 ,000,000,000,0 0,000,  0,"+"0 0,0  ,000,000,000,000,000,000, 00,000,"+"0 0,0 0,0 0,0 0,0 0,000,",
"0 0,0 0,0  ,0 0,0  ,0  ,0  ,0 0, 0 ,  0,"+"0 0,0  ,000,0 0,0 0,0 0,0 0,0 0,0  , 0 ,"+"0 0,0 0,0 0,0 0,0 0,  0,",
"000,00 ,0  ,0 0,00 ,00 ,0 0,000, 0 ,  0,"+"00 ,0  ,0 0,0 0,0 0,000,0 0,00 , 0 , 0 ,"+"0 0,0 0,0 0, 0 ,000, 0 ,",
"0 0,0 0,0  ,0 0,0  ,0  ,0 0,0 0, 0 ,0 0,"+"0 0,0  ,0 0,0 0,0 0,0  ,000,0 0,  0, 0 ,"+"0 0,0 0,000,0 0, 0 ,0  ,",
"0 0,000,000,00 ,000,0  ,000,0 0,000,000,"+"0 0,000,0 0,0 0,000,0  ,000,0 0,00 , 0 ,"+"000, 0 ,000,0 0, 0 ,000,",
];
const picLower = [
"   ,0  ,   ,  0,   ,  0,   ,0  , 0 ,  0,"+"0  , 0 ,   ,   ,   ,   ,   ,   ,   , 0 ,"+"   ,   ,   ,   ,   ,   ,",
"   ,0  ,   ,  0,   , 0 ,000,0  ,   ,   ,"+"0  , 0 ,   ,   ,   ,000,000,   ,   ,000,"+"   ,   ,   ,   ,0 0,   ,",
" 00,00 ,000, 00, 0 ,000,000,000, 0 ,  0,"+"0 0, 0 ,00 ,00 ,000,0 0,0 0,000, 00, 0 ,"+"0 0,0 0,0 0,0 0,000,00 ,",
"0 0,0 0,0  ,0 0,000, 0 ,  0,0 0, 0 ,0 0,"+"00 , 0 ,000,0 0,0 0,000,000,0  , 0 , 0 ,"+"0 0,0 0,000, 0 ,  0, 0 ,",
" 00,00 ,000, 00,00 , 0 ,00 ,0 0, 0 , 00,"+"0 0, 0 ,0 0,0 0,000,0  ,  0,0  ,00 ,  0,"+" 00, 0 ,000,0 0,00 , 00,",
];
const picNumber = [
"000, 00,000,000,0 0,000,000,000,000,000,",
"0 0,  0,  0,  0,0 0,0  ,0  ,  0,0 0,0 0,",
"0 0,  0,000,000,000,000,000,  0,000,000,",
"0 0,  0,0  ,  0,  0,  0,0 0,  0,0 0,  0,",
"000,  0,000,000,  0,000,000,  0,000,000,",
];
//  !"#$%&'()*+,-./
const picSym0 = [
    "   , 0 ,0 0,0 0, 0 ,0 0,   , 0 ,  0,0  , 0 ,   ,   ,   ,   ,  0,",
    "   , 0 ,0 0,000, 00,  0,00 , 0 , 0 , 0 ,000, 0 ,   ,   ,   ,  0,",
    "   , 0 ,0 0,0 0, 0 , 0 ,000, 0 , 0 , 0 , 0 ,000,   ,000,   , 0 ,",
    "   ,   ,   ,000,00 ,0  ,00 ,   , 0 , 0 ,0 0, 0 ,00 ,   ,   ,0  ,",
    "   , 0 ,   ,0 0, 0 ,0 0,000,   ,  0,0  ,   ,   , 0 ,   , 0 ,0  ,",
];
// 0123456789
// :;<=>?@
const picSym1 = [
    "   ,   ,  0,   ,0  ,000, 0 ,",
    " 0 , 0 , 0 ,000, 0 ,  0,0 0,",
    "   ,   ,0  ,   ,  0, 00,000,",
    " 0 , 0 , 0 ,000, 0 ,   ,000,",
    "   , 0 ,  0,   ,0  , 0 , 0 ,",
];
// ABCDEFGHIJKLMNOPQRSTUVWXYZ
// [\]^_`
const picSym2 = [
    "000,0  ,000, 0 ,   , 0 ,",
    "0  ,0  ,  0,0 0,   , 0 ,",
    "0  , 0 ,  0,   ,   ,  0,",
    "0  ,  0,  0,   ,   ,   ,",
    "000,  0,000,   ,000,   ,",
];
// abcdefghijklmnopqrstuvwxyz
// {|}~
const picSym3 = [
    " 00, 0 ,00 ,   ,",
    " 0 , 0 , 0 ,   ,",
    "0  , 0 ,  0, 00,",
    " 0 , 0 , 0 ,0  ,",
    " 00, 0 ,00 ,   ,",
];

function getMap(ch) {
    function getCh(arr, idx) {
        return [0,1,2,3,4].map(function(x) { return arr[x].substring(idx*4, idx*4+3); } );
    }
    var idx = 0;
    if (ch >= 'a' && ch <= 'z') {
        idx = ch.charCodeAt() - 'a'.charCodeAt();
        return getCh(picLower, idx);
    } else if (ch >= 'A' && ch <= 'Z') {
        idx = ch.charCodeAt() - 'A'.charCodeAt();
        return getCh(picUpper, idx);
    } else if (ch >= '0' && ch <= '9') {
        idx = ch.charCodeAt() - '0'.charCodeAt();
        return getCh(picNumber, idx);
    } else if (ch >= ' ' && ch <= '/') {
        idx = ch.charCodeAt() - ' '.charCodeAt();
        return getCh(picSym0, idx);
    } else if (ch >= ':' && ch <= '@') {
        idx = ch.charCodeAt() - ':'.charCodeAt();
        return getCh(picSym1, idx);
    } else if (ch >= '[' && ch <= '`') {
        idx = ch.charCodeAt() - '['.charCodeAt();
        return getCh(picSym2, idx);
    } else if (ch >= '{' && ch <= '~') {
        idx = ch.charCodeAt() - '{'.charCodeAt();
        return getCh(picSym3, idx);
    }
    else {
        return [0,1,2,3,4].map(function(x) { return "   "; } );
    }
}

function Word(words) {
    var params = words[0].split(",");
    words = words.slice(1).join(' ');
    this.map = ["", "", "", "", ""];
    for (var ch of words) {
        var chMap = getMap(ch);
        for (var i = 0; i < 5; i++) {
            this.map[i] += chMap[i];
            this.map[i] += " ";
        }
    }
    console.log(this.map);

    this.pos = -U.STRIP_LEN;
    this.FGCOLOR = [255, 255, 0];
    this.BGCOLOR = U.BGCOLOR;
    this.times = -1;

    // word color=FF00CC,bgcolor=030303,times=1 asdf
    for (var param of params) {
        if (param.substring(0, 6) === "color=") {
            this.FGCOLOR = [
                parseInt(param.substring(6, 8), 16),
                parseInt(param.substring(8, 10), 16),
                parseInt(param.substring(10, 12), 16),
            ];
        }
        if (param.substring(0, 8) === "bgcolor=") {
            this.BGCOLOR = [
                parseInt(param.substring(8, 10), 16),
                parseInt(param.substring(10, 12), 16),
                parseInt(param.substring(12, 14), 16),
            ];
        }
        if (param.substring(0, 6) === "times=") {
            this.times = parseInt(param.substring(6), 10);
        }
    }
}

Word.prototype.move = function() {
    if (this.pos >= this.map[0].length) {
        this.pos = -U.STRIP_LEN;
        if (this.times > 0) {
            this.times--;
        }
        return;
    }
    this.pos++;
};
Word.prototype.render = function() {
    if (this.times===0) {
        return "rndAge";
    }
    const cmds = [];
    const getPx = (function(x, y) {
        if (y<0) return 0;
        if (y>=this.map[x].length) return 0;
        if (this.map[x][y] === " ") return 0;
        return 1;
    }).bind(this);
    for (var x = 0; x < 5; x++) {
        var yStart = 0;
        while (yStart<U.STRIP_LEN) {
            var mapStart = this.pos + yStart;
            var yEnd = yStart+1;
            while (yEnd<U.STRIP_LEN && getPx(x, this.pos+yEnd) === getPx(x, mapStart)) {
                yEnd++;
            }
            var cmd = new U.Cmd(x, yStart, yEnd-yStart, getPx(x,mapStart)===1?this.FGCOLOR:this.BGCOLOR);
            cmds.push(cmd);
            yStart = yEnd;
        }
        cmds.push(U.Cmd.flush[x]);
    }

    // console.log(cmds);
    return cmds;
};

var counter = 0;
Word.prototype.run = function() {
    if (counter++ % 2 === 0) {
        this.move();
    }
    return this.render();
}

module.exports = Word;
