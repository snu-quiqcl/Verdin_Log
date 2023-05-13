# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 19:55:23 2023

@author: alexi
"""

import pyvisa
import time
import sys
import os
import numpy as np
import matplotlib
# Make sure that we are using QT5
matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.lines import Line2D

sys.path.insert(0, '..')
from TDS220.OscilloscopeWidgetUI_v1_02 import Ui_OscilloscopeWidget
from TDS220.TDS220_TCPClient_v1_00 import TDS220



class FIG_MAKE(QtWidgets.QWidget):
    def __init__(self, parent, device):
        QtWidgets.QWidget.__init__(self)        
        self.ui = Ui_OscilloscopeWidget()
        self.ui.setupUi(self)
        self.parent = parent
        self.oscilloscope = device

        self.xpoints = 1000
#        self.show()
        self.deviceOpen = False
        self.isSingleRun = False
        self.autoUpdate = False
        self.attachPlotToQWidget()
        self.channelOn = [True, True]
        self.yscale = [True, True]
        
    def attach_plot(self):
        self.fig = Figure(figsize=(4,3), dpi=100)
        self.axes = self.fig.add_subplot(111)
    
        self.axes.set_xlim(0, self.xpoints)
        self.axes.set_ylim(0, 256)
    
        self.axes.set_xticks(np.arange(0, self.xpoints+1, self.xpoints/10))
        self.axes.set_yticks(np.arange(0, 257, 32))
    
        self.axes.set_xticklabels([])
        self.axes.set_yticklabels([])
    
        self.axes.grid(which='both')
    
        # Adding curve to the plot
        self.line1 = Line2D(range(0, self.xpoints), [128]*self.xpoints, color='y')
        # http://matplotlib.org/api/artist_api.html#matplotlib.lines.Line2D
        self.axes.add_line(self.line1)
        self.line2 = Line2D(range(0, self.xpoints), [128]*self.xpoints, color='g')
        self.axes.add_line(self.line2)
    
        self.lineList = (self.line1, self.line2)
        self.scaleList = (self.ui.ch1Y, self.ui.ch2Y)
        self.buttonList = (self.ui.pushButton_Ch1, self.ui.pushButton_Ch2)
    
        self.canvas1 = FigureCanvas(self.fig)
        self.canvas1.setParent(self.ui.widget)
        self.canvas1.draw()

rm = pyvisa.ResourceManager()
inst = rm.open_resource('ASRL4')
inst.encoding = 'latin-1'

string_to_send = '*IDN?'
inst.write(string_to_send)
#inst.timeout = 50000
a = inst.read()
print(a)

string_to_send = 'ACQuire?'
inst.write(string_to_send)
a = inst.read()
print(a)

inst.write('SELECT:CH1 ON')
inst.write('ACQUire:MODe SAMPLE')
inst.write('ACQUire:STOPAFTER SEQUENCE')
inst.write('ACQUire:STATE ON')
inst.write('MEASUrement:IMMed:TYPe FREQuency')
inst.write('MEASUrement:IMMed:SOUrce CH1')  
inst.write('MEASUrement:IMMed:VALUE?')
chan1Freq = float(inst.read())
print(chan1Freq)

inst.close()

"""
inst.write('MEASUrement:IMMed:TYPe PK2pk') 
inst.write('MEASUrement:IMMed:SOUrce CH1')  
inst.write('MEASUrement:IMMed:VALUE?')
chan1VPP = float(inst.read())/2

inst.write('SELECT:CH2 ON')
inst.write('ACQUire:MODe SAMPLE')
inst.write('ACQUire:STOPAFTER SEQUENCE')
inst.write('ACQUire:STATE ON')
inst.write('MEASUrement:IMMed:TYPe FREQuency')
inst.write('MEASUrement:IMMed:SOUrce CH2')  
inst.write('MEASUrement:IMMed:VALUE?')
chan2Freq = float(inst.read())
inst.write('MEASUrement:IMMed:TYPe PK2pk') 
inst.write('MEASUrement:IMMed:SOUrce CH2')  
inst.write('MEASUrement:IMMed:VALUE?')
chan2VPP = float(inst.read())/2

inst.write('WFMPre:NR_PT?')
xscale = inst.read()   
print(chan1Freq)
print(chan1VPP)
print(chan2Freq)
print(chan2VPP)
print(xscale)
    
    
inst.write('DATA:SOU CH1')
inst.write('DATA:WIDTH 1')
inst.write('DATA:ENC RPB')

inst.write('WFMPRE:YMULT?')
ans = inst.read()
ymult = float(ans)
print(ymult)

inst.write('WFMPRE:YZERO?')
ans = inst.read()
yzero = float(ans)
print(yzero)

inst.write('WFMPRE:YOFF?')
ans = inst.read()
yoff = float(ans)
print(yoff)

inst.write('WFMPRE:XINCR?')
ans = inst.read()
xincr = float(ans)
print(xincr)


inst.write('ACQuire:MODe:SAMPLE')
inst.write('CURVE?')
data = inst.read_raw(16)
print(data)
ADC_wave = data[headerlen:-1]

ADC_wave = np.array(unpack('%sB' % len(ADC_wave),ADC_wave))
ADC_wave = ADC_wave[0:len(ADC_wave)-2]

Volts = (ADC_wave - yoff) * ymult  + yzero

Time = np.arange(0, xincr * len(Volts), xincr)

Volts = Volts.tolist()
Time = Time.tolist()

xscale = xincr
#self.ui.timebase.setText('    %s/' % makeTimeString(xscale, 0))
    
chYscale = ymult
chLine = 

#self.scaleList[n].setText('%s/    ' % makeVoltageString(chYscale, 0))
chLine.set_data(range(0, len(Volts)), Volts)
chLine.set_visible(True)

canvas1.draw()
        
inst.close()
"""