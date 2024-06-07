const U = require('./utils');

function Fill() {
}

var cnt = 0;
Fill.prototype.run = function() {
    const y = cnt&0x1F;
    const round = cnt>>5;
    const h0 = round * (1.0/6);
    const h1 = (round+1) * (1.0/6);
    const cmds = [];
    if (y<24) {
        for (var x = 0; x < 5; x++) {
            var cmd = new U.Cmd([x,y], U.hsvToRgb(h0, 1.0, 128), [x,y], U.hsvToRgb(h1, 1.0, 128), 32);
            cmds.push(cmd);
        }
    }
    cnt++;
    return cmds;
}

module.exports = Fill;