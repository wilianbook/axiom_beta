#!/bin/bash

./linear_conf.sh 0 0.3125
# for n in `seq 0 2 1024`; do devmem $[ 0x60300000 + n*4 ] 16 0xF00; done



for n in `seq 0 600`; do 
	devmem $[ 0x18000000 + 200*8 + n*16384 ] 64 0x000000000000FFFF
	devmem $[ 0x1A000000 + 200*8 + n*16384 ] 64 0x000000000000FFFF
	devmem $[ 0x1C000000 + 200*8 + n*16384 ] 64 0x000000000000FFFF
	devmem $[ 0x1E000000 + 200*8 + n*16384 ] 64 0x000000000000FFFF
done

devmem $[ 0x60300000 + 200*4 ] 16 0xF00
devmem $[ 0x60302000 + 200*4 ] 16 0xF00


for n in `seq 0 400`; do 
	devmem $[ 0x18000000 + 791*8 + n*16384 ] 64 0x000000000000F777
	devmem $[ 0x1A000000 + 791*8 + n*16384 ] 64 0x000000000000F777
	devmem $[ 0x1C000000 + 791*8 + n*16384 ] 64 0x000000000000F777
	devmem $[ 0x1E000000 + 791*8 + n*16384 ] 64 0x000000000000F777
done

devmem $[ 0x60300000 + 791*4 ] 16 0xF00
devmem $[ 0x60302000 + 791*4 ] 16 0xF00

