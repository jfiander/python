#!/usr/bin/env python
import sys
sys.path.insert(0, '/home/pi/repos/vendor/zeroborg')

import ZeroBorg
ZB = ZeroBorg.ZeroBorg()
ZB.Init()
ZB.MotorsOff()
ZB.ResetEpo()

print "\nCurrent Status:\n"
print "Motor 1: ", ZB.GetMotor1()
print "Motor 2: ", ZB.GetMotor2()
print "Motor 3: ", ZB.GetMotor3()
print "Motor 4: ", ZB.GetMotor4()

print "EPO:     ", ZB.GetEpo()
