#!/bin/sh

cd "${0%/*}"		# change into script dir

. ./cmv.func

fil2=`fil_reg 0x42`
fil3=`fil_reg 0x43`
fil4=`fil_reg 0x44`
fil5=`fil_reg 0x45`
fil6=`fil_reg 0x46`

pma=$[ (((fil6 >> 15) & 1) << 32) | fil2 ]
pmm=$[ (((fil6 >> 14) & 1) << 32) | fil3 ]

printf "match:\t\t\t%09X\n" $pma
printf "mismatch:\t\t%09X\n" $pmm
printf "waddr_in:\t\t0x%08X\n" $fil4
printf "waddr_sel:\t\t0x%X\n" $[ fil5 >> 30 ]
printf "waddr_inactive:\t\t0x%X\n" $[ (fil5 >> 24) & 0xF ]
printf "fifo_data_wrerr:\t0x%X\n" $[ (fil5 >> 21) & 0x1 ]
printf "fifo_data_rderr:\t0x%X\n" $[ (fil5 >> 20) & 0x1 ]
printf "fifo_data_full:\t\t0x%X\n" $[ (fil5 >> 19) & 0x1 ]
printf "fifo_data_high:\t\t0x%X\n" $[ (fil5 >> 18) & 0x1 ]
printf "fifo_data_low:\t\t0x%X\n" $[ (fil5 >> 17) & 0x1 ]
printf "fifo_data_empty:\t0x%X\n" $[ (fil5 >> 16) & 0x1 ]
printf "buttons:\t\t0x%02X\n" $[ (fil5 >> 8) & 0x1F ]
printf "switches:\t\t0x%02X\n" $[ fil5 & 0xFF ]
printf "cseq_done:\t\t0x%X\n" $[ (fil5 >> 31) & 0x1 ]
printf "cseq_fcnt:\t\t0x%03X\n" $[ (fil5 >> 16) & 0xFFF ]



