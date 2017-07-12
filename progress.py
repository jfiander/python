#!/usr/bin/python
import os, time

rows, _ = os.popen('stty size', 'r').read().split()

def run(max = 100000, current = 0, delay = 0.0001):
  spinner_state = 0
  spinners = ['|', '/', '-', '\\']
  modulo = max / 100
  print("")
  while current <= max:
    if current % modulo == 0:
      spinner = spinners[spinner_state]
      spinner_state = spinner_state + 1
      if spinner_state > 3:
        spinner_state = 0
    print("\r\033[1A[" + spinner + "] " + str(current).ljust(int(rows), ' '))
    current = current + 1

    time.sleep(delay) # DEVELOPMENT
  spinner = "+"
  current = "Done!"
  print("\r\033[1A[" + spinner + "] " + str(current).ljust(int(rows), ' '))

run()
