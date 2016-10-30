#!/bin/bash

. ./cmv.func

for i in `seq 0 31`; do
    del_reg 33 $i
    for j in `seq 0 31`; do
	del_reg 32 $j

	sleep 0.5
	printf "%3d,%-3d " $i $j
	fil_reg 0x46
    done
done
