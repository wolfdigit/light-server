const U = require('./utils');

const MAXAGE = 30.0;

function Obj(x, y, rgb) {
    this.age = MAXAGE;
    this.x = x;
    this.y = y;
    this.rgb = rgb;
}
Obj.prototype.run = function() {
    this.age -= 1;
    if (this.age < 0) {
        return null;
    }
    const rgb = U.mixRgb(U.BGCOLOR, this.rgb, this.age/MAXAGE);
    return new U.Cmd(this.x, this.y, 1, rgb);
};
Obj.prototype.id = function() {
    return this.x*U.STRIP_LEN + this.y;
};

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
    const newObj = new Obj(x, y, rgb);
    this.objs[newObj.id()] = newObj;
};
RndAge.prototype.run = function() {
    const rnd = Math.random();
    if (rnd < 0.3) {
        this.add();
    }
    const cmds = [];
    for (var id in this.objs) {
        var obj = this.objs[id];
        var cmd = obj.run();
        if (cmd === null) {
            delete this.objs[id];
        } else {
            cmds.push(cmd);
        }
    }
    return cmds.concat(U.Cmd.flush);
};

module.exports = RndAge;