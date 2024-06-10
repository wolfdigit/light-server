#!/usr/bin/env python

import random
import time
import serial

from clock import Clock
from scheduler import Scheduler
random.seed()

from rndAge import RndAge
from word import Word
from util import  Cmd

def waitAck():
	for w in range(1000):
		if ser.inWaiting()>0:
			data = ser.read(ser.inWaiting())
			break

def writeSerial(buff):
	ser.write(buff)
	waitAck()

def setBg():
	writeSerial(Cmd.setBg().serialize())
	writeSerial(Cmd.flush(0, 5).serialize())

# runner = RndAge()
# runner = Word(["times=1", "Hello, world!"])
runner = Scheduler(RndAge())
runner.prepend_task(Word(["times=1", "Hello, world!"]))
# runner.set_interval(Clock(), 3000)
runner.set_cronjob(Clock(), "0 */5 * * *")

while True:
	try:
		ser = serial.Serial("/dev/ttyS0", baudrate=115200, parity="E")
		setBg()
		prev = time.time()
		while True:
			# print("opening tmp file")
			# with open('/tmp/light', 'r') as f:
			cmds = runner.run()
			if not isinstance(cmds, list):
				runner = RndAge()    # TODO: pipe
			else:
				print("n cmd="+str(len(cmds)))
				for cmd in cmds:
					writeSerial(cmd.serialize())
			now = time.time()
			time.sleep(max(0.1-(now-prev), 0))
			prev = now
	except Exception as ex:
		print(ex)
		time.sleep(5)
