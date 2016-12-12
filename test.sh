#!/bin/bash

echo "to test call this script with the ip address of your load balancer"
echo "example:"
echo "$0 111.222.333.444"
BALANCER=$1
COUNT=100
CONCURRENT=2
# Benchmarking time limit in seconds
TIMELIMIT=30
echo "Running apache bench with ${COUNT} requests and concurrency of ${CONCURRENT}"
echo "to see how many requests we can respond to in ${TIMEOUT} seconds."
ab -n ${COUNT} -c ${CONCURRENT} -t ${TIMELIMIT} "http://${BALANCER}/?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&BBOX=-34.1618264695945939,18.58220000000000027,-33.71490000000000009,19.24800000000000111&CRS=EPSG:4326&WIDTH=194&HEIGHT=130&LAYERS=CapeWinelands&STYLES=&FORMAT=image/jpeg&DPI=72&MAP_RESOLUTION=72&FORMAT_OPTIONS=dpi:72"

echo "Making an image request - you should see it pop up when done"
rm test.png
wget -O test.png "http://${BALANCER}/?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&BBOX=-34.1618264695945939,18.58220000000000027,-33.71490000000000009,19.24800000000000111&CRS=EPSG:4326&WIDTH=194&HEIGHT=130&LAYERS=CapeWinelands&STYLES=&FORMAT=image/jpeg&DPI=72&MAP_RESOLUTION=72&FORMAT_OPTIONS=dpi:72"
open test.png
