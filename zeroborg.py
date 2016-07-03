#!/usr/bin/env python
import sys
sys.path.insert(0, '/home/pi/repos/vendor/zeroborg')

import ZeroBorg
ZB = ZeroBorg.ZeroBorg()
ZB.Init()
ZB.MotorsOff()
ZB.ResetEpo()

speed = 1

print "\nCurrent Status:\n"
print "Motor 1: ", ZB.GetMotor1() # Front Left
print "Motor 2: ", ZB.GetMotor2() # Rear Left
print "Motor 3: ", ZB.GetMotor3() # Front Right
print "Motor 4: ", ZB.GetMotor4() # Rear Right

print "EPO:     ", ZB.GetEpo()

print

##########

while (1):
  c = raw_input('> ')

  if (c == "exit"):
    print "Shutting down\n"
    ZB.MotorsOff()
    break
  elif (c == "speed"):
    speed = float(raw_input('speed> '))
  elif (c == "w"):
    print "Forward"
    ZB.SetMotor1(speed)
    ZB.SetMotor2(speed)
    ZB.SetMotor3(-speed)
    ZB.SetMotor4(-speed)
  elif (c == "a"):
    print "Left"
    ZB.SetMotor1(-speed)
    ZB.SetMotor2(-speed)
    ZB.SetMotor3(-speed)
    ZB.SetMotor4(-speed)
  elif (c == "d"):
    print "Right"
    ZB.SetMotor1(speed)
    ZB.SetMotor2(speed)
    ZB.SetMotor3(speed)
    ZB.SetMotor4(speed)
  elif (c == "s"):
    print "Back"
    ZB.SetMotor1(-speed)
    ZB.SetMotor2(-speed)
    ZB.SetMotor3(speed)
    ZB.SetMotor4(speed)
  elif (c == "x"):
    print "Stop"
    ZB.MotorsOff()

  print "1: ", ZB.GetMotor1(), " - 2: ", ZB.GetMotor2(), " - 3: ", ZB.GetMotor3(), " - 4: ", ZB.GetMotor4()
