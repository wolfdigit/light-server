const U = require('./utils');

function rgbToBgColor(r, g, b) {
    const scale = 1.0/U.BRIGHT;
    return "rgb(" + r*scale + "," + g*scale + "," + b*scale + ")";
}

function SerialPort(path, options) {
    console.log("opening mock serial at path: " + path);
    console.log("baudRate: " + options.baudRate);
}
SerialPort.prototype.open = function(callback) {
    callback();
};
SerialPort.prototype.close = function(callback) {
    callback();
};
SerialPort.prototype.write = function(buff) {
    if (global.mockSerialCrash) {
        global.mockSerialCrash = false;
        throw new Error("mock crash");
    }
    var data = Uint8Array.from(buff);
    // console.log("write: " + data);
    var x = buff.readUInt8(0);
    var start = buff.readUInt16LE(1);
    var len = buff.readUInt16LE(3);
    var r = buff.readUInt8(5);
    var g = buff.readUInt8(6);
    var b = buff.readUInt8(7);
    for (var y=start; y<start+len; y++) {
        document.getElementById("lite-" + x + "-" + y).style.backgroundColor = rgbToBgColor(r, g, b);
    }
};
global.mockSerialCrash = false;

module.exports = { SerialPort };