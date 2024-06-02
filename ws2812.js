const io = require('./io-mock');
const U = require('./utils');
const RndAge = require('./rnd-age');
const Word = require('./word');

function delay(ms) {
    return function(data) {
        return new Promise(function(resolve, reject) {
            setTimeout(resolve, ms, data);
        });
    }
}

// var runner = new RndAge();
var runner = new Word(["times=1", "Hello, world!"]);
function step() {
    function gen(cmd) {
        return function() {
            return io.writeSerial(cmd.serialize());
        };
    }

    var cmds = runner.run();
    if (!Array.isArray(cmds)) {
        io.sendFifo(cmds);
        return Promise.resolve();
    }
    console.log("n cmd=" + cmds.length);
    var promise = Promise.resolve();
    for (var cmd of cmds) {
        // console.log(cmd);
        promise = promise.then(gen(cmd));
    }
    return promise;
}

function loop() {
    return step().then(delay(100)).then(loop);
}

function openAndLoop() {
    io.openSerial()
    .then(loop)
    .catch(function(err) {
        console.log("err: " + err);
        return delay(5000)().then(openAndLoop);
    });
}


function setBg() {
    function gen(i) {
        return function() {
            return io.writeSerial((new U.Cmd(i, 0, U.STRIP_LEN, U.BGCOLOR)).serialize());
        };
    }

    var promise = Promise.resolve();
    for (var i = 0; i < 5; i++) {
        promise = promise.then(gen(i));
    }

    return promise;
}

io.openSerial()
.then(setBg)
.then(io.closeSerial)
.then(openAndLoop);


io.onFifo(function(data) {
    const words = data.split(' ');
    const mode = words[0];
    switch (mode.toLowerCase()) {
        case 'word':
        case 'wordleft':
            runner = new Word(words.slice(1));
            break;
        case 'rndage':
        default:
            runner = new RndAge();
    }
});
io.startFifo('/tmp/pipe');
