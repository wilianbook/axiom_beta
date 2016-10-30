#!/bin/bash

P=( 0123 0132 0213 0231 0312 0321 1023 1032 1203 1230 1302 1320 2013 2031 2103 2130 2301 2310 3012 3021 3102 3120 3201 3210 )

for n in `seq 0 ${#P[*]}`; do
  perm=${P[$n]}
  echo -n "$n $perm "
  for b in `seq 0 3`; do
    pv=${perm:$b:1}
    g0=$[ 192 + b * 3 ]
    g1=$[ 193 + b * 3 ]
    v0=$[ pv & 1 ]
    v1=$[ (pv >> 1) & 1 ]
    echo $v0 >/sys/class/gpio/gpio$g0/value
    echo $v1 >/sys/class/gpio/gpio$g1/value
  done
  for m in `seq 0 15`; do
    for b in `seq 0 3`; do
      gi=$[ 194 + b * 3 ]
      vi=$[ (m >> b) & 1 ]
        echo $vi >/sys/class/gpio/gpio$gi/value
    done
    echo -n .
    sleep 10
  done
  echo .
done

