#!/bin/bash

DLY=$[ 960 + $1 ]
DV=0

for n in `seq 0 31`; do
  DV=$[ DV ^ 1 ]
  echo $DV >/sys/class/gpio/gpio$DLY/value

  echo "$n $DV"
  sleep 1
done
