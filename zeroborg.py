#!/usr/bin/env python
import sys
sys.path.insert(0, '/home/pi/repos/vendor/zeroborg')

import ZeroBorg
ZB = ZeroBorg.ZeroBorg()

if ZB.foundChip:
    print 'Found ZeroBorg.'
else:
    print 'No ZeroBorg Found.'
    exit(1)
