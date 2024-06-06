const U = require('./utils');

function OutShoot() {
}

OutShoot.prototype.run = function() {
    if (Math.random()<0.2) {
        return [this.add()];
    }
    else {
        return [];
    }
}

OutShoot.prototype.add = function() {
    const dir =  (Math.random()<0.5);
    const srcXy = [2, dir?11:12];
    const theta = (Math.random()-0.5)*Math.PI;
    const dstXy = [Math.floor(Math.sin(theta)*12+2), Math.floor(Math.cos(theta)*12)*(dir?-1:1)+(dir?11:12)];
    const h = Math.random();
    const s = 1.0;
    const v = 255;
    const rgb = U.hsvToRgb(h, s, v);
    const alpha = 0.15;
    const srcRgb = [Math.floor(U.BGCOLOR[0]*(1-alpha)+rgb[0]*alpha), Math.floor(U.BGCOLOR[1]*(1-alpha)+rgb[1]*alpha), Math.floor(U.BGCOLOR[2]*(1-alpha)+rgb[2]*alpha)];
    const dstRgb = rgb;
    const ttl = Math.floor(Math.random()*24+12);
    const cmd = new U.Cmd(srcXy, srcRgb, dstXy, dstRgb, ttl);
    return cmd;
}

module.exports = OutShoot;