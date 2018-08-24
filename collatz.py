#!/usr/bin/python

import sys

n = 1

while True:
  i = n
  while i != 1:
    if i % 2 == 1:
      i = 3 * i + 1
    else:
      i = i / 2
  sys.stdout.write('.')
  n = n + 1
