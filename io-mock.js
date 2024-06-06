/*****************************************
 * serial port
 *****************************************/
const U = require('./utils');

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
    const obj = {};
    obj.srcXy = [buff.readInt8(0), buff.readInt8(1)];
    obj.srcRgb = [buff.readUInt8(2), buff.readUInt8(3), buff.readUInt8(4)];
    obj.dstXy = [buff.readInt8(5), buff.readInt8(6)];
    obj.dstRgb = [buff.readUInt8(7), buff.readUInt8(8), buff.readUInt8(9)];
    obj.ttl = buff.readUInt16LE(10);
    obj.age = 0;
    if (obj.ttl==0 &&
        obj.srcXy[0]==obj.dstXy[0] &&
        obj.srcXy[1]==obj.dstXy[1] &&
        obj.srcRgb[0]==obj.dstRgb[0] &&
        obj.srcRgb[1]==obj.dstRgb[1] &&
        obj.srcRgb[2]==obj.dstRgb[2]
    ) {
        document.BGCOLOR = `rgb(${obj.dstRgb[0]}, ${obj.dstRgb[1]}, ${obj.dstRgb[2]})`;
    }
    else {
        document.objs.push(obj);
    }
    callback();
};
window.mockSerialCrash = false;
document.BRIGHT = U.BRIGHT;
document.BGCOLOR = `rgb(${U.BGCOLOR[0]}, ${U.BGCOLOR[1]}, ${U.BGCOLOR[2]})`;

function delay(ms) {
    return function(data) {
        return new Promise(function(resolve, reject) {
            setTimeout(resolve, ms, data);
        });
    }
}

var ser = undefined;
function openSerial() {
    ser = new SerialPort("/dev/ttyS0", { baudRate: 9600 });
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
    }).then(delay(2));
}




/*****************************************
 * message FIFO
 *****************************************/

const cp = require('child_process');
const fs = require('fs');

var callback = undefined;
function startFifo(path) {
    const handler = function() {
        const data = document.getElementById("fifo").value;
        if (callback!==undefined) {
            callback(data);
        }
    };
    document.getElementById("fifoSend").addEventListener('click', handler);
    document.getElementById("fifo").addEventListener('keyup', function(event) {
        if (event.key === "Enter") {
            handler();
        }
    });
}

function onFifo(cb) {
    callback = cb;
}

function sendFifo(data) {
    callback(data);
}

module.exports = {
    openSerial: openSerial,
    closeSerial: closeSerial,
    writeSerial: writeSerial,
    startFifo: startFifo,
    onFifo: onFifo,
    sendFifo: sendFifo,
 };