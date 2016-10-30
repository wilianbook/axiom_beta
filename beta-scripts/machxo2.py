#!/bin/env python3

# Copyright (C) 2016 Herbert Poetzl

import sys
import serial
import struct

from smbus import SMBus
from time import sleep
from bitarray import bitarray
from jtag import *


def rev(s):
    return s[::-1]

def h2b(s):
    return ''.join([format(int(_,16),"04b") for _ in s])
    
def b2h(s):
    return ''.join([format(int(''.join(_),2),"X") for _ in zip(*[iter(s)]*4)])

class MachXO2:
    ISC_DATA_SHIFT          = ( 0x0A, 0 )
    ISC_ERASE               = ( 0x0E, 0 )
    ISC_DISCHARGE           = ( 0x14, 0 )
    EXTEST                  = ( 0x15, 0 )
    HIGHZ                   = ( 0x18, 0 )
    UIDCODE_PUB             = ( 0x19, 0 )
    PRELOAD                 = ( 0x1C, 0 )
    SAMPLE                  = ( 0x1C, 0 )
    ISC_ERASE_DONE          = ( 0x24, 0 )
    ISC_DISABLE             = ( 0x26, 0 )
    ISC_NOOP                = ( 0x30, 0 )
    LSC_RESET_CRC           = ( 0x3B, 0 )
    LSC_READ_STATUS         = ( 0x3C, 0 )
    ISC_ADDRESS_SHIFT       = ( 0x42, 0 )
    LSC_INIT_ADDRESS        = ( 0x46, 0 )
    LSC_INIT_ADDR_UFM       = ( 0x47, 0 )
    ISC_PROGRAM_DONE        = ( 0x5E, 0 )
    LSC_READ_CRC            = ( 0x60, 0 )
    ISC_PROGRAM             = ( 0x67, 0 )
    LSC_PROG_INCR_NV        = ( 0x70, 0 )
    LSC_READ_INCR_NV        = ( 0x73, 0 )
    LSC_ENABLE_X            = ( 0x74, 0 )
    CLAMP                   = ( 0x78, 0 )
    LSC_REFRESH             = ( 0x79, 0 )
    LSC_BITSTREAM_BURST     = ( 0x7A, 0 )
    LSC_DEVICE_CTRL         = ( 0x7D, 0 )
    ISC_READ                = ( 0x80, 0 )
    LSC_PROG_INCR_RTI       = ( 0x82, 0 )
    LSC_WRITE_ADDRESS       = ( 0xB4, 0 )
    LSC_PROG_INCR_ENC       = ( 0xB6, 0 )
    LSC_PROG_INCR_CMP       = ( 0xB8, 0 )
    LSC_PROG_INCR_CNE       = ( 0xBA, 0 )
    LSC_SHIFT_PASSWORD      = ( 0xBC, 0 )
    USERCODE                = ( 0xC0, 0 )
    ISC_PROGRAM_USERCODE    = ( 0xC2, 0 )
    ISC_ENABLE              = ( 0xC6, 0 )
    LSC_PROG_TAG            = ( 0xC9, 0 )
    LSC_READ_TAG            = ( 0xCA, 0 )
    LSC_ERASE_TAG           = ( 0xCB, 0 )
    ISC_PROGRAM_SECURITY    = ( 0xCE, 0 )
    LSC_PROGRAM_SECPLUS     = ( 0xCF, 0 )
    IDCODE                  = ( 0xE0, 0 )
    LSC_PROG_FEATURE        = ( 0xE4, 0 )
    LSC_READ_FEATURE        = ( 0xE7, 0 )
    LSC_CHECK_BUSY          = ( 0xF0, 0 )
    LSC_PROG_PASSWORD       = ( 0xF1, 0 )
    LSC_READ_PASSWORD       = ( 0xF2, 0 )
    LSC_PROG_CIPHER_KEY     = ( 0xF3, 0 )
    LSC_READ_CIPHER_KEY     = ( 0xF4, 0 )
    LSC_PROG_FEABITS        = ( 0xF8, 0 )
    LSC_PROG_OTP            = ( 0xF9, 0 )
    LSC_READ_OTP            = ( 0xFA, 0 )
    LSC_READ_FEABITS        = ( 0xFB, 0 )
    BYPASS                  = ( 0xFF, 0 )

    DEV = { 
        "00000000000000000000000000000000" : "<zeros>",
        "00000001001010111001000001000011" : "MXO2-640HC",
        "00000001001010111010000001000011" : "MXO2-1200HC",
        "00000001001010111011000001000011" : "MXO2-2000HC" }

    CELLS = { 
        "00000000000000000000000000000000" : 0,
        "00000001001010111001000001000011" : 19*8,
        "00000001001010111010000001000011" : 26*8,
        "00000001001010111011000001000011" : 53*8 }

    SBITS = [
        ( 0, 1, "TRAN"),
        ( 1, 3, ["CFG", "SRAM", "EFUSE", "?", "?", "?", "?", "?", "?"]),
        ( 4, 1, "JTAG"),
        ( 5, 1, "PWDPROT"),
        ( 6, 1, "OTP"),
        ( 7, 1, "DECRYPT"),
        ( 8, 1, "DONE"),
        ( 9, 1, "ISC"),
        (10, 1, "WRITE"),
        (11, 1, "READ"),
        (12, 1, "BUSY"),
        (13, 1, "FAIL"),
        (14, 1, "FEAOTP"),
        (15, 1, "DONLY"),
        (16, 1, "PWDEN"),
        (17, 1, "UFMOTP"),
        (18, 1, "ASSP"),
        (19, 1, "SDMEN"),
        (20, 1, "EPREAM"),
        (21, 1, "PREAM"),
        (22, 1, "SPIFAIL"),
        (23, 3, ["BSE", "OK", "ID", "CMD", "CRC", "PRMB", "ABRT", "OVFL", "SDM"]),
        (26, 1, "EEXEC"),
        (27, 1, "EIO"),
        (28, 1, "INVCMD"),
        (29, 1, "ESED"),
        (30, 1, "BYPASS"),
        (31, 1, "FTM") ]

    FBITS = [
        (  0, 32, "IDCODE"),
        ( 32, 8, "TRACEID"),
        ( 40, 8, "I2CADDR"),
        ( 48, 1, "SECPWD"),
        ( 49, 1, "DECONLY"),
        ( 50, 1, "PWDFLASH"),
        ( 51, 1, "PWDALL"),
        ( 52, 1, "MYASSP"),
        ( 53, 1, "PROGRAM"),
        ( 54, 1, "INIT"),
        ( 55, 1, "DONE"),
        ( 56, 1, "JTAG"),
        ( 57, 1, "SSPI"),
        ( 58, 1, "I2C"),
        ( 59, 1, "MSPI"),
        ( 60, 1, "BOOTS1"),
        ( 61, 1, "BOOTS2"),
        ( 62, 2, "RSVD") ]

    def __init__(self, i2c):
        self.i2c = i2c
        self.jtag = JTag(i2c)


    def status(self):
        jtag.sir(rev(h2b("3C")))    # shift in READ_STATUS (0x3C)
        status = jtag.tdo(32)       # read status
        hr = []
        for (sbit, blen, name) in sbits:
            bits = rev(status)[sbit:sbit+blen]
            if blen == 1:
                if bits == "1":
                    hr.append(name)
            else:
                bval = int(bits, 2)
                hr.append("%s=%s" % (name[0], name[bval+1]))
        print("status %s [%s] %s" %
            (b2h(status), status, " ".join(hr)))
    
        


i2c = SMBus(2)


with open(sys.argv[1]) as f:
    cont = f.readlines()


# i2c.write_byte(0x38, 0x01)  # TDO_W input
# i2c.write_byte(0x3A, 0xFF)  # all pullups

# i2c.write_byte(0x39, 0x00) 

jtag = JTag(i2c)

jtag.sir(rev(h2b("E0")))    # shift in IDCODE (0xE0)
idcode = jtag.tdo(32)       # read idcode
dev = devid[idcode]
print("found %s [%s]" % (dev, idcode))

jtag.sir(rev(h2b("1C")))    # shift in PRELOAD (0x1C)
jtag.tdi(rev(h2b("F"*106)))
jtag.idle(2)

status(jtag)
jtag.sir(rev(h2b("FF")))    # shift in BYPASS (0xFF)
jtag.idle(2)

jtag.sir(rev(h2b("C6")))    # shift in ISC ENABLE (0xC6) 
jtag.tdi(rev(h2b("08")))
jtag.runtest(2)

jtag.sir(rev(h2b("0E")))    # shift in ISC ERASE (0x0E)
jtag.tdi(rev(h2b("0E")))
jtag.idle(2)

jtag.sir(rev(h2b("46")))    # shift in LSC_INIT_ADDRESS (0x46)
jtag.tdi(rev(h2b("04")))
jtag.idle(2)

status(jtag)

data = ""
scan = False
for line in cont:
    if line[0] == '*':
        scan = False
        # break               # skip zeros
    if line[0] == 'L':
        scan = True
    if scan and line[0] in "01":
        jtag.sir(rev(h2b("70")))    # shift in LSC_PROG_INCR_NV (0x70)
        jtag.tdi(rev(line.strip()))
        jtag.idle(10)

jtag.sir(rev(h2b("46")))    # shift in LSC_INIT_ADDRESS (0x46)
jtag.tdi(rev(h2b("02")))
jtag.idle(2)

jtag.sir(rev(h2b("E4")))    # shift in LSC_PROG_FEATURE (0xE4)
jtag.tdi(rev(h2b("0000000000000010")))
jtag.idle(2)

status(jtag)

jtag.sir(rev(h2b("F8")))    # shift in LSC_PROG_FEABITS (0xF8)
jtag.tdi(rev(h2b("0620")))
jtag.idle(2)

status(jtag)

jtag.sir(rev(h2b("5E")))    # shift in ISC PROGRAM DONE (0x5E)
jtag.sir(rev(h2b("F0")))    # shift in LSC_CHECK_BUSY (0xF0)
busy = jtag.tdo(1)          # read busy flag
print("busy = %s" % (busy))
jtag.idle(2)

status(jtag)
jtag.sir(rev(h2b("C0")))    # shift in USERCODE (0xC0)
usercode = jtag.tdo(32)     # read usercode
print("usercode %s [%s]" % (b2h(usercode), usercode))

status(jtag)

jtag.sir(rev(h2b("79")))    # shift in LSC_REFRESH (0x79) 
jtag.idle(2)

jtag.sir(rev(h2b("26")))    # shift in ISC DISABLE (0x26)
jtag.idle(2)
status(jtag)

jtag.reset()

# i2c.write_byte(0x39, 0x00) 


