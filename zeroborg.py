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
