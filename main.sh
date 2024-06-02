#!/bin/sh
cd $(dirname "$0")
python web.py &
# python ws2812.py
node ws2812.js
