#!/bin/bash

BIT=$[ 968 + $1 ]
BV=0

for m in `seq 0 7`; do
  BV=$[ BV ^ 1 ]
  echo $BV >/sys/class/gpio/gpio$BIT/value

  echo "$m $BV"
  sleep 1
done
