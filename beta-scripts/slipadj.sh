#!/bin/bash


for m in `seq 0 15`; do
  echo $m
  for b in `seq 0 3`; do
    BV=$[ (m >> b) & 1 ]
    BIT=$[ 972 + b ]
    echo $BV >/sys/class/gpio/gpio$BIT/value
  done
  sleep 1
done
