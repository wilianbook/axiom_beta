#!/bin/env python3

import os
import sys
from bitarray import bitarray


def calc_ecc(ecc, byte):
    for bit in range(8):
        if (byte ^ ecc) & 1:
            ecc = ((ecc >> 1) ^ 0x83) & 0xFF
        else:
            ecc = (ecc >> 1) & 0xFF
        byte = byte >> 1
    return ecc

def splice(hdr, val):
    hdra = bitarray(endian='little')
    hdra.frombytes(bytes(hdr))
    vala = bitarray(endian='little')
    vala.frombytes(bytes(val))

    for i in range(32):
        nibh = bitarray([vala[i*2+j*64] for j in range(4)])
        nibl = bitarray([vala[i*2+1+j*64] for j in range(4)])
        data = nibl + nibh + hdra[i:i+1]
        val = sum([(1 << i) if t else 0 for i,t in enumerate(data)])
        print("%s\t0x%02x\t0x%03x" % (data.to01()[::-1], i, val))
        
        

def hex_list(vals):
    return ",".join("{:02x}".format(v) for v in vals)


if_type = int(sys.argv[1], 0)
if_vers = int(sys.argv[2], 0)
if_len = len(sys.argv) - 3

hdr_ecc = calc_ecc(0, if_type)
hdr_ecc = calc_ecc(hdr_ecc, if_vers)
hdr_ecc = calc_ecc(hdr_ecc, if_len)

print("# hdr: %02x,%02x,%02x -> %02x" % (if_type, if_vers, if_len, hdr_ecc))

vals = [int(x, 0) for x in sys.argv[1:]]
vsum = sum(vals + [if_len]) & 0xFF
chk = (0x100 - vsum) & 0xFF

print("# chk: %s,%02x -> %02x" % (hex_list(vals), if_len, chk))

hdr = vals[:3] + [hdr_ecc]
data = [chk] + vals[2:]
num, ecc, pkt = 0, 0, []
for val in data:
    if num == 7:
        pkt += [ecc]
        num, ecc = 0, 0
    else:
        pkt += [val]
        num += 1
        ecc = calc_ecc(ecc, val)

if num < 7:
    while num < 7:
        pkt += [0]
        num += 1
        ecc = calc_ecc(ecc, 0)
    pkt += [ecc]

if len(pkt) % 32 > 0:
    pkt += [0]*(32 - (len(pkt) % 32))


print("# pkt: %s %s %02x" % (hex_list(hdr), hex_list(pkt), int(len(pkt)/32)))
data = splice(hdr, pkt)

