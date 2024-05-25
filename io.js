/*****************************************
 * serial port
 *****************************************/
const SerialPort = require('serialport').SerialPort;

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
function openAndLoopFifo() {
    const readFs = fs.createReadStream(path);
    readFs.on('data', function(data) {
        data = data.toString();
        if (callback!==undefined) {
            callback(data);
        }
    });
    readFs.on('error', function(err) {
        setTimeout(openAndLoopFifo, 5000);
    });
    readFs.on('close', function() {
        setTimeout(openAndLoopFifo, 5000);
    });
}
function startFifo(path) {
    const mkfifo = cp.spawn('mkfifo', [path]);
    mkfifo.on('exit', function() {
        openAndLoopFifo();
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