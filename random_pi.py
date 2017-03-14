#!/usr/bin/python3
import math
from fractions import gcd
from random import randint
import sys, getopt

def main(argv):
  iterations = 1000
  limit      = 1000

  try:
    opts, args = getopt.getopt(argv, "hn:l:")
  except getopt.GetoptError as e:
    print('Invalid option:', e)
    sys.exit(1)

  for opt, arg in opts:
    if opt == "-n":
      iterations = int(arg)
    elif opt == "-l":
      limit = int(arg)

  step     = 0
  coprimes = 0

  while step < iterations:
    a = randint(1, limit)
    b = randint(1, limit)
    if gcd(a, b) == 1:
      coprimes += 1
    step += 1

  result = math.sqrt(6/(coprimes / iterations))

  print("Pi is approximately:", result)

if __name__ == "__main__":
  main(sys.argv[1:])
