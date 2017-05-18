#!/usr/bin/python

input  = raw_input()
output = ""

if len(input)%2 > 0:
  input = input + "0"

pairs = [input[i:i+2] for i in range(0, len(input), 2)]

for pair in pairs:
  if pair == "00":
    base = "A"
  elif pair == "01":
    base = "C"
  elif pair == "10":
    base = "G"
  elif pair == "11":
    base = "T"
  output = output + base

print(output)
