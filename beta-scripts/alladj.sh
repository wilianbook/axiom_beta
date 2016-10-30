#!/bin/bash

DLY=$[ 960 + $1 ]
BIT=$[ 968 + $1 ]

DV=0
BV=0

for m in `seq 0 7`; do
  BV=$[ BV ^ 1 ]
  echo $BV >/sys/class/gpio/gpio$BIT/value

  for n in `seq 0 31`; do
    DV=$[ DV ^ 1 ]
    echo $DV >/sys/class/gpio/gpio$DLY/value

    echo "$m $n $BV $DV"
    sleep 1
  done
done
