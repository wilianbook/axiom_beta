#!/bin/bash

fil_reg 15 0
sleep 0.5

pon_reg 2 0x200
pon_reg 3 0x64

./mat4_conf.sh 0 0 0 0  0 0 0 1  0 0.5 0.5 0  1 0 0 0

./mimg -o -P 0
./mimg -T 6

