#!/bin/sh

avrdude -p m32u4 -c linuxgpio -v -e -U flash:w:$1 -U lock:w:0x0f:m
