const BRIGHT = 0.3;
const PXSIZE = 3;
const STRIP_LEN = 24;
const BGCOLOR = [0, 12, 12];

function Cmd(srcXy, srcRgb, dstXy, dstRgb, ttl) {
    this.srcXy = srcXy
    this.srcRgb = srcRgb
    this.dstXy = dstXy
    this.dstRgb = dstRgb
    this.ttl = ttl
}

Cmd.prototype.serialize = function() {
    const data = [
        this.srcXy[0], this.srcXy[1],
        Math.floor(this.srcRgb[0]*BRIGHT), Math.floor(this.srcRgb[1]*BRIGHT), Math.floor(this.srcRgb[2]*BRIGHT),
        this.dstXy[0], this.dstXy[1],
        Math.floor(this.dstRgb[0]*BRIGHT), Math.floor(this.dstRgb[1]*BRIGHT), Math.floor(this.dstRgb[2]*BRIGHT),
        this.ttl&0xFF, (this.ttl>>8)&0xFF
    ]
    if (Buffer.from!==undefined) {
        return Buffer.from(data);
    }
    else {
        return new Buffer(data);
    }
}
Cmd.prototype.inspect = function() {
    return this.srcXy.join(",")+":"+this.srcRgb.join(",")+" - "+this.dstXy.join(",")+":"+this.dstRgb.join(",") + " @"+this.ttl;
}
Cmd.setBg = function(rgb) {
    return new Cmd([0,0], BGCOLOR, [0,0], BGCOLOR, 0);
}

function hsvToRgb(h, s, v) {
    if (s == 0.0) {
        return v, v, v
    }
    var i = Math.floor(h * 6.0)
    const f = (h * 6.0) - i
    const p = v * (1.0 - s)
    const q = v * (1.0 - s * f)
    const t = v * (1.0 - s * (1.0 - f))
    i = i % 6
    if (i == 0) {
        return [v, t, p]
    }
    if (i == 1) {
        return [q, v, p]
    }
    if (i == 2) {
        return [p, v, t]
    }
    if (i == 3) {
        return [p, q, v]
    }
    if (i == 4) {
        return [t, p, v]
    }
    if (i == 5) {
        return [v, p, q]
    }
}

function mixRgb(rgb1, rgb2, alpha) {
    return [
        rgb1[0]*(1-alpha) + rgb2[0]*alpha,
        rgb1[1]*(1-alpha) + rgb2[1]*alpha,
        rgb1[2]*(1-alpha) + rgb2[2]*alpha
    ];
}

module.exports = {
    BRIGHT: BRIGHT,
    BGCOLOR: BGCOLOR,
    STRIP_LEN: STRIP_LEN,
    Cmd: Cmd,
    hsvToRgb: hsvToRgb,
    mixRgb: mixRgb
};