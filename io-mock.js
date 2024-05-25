/*****************************************
 * serial port
 *****************************************/
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
SerialPort.prototype.write = function(buff, callback) {
    if (window.mockSerialCrash) {
        window.mockSerialCrash = false;
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
    callback();
};
window.mockSerialCrash = false;

function delay(ms) {
    return function(data) {
        return new Promise(function(resolve, reject) {
            setTimeout(resolve, ms, data);
        });
    }
}

var ser = undefined;
function openSerial() {
    ser = new SerialPort("/dev/ttyS0", { baudRate: 38400 });
    return new Promise(function(resolve, reject) {
        ser.open(resolve);
    });
}

function closeSerial() {
    return new Promise(function(resolve, reject) {
        ser.close(resolve);
    });
}

function writeSerial(buff) {
    return new Promise(function(resolve, reject) {
        ser.write(buff, resolve);
    }).then(delay(5));
}




/*****************************************
 * message FIFO
 *****************************************/

const cp = require('child_process');
const fs = require('fs');

var callback = undefined;
function startFifo(path) {
    document.getElementById("fifoSend").addEventListener('click', function() {
        const data = document.getElementById("fifo").value;
        if (callback!==undefined) {
            callback(data);
        }
    });
}

function onFifo(cb) {
    callback = cb;
}

module.exports = {
    openSerial: openSerial,
    closeSerial: closeSerial,
    writeSerial: writeSerial,
    startFifo: startFifo,
    onFifo: onFifo
 };