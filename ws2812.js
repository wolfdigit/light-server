const SerialPort = require('serialport').SerialPort;
const U = require('./utils');
const RndAge = require('./rnd-age');

function delay(ms) {
    return function(data) {
        return new Promise(function(resolve, reject) {
            setTimeout(resolve, ms, data);
        });
    }
}

var ser;
var rndAge = new RndAge();
function step() {
    function gen(cmd) {
        return function() {
            ser.write(cmd.serialize());
        };
    }

    var cmds = rndAge.run();
    console.log("n cmd=" + cmds.length);
    var promise = delay(0)();
    for (var cmd of cmds) {
        // console.log(cmd);
        promise = promise.then(gen(cmd)).then(delay(10));
    }
    return promise;
}

function loop() {
    return step().then(delay(100)).then(loop);
}

function openAndLoop() {
    ser = new SerialPort("/dev/ttyS0", { baudRate: 9600 });
    return new Promise(function(resolve, reject) {
        ser.open(resolve);
    }).then(loop).catch(function(err) {
        console.log("err: " + err);
        return delay(5000)(err).then(openAndLoop);
    });
}

ser = new SerialPort("/dev/ttyS0", { baudRate: 9600 });
ser.open(function() {
    function gen(i) {
        return function() {
            ser.write((new U.Cmd(i, 0, U.STRIP_LEN, U.BGCOLOR)).serialize());
        };
    }

    var promise = delay(0)();
    for (var i = 0; i < 5; i++) {
        promise = promise.then(gen(i)).then(delay(10));
    }

    promise.then(function() {
        ser.close(function() {
            openAndLoop();
        });
    });
});
