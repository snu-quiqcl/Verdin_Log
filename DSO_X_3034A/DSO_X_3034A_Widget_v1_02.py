#!/usr/bin/python3
## -*- coding: utf-8 -*-

# This script is stored in O:/media/IonTrap/Device Control Scripts/Agilent DSO-X 3034A/new

# Change log
# v1_00: Initial version
# v2_00: To execute DSO_X_3034A object in a separate thread, QT signal is
#   added, and the structure is modified to accomodate separate thread


from __future__ import unicode_literals

import ImportForSpyderAndQt5


DEBUG = True


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
from DSO_X_3034A.OscilloscopeWidgetUI_v1_02 import Ui_OscilloscopeWidget
from DSO_X_3034A.DSO_X_3034A_TCPClient_v1_00 import DSO_X_3034A


progname = os.path.basename(sys.argv[0])
progversion = "0.1"

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


class DSO_X_3034A_Widget(QtWidgets.QWidget):
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


    def updateParameterStatus(self):
        if self.oscilloscope.isConnected():
            totalQuery = ':OPERegister:CONDition?;' + \
                ':TRIGger:SWEep?;' + \
                ':TRIGger:EDGE:SOURce?'
            status = self.oscilloscope.query(totalQuery)
            (OPERegister, triggerSweep, triggerEdgeSource) = status.split(';')
            
            if bin(int(OPERegister))[-4] == '0':
                self.ui.runStopButton.setChecked(False)
                self.ui.runStopStatus.setText('STOP')
            else:
                self.ui.runStopButton.setChecked(True)
                self.ui.runStopStatus.setText('RUN')
            self.ui.sweepModeComboBox.setCurrentText(triggerSweep)
            self.ui.triggerSourceComboBox.setCurrentText(triggerEdgeSource)
            
            self.deviceOpen = True
            self.isSingleRun = False
        
        

    def runStop(self, checked):
        if self.isSingleRun:
            self.singleClean('Aborted')
        if checked == True:
            if self.ui.sweepModeComboBox.currentText() == 'NORM':
                self.ui.updateButton.setEnabled(False)
                if self.autoUpdate:
                    self.autoUpdateTimer.stop()
                    self.autoUpdate = False
                    self.ui.autoUpdateButton.setChecked(False)
                self.ui.autoUpdateButton.setEnabled(False)
            self.oscilloscope.write(':RUN')
            self.ui.runStopStatus.setText('RUN')

        else:
            self.oscilloscope.write(':STOP')
            self.ui.runStopStatus.setText('STOP')
            self.ui.updateButton.setEnabled(True)
            self.ui.autoUpdateButton.setEnabled(True)
        
    def single(self):
        self.isSingleRun = True
        self.oscilloscope.query(':TER?') # Clear TER
        self.oscilloscope.write(':SINGle')
        if self.ui.runStopButton.isChecked():
            self.oscilloscope.query(':TER?') # Clear TER
            self.ui.runStopStatus.setText('STOP')
            self.ui.runStopButton.setChecked(False)
        self.prevSweepMode = self.ui.sweepModeComboBox.currentText()
        if self.prevSweepMode == 'AUTO':
            self.ui.sweepModeComboBox.setCurrentText('NORM')
        self.ui.singleButton.setChecked(True)
        self.ui.triggerStatus.setText('Armed')
        self.ui.sweepModeComboBox.setEnabled(False)
        self.ui.triggerSourceComboBox.setEnabled(False)
        self.ui.updateButton.setEnabled(False)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.checkTER)
        self.timer.setInterval(500)
        self.timer.start()
        
    def singleClean(self, triggerStatusMessage):
        self.timer.stop()
        self.isSingleRun = False
        self.ui.singleButton.setChecked(False)
        self.ui.sweepModeComboBox.setCurrentText(self.prevSweepMode)
        self.ui.triggerStatus.setText(triggerStatusMessage)
        self.ui.sweepModeComboBox.setEnabled(True)
        self.ui.triggerSourceComboBox.setEnabled(True)
        self.ui.updateButton.setEnabled(True)
        

    def checkTER(self):
        self.timer.setInterval(1500)
        triggerEventRegister = self.oscilloscope.query(':TER?')
        #print('triggerEventRegister:', triggerEventRegister)
        if triggerEventRegister == '+1':
            self.singleClean('Triggered')
        
    def sweepModeChanged(self, sweepMode):
        if sweepMode == 'AUTO':
            self.oscilloscope.triggerAuto(True)
            self.ui.updateButton.setEnabled(True)
            self.ui.autoUpdateButton.setEnabled(True)
        elif sweepMode == 'NORM':
            if self.ui.runStopStatus.text() == 'RUN':
                self.ui.updateButton.setEnabled(False)
                if self.autoUpdate:
                    self.autoUpdateTimer.stop()
                    self.autoUpdate = False
                    self.ui.autoUpdateButton.setChecked(False)
                self.ui.autoUpdateButton.setEnabled(False)
            self.oscilloscope.triggerAuto(False)
        else:
            print('Unknown sweep mode:', sweepMode)
        
    def triggerForced(self):
        self.oscilloscope.write(':TRIGger:FORCe')
        
    def triggerSourceChanged(self, source):
        self.oscilloscope.write(':TRIGger:EDGE:SOURce ' + source)


    def attachPlotToQWidget(self):
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
        self.line3 = Line2D(range(0, self.xpoints), [128]*self.xpoints, color='b')
        self.axes.add_line(self.line3)
        self.line4 = Line2D(range(0, self.xpoints), [128]*self.xpoints, color='r')
        self.axes.add_line(self.line4)

        self.lineList = (self.line1, self.line2, self.line3, self.line4)
        self.scaleList = (self.ui.ch1Y, self.ui.ch2Y, self.ui.ch3Y, self.ui.ch4Y)
        self.buttonList = (self.ui.pushButton_Ch1, self.ui.pushButton_Ch2,
                           self.ui.pushButton_Ch3, self.ui.pushButton_Ch4)

        self.canvas1 = FigureCanvas(self.fig)
        self.canvas1.setParent(self.ui.widget)
        self.canvas1.draw()

    def autoUpdate(self, checked):
        if checked:
            self.autoUpdateTimer = QtCore.QTimer()
            self.autoUpdateTimer.timeout.connect(self.updatePlot)
            self.autoUpdateTimer.setInterval(self.ui.updateIntervalSpinBox.value()*1000)
            self.autoUpdateTimer.start()            
            self.autoUpdate = True
        else:
            self.autoUpdateTimer.stop()
            self.autoUpdate = False

        
    def updatePlot(self):
        self.oscilloscope.readAllActiveData()
        self.drawPlot()
        
        if float(self.oscilloscope.chan1Freq) > 1e9:
            chan1FreqString = self.oscilloscope.chan1Freq
        else:
            chan1FreqString = makeFrequencyString(float(self.oscilloscope.chan1Freq))
        if float(self.oscilloscope.chan3DelayWRTChan2) > 1e9:
            chan3DelayWRTChan2String = self.oscilloscope.chan3DelayWRTChan2
        else:
            chan3DelayWRTChan2String = makeTimeString(self.oscilloscope.chan3DelayWRTChan2, 1)
        if float(self.oscilloscope.chan4DelayWRTChan2) > 1e9:
            chan4DelayWRTChan2String = self.oscilloscope.chan4DelayWRTChan2
        else:
            chan4DelayWRTChan2String = makeTimeString(self.oscilloscope.chan4DelayWRTChan2, 1)
            
        text = ('Ch1 Freq: %s\n' % chan1FreqString) + \
            ('Ch1 VPP: %s\n' % makeVoltageString(float(self.oscilloscope.chan1VPP))) + \
            ('Delay bet. Ch2 & Ch3: %s\n' % chan3DelayWRTChan2String) + \
            ('Delay bet. Ch2 & Ch4: %s\n' % chan4DelayWRTChan2String)
        self.ui.MeasurementLabel.setText(text)
    
    def drawPlot(self):
        xscale = self.oscilloscope.xscale
        self.ui.timebase.setText('    %s/' % makeTimeString(xscale, 0))
            
        for n in range(4):
            chYscale = self.oscilloscope.yscale[n]
            chLine = self.lineList[n]
            if self.buttonList[n].isChecked():
                self.scaleList[n].setText('%s/    ' % makeVoltageString(chYscale, 0))
                chLine.set_data(range(0, len(self.oscilloscope.ydata[n])), 
                                self.oscilloscope.ydata[n])
                chLine.set_visible(True)
            else:
                self.scaleList[n].setText('        ')
                chLine.set_visible(False)
        self.canvas1.draw()

    def closeEvent(self, event):
        if self.isSingleRun:
            self.singleClean('Aborted')
        buttonReply = QtWidgets.QMessageBox.question(self, 'Warning', \
            'The connection to the oscilloscope is still active. ' +\
            'The oscilloscope can be accessed by only one machine, ' +\
            'so when this machine is connected to the oscilloscope, ' +\
            'other machines cannot connect to this oscilloscope.\n\n' +\
            ' Do you want to keep the connection to the oscilloscope?', \
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        if buttonReply == QtWidgets.QMessageBox.No:
            self.oscilloscope.disconnect()
            self.parent.ui.actionOscilloscopeControl.setEnabled(False)
        QtWidgets.QWidget.closeEvent(self, event)
        
            
if __name__ == "__main__":
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
        
    oscilloscope = DSO_X_3034A(defaultIPAddress = '10.1.1.141', defaultTCPPort = 3034)
    MainWindow = DSO_X_3034A_Widget(None, oscilloscope)
    MainWindow.show()
    sys.exit(app.exec_())

