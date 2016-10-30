#!/bin/sh

cd "${0%/*}"		# change into script dir

. ./i2c1.func


i2c1_set 0x38 0x01	# TDO_W input
i2c1_set 0x3A 0xFF	# all pullups

TDO=0x1; TDI=0x2; TCK=0x4; TMS=0x8


jtag_clock() {
  local v=$[ $1|$2 ]
  i2c1_set 0x39 $v
  i2c1_set 0x39 $[v|TCK]
}

jtag_in() {
  local b=$[`i2c1_get 0x39`&TDO]
  [ $b -eq 0 ] && echo "0" || echo "1"
}

jtag_shift() {
  local so=$2
  local si=""
  while [ -n "$so" ]; do
    local b=${so:$[${#so}-1]}	# ${so:-1} doesn't work
    so=${so::-1}
    local v=0; [ $b == '1' ] && v=$TDI 
    [ -n "$so" ] \
	&& jtag_clock $1 $v \
	|| jtag_clock $1 $[v|TMS]
    b=`jtag_in`
    si="$b$si"
  done
  echo $si
}

jtag_cseq() {
  local bv=$1; shift
  for v in "$@"; do
    jtag_clock $bv $v
  done
}

OST=0x00

i2c1_set 0x39 0x0

# goto reset
# jtag_cseq $OST $TMS $TMS $TMS $TMS $TMS
i2c1_set 0x13 6 0xFF

# goto Shift-IR
# jtag_cseq $OST 0 $TMS $TMS 0 0
i2c1_set 0x13 5 0x06

# shift in IDCODE [11100000]
# s=`jtag_shift $OST 11100000`
# echo "$s"
i2c1_set 0x14 0xE0
echo `i2c1_get 0x14`

# goto Shift-DR
# jtag_cseq $OST $TMS $TMS 0 0
i2c1_set 0x13 4 0x3


#s=`jtag_shift $OST 11100000000000000000000000011111`
#echo "$s"
i2c1_set 0x18 0x1F
echo `i2c1_get 0x18`
i2c1_set 0x18 0x00
echo `i2c1_get 0x18`
i2c1_set 0x18 0x00
echo `i2c1_get 0x18`
i2c1_set 0x14 0xE0
echo `i2c1_get 0x14`


# goto reset
# jtag_cseq $OST $TMS $TMS $TMS $TMS $TMS
i2c1_set 0x13 6 0xFF


i2c1_set 0x39 $OST

exit 0

