# -*- coding: utf-8 -*-
"""
Created on Fri Dec 29 14:26:41 2017

@author: 1109282
"""

chan1Freq = '77000000.0'

def makeFrequencyString(freq):
    if (freq < 1e3 ):
        return ('%.1f Hz' % freq)
    elif (freq < 1e6 ):
        return ('%.1f kHz' % (freq/1e3))
    else:
        return ('%.1f MHz' % (freq/1e6))

def makeVoltageString(volt, numberOfDigitAfterDecimalPoint = 1):
    format = '%%.%df' % numberOfDigitAfterDecimalPoint
    if volt < 1.0:
        return ((format +'mV') % (volt*1e3))
    else:
        return ((format +'V') % volt)

def makeTimeString(timeValue, numberOfDigitAfterDecimalPoint = 0):
    format = '%%.%df' % numberOfDigitAfterDecimalPoint
    if timeValue >= 1.0:
        return ((format + 's') % timeValue)
    elif timeValue >= 1.0e-3:
        return ((format + 'ms') % (timeValue*1e3))
    elif timeValue >= 1.0e-6:
        return ((format + 'us') % (timeValue*1e6))
    else:
        return ((format + 'ns') % (timeValue*1e9))

    
makeFrequencyString(float('770.0'))
makeVoltageString(float('4.4'),0)
makeTimeString(float('50e-9'))

makeVoltageString(0.1, 0)
'%%.%df' % 0

'%.0f' % 100

