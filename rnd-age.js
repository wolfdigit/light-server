const U = require('./utils');

const MAXAGE = 30.0;

function RndAge() {
    this.objs = {};
}
RndAge.prototype.add = function() {
    const x = Math.floor(5*Math.random());
    const y = Math.floor(U.STRIP_LEN*Math.random());
    const h = Math.random();
    const s = 1.0;
    const v = 255;
    const rgb = U.hsvToRgb(h, s, v);
    const newObj = new U.Cmd([x,y], rgb, [x,y], U.BGCOLOR, MAXAGE);
    return newObj;
};
RndAge.prototype.run = function() {
    const rnd = Math.random();
    if (rnd < 0.8) {
        const cmd = this.add();
        return [cmd];
    }
    else {
        return [];
    }
};

module.exports = RndAge;