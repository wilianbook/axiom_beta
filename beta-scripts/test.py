#!/bin/env python3

import sys

data = sys.argv[1:]

while len(data) > 0:
    car, cdr, data = data[0], data[1:4], data[4:]
    print("%s|%s -> %s" % (car, cdr, data))

