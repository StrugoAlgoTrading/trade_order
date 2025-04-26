#!/bin/bash

echo "Starting Xvfb..."
Xvfb :1 -screen 0 1024x768x16 &

echo "Starting socat..."
socat TCP-LISTEN:4004,fork TCP:localhost:4002 &

export DISPLAY=:1

echo "Starting IB Gateway via IBC..."
/home/ibgateway/ibc/ibcstart.sh gateway
