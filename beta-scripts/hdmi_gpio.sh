#!/bin/bash

gpio=(
    $[ $1 & 1 ] $[ ($1 >> 1) & 1 ] $5
    $[ $2 & 1 ] $[ ($2 >> 1) & 1 ] $6
    $[ $3 & 1 ] $[ ($3 >> 1) & 1 ] $7
    $[ $4 & 1 ] $[ ($4 >> 1) & 1 ] $8 )

for n in `seq 192 203`; do
    idx=$[ n - 192 ]
    echo ${gpio[$idx]} >/sys/class/gpio/gpio$n/value
done
