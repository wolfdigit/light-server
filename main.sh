#!/bin/sh
cd $(dirname "$0")
python web.py &
node ws2812.js
