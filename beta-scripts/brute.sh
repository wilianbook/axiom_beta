#!/bin/bash

for n in `seq 0 255`; do
  echo "$n"
  for b in `seq 0 7`; do
    bv=$[ (n >> b) & 1 ]
    gp=$[ 192 + b + (b/2) ]
    echo $bv >/sys/class/gpio/gpio$gp/value
  done
  sleep 2
done

