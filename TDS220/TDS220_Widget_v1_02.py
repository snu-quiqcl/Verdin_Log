#!/usr/bin/python3
## -*- coding: utf-8 -*-

# This script is stored in O:/media/IonTrap/Device Control Scripts/Agilent DSO-X 3034A/new

# Change log
# v1_00: Initial version
# v2_00: To execute TDS220 object in a separate thread, QT signal is
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
from TDS220.OscilloscopeWidgetUI_v1_02 import Ui_OscilloscopeWidget
from TDS220.TDS220_TCPClient_v1_00 import TDS220
from TDS220.TDS220_Logger_v1_00 import TDS220_Logger as logger
from threading import Thread, Event, Lock
import time
import math

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
    if volt < 1e-6:
        return ((format +'uV') % (volt*1e9))
    elif volt < 1e-3:
        return ((format +'uV') % (volt*1e6))
    elif volt < 1.0:
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


class TDS220_Widget(QtWidgets.QWidget):
    def __init__(self, parent, device):
        QtWidgets.QWidget.__init__(self)        
        self.ui = Ui_OscilloscopeWidget()
        self.ui.setupUi(self)
        self.parent = parent
        self.oscilloscope = device

        self.xpoints = 2450
#        self.show()
        self.deviceOpen = False
        self.isSingleRun = False
        self.autoUpdate = False
        self.attachPlotToQWidget()
        self.trigger_value = 0
        self.trigger_mul = 1
        self.timer = QtCore.QTimer()
        #self.timer.timeout.connect(self.checkTER)
        self.timer.setInterval(500)
        self.timer.start()
        self.buttonList_ = [self.ui.pushButton_Ch1, self.ui.pushButton_Ch2, \
                            self.ui.runStopButton, self.ui.singleButton, \
                            self.ui.triggerForceButton, self.ui.SetTriggerLevel, \
                            self.ui.updateButton, self.ui.CH1_DC, self.ui.CH2_DC, \
                            self.ui.CH1_AC, self.ui.CH2_AC, self.ui.CH1_GND,\
                            self.ui.LOG_START, self.ui.CH2_GND, self.ui.autoUpdateButton]
        self.event = Event()
        self.event.clear()
        self.auto_update_thread = Thread(target=self.updatePlot_caller)
        self.auto_update_thread.start()
        self.horizontal_scale_list = [[1,2.5,5],[1e-9,1e-8,1e-7,1e-6,1e-5,1e-4,\
                                    1e-3,1e-2,1e-1,1],['1','2.5','5'],['E-9',\
                                    'E-8','E-7','E-6','E-5','E-4','E-3','E-2',\
                                    'E-1','']]
        self.current_horizontal_scale = [0,0]
        self.volts_scale_list = [[1,2.5,5],[1e-3,1e-2,1e-1,1],['1','2.5',\
                                    '5'],['E-3','E-2','E-1','']]
        self.current_CH1_volts_scale = [0,0]
        self.current_CH2_volts_scale = [0,0]
        self.logger = logger(self)


    def updateParameterStatus(self):
        if self.oscilloscope.isConnected():
            totalQuery = ':TRIGger:MAIn:EDGE:SOURce?'
            status = self.oscilloscope.query(totalQuery)
            (triggerEdgeSource) = status
            #SELect:CH1? -> 0 OFF or 1 ON
            totalQuery = ':SELect:CH1?;:SELect:CH2?;'
            [ch1on, ch2on] = self.oscilloscope.query(totalQuery).split(';')
            if ch1on == '0':
                self.oscilloscope.channelOn[0] = False
                self.ui.pushButton_Ch1.setChecked(False)
            else:
                self.oscilloscope.channelOn[0] = True
                self.ui.pushButton_Ch1.setChecked(True)
                
            if ch2on == '0':
                self.oscilloscope.channelOn[1] = False
                self.ui.pushButton_Ch2.setChecked(False)
            else:
                self.oscilloscope.channelOn[1] = True
                self.ui.pushButton_Ch2.setChecked(True)
            
            self.ui.triggerSourceComboBox.setCurrentText(triggerEdgeSource)
            #CH1 , CH2 button setting
            totalQuery = ':HORizontal:MAIn:SCAle?;'
            [horiz_scale] = self.oscilloscope.query(totalQuery).split(';')
            print(horiz_scale)
            for i_ in range(len(self.horizontal_scale_list[0])):
                for j_ in range(len(self.horizontal_scale_list[1])):
                    if float(horiz_scale) == self.horizontal_scale_list[0][i_]\
                        * self.horizontal_scale_list[1][j_]:
                            self.current_horizontal_scale = [i_,j_]
            
            self.ui.HorizontalScale_Val.display(self.volts_scale_list[0][self.current_CH1_volts_scale[0]] *
                                           self.volts_scale_list[1][self.current_CH1_volts_scale[1]])
                            
            totalQuery = ':CH1:SCAle?;'
            [ch1_scale] = self.oscilloscope.query(totalQuery).split(';')
            print(ch1_scale)
            for i_ in range(len(self.volts_scale_list[0])):
                for j_ in range(len(self.volts_scale_list[1])):
                    if float(horiz_scale) == self.volts_scale_list[0][i_]\
                        * self.volts_scale_list[1][j_]:
                            self.current_CH1_volts_scale = [i_,j_]
                            
            self.ui.CH1_VoltsScale_Val.display(self.volts_scale_list[0][self.current_CH1_volts_scale[0]] *
                                           self.volts_scale_list[1][self.current_CH1_volts_scale[1]])
                            
            totalQuery = ':CH2:SCAle?;'
            [ch2_scale] = self.oscilloscope.query(totalQuery).split(';')
            print(ch2_scale)
            for i_ in range(len(self.volts_scale_list[0])):
                for j_ in range(len(self.volts_scale_list[1])):
                    if float(horiz_scale) == self.volts_scale_list[0][i_]\
                        * self.volts_scale_list[1][j_]:
                            self.current_CH2_volts_scale = [i_,j_]
            
            self.ui.CH2_VoltsScale_Val.display(self.volts_scale_list[0][self.current_CH2_volts_scale[0]] *
                                           self.volts_scale_list[1][self.current_CH2_volts_scale[1]])
            
            self.deviceOpen = True
            self.isSingleRun = False
        
        

    def runStop(self, checked):
        if self.isSingleRun:
            self.singleClean('Aborted')
        if checked == True:
            self.ui.updateButton.setEnabled(False)
            if self.autoUpdate:
                self.autoUpdateTimer.stop()
                self.autoUpdate = False
                self.ui.autoUpdateButton.setChecked(False)
            self.ui.autoUpdateButton.setEnabled(False)
            self.oscilloscope.write('ACQuire:STATE RUN')
            self.ui.runStopStatus.setText('RUN')

        else:
            self.oscilloscope.write('ACQuire:STATE STOP')
            self.ui.runStopStatus.setText('STOP')
            self.ui.updateButton.setEnabled(True)
            self.ui.autoUpdateButton.setEnabled(True)
        
    def single(self):
        self.isSingleRun = True
        self.oscilloscope.write(':ACQUire:STOPAFTER RUNSTop')
        if self.ui.runStopButton.isChecked():
            self.ui.runStopStatus.setText('STOP')
            self.ui.runStopButton.setChecked(False)
        self.ui.singleButton.setChecked(True)
        self.ui.triggerStatus.setText('Armed')
        self.ui.triggerSourceComboBox.setEnabled(False)
        self.ui.updateButton.setEnabled(False)
        
    def singleClean(self, triggerStatusMessage):
        self.timer.stop()
        self.isSingleRun = False
        self.ui.singleButton.setChecked(False)
        self.ui.triggerStatus.setText(triggerStatusMessage)
        self.ui.triggerSourceComboBox.setEnabled(True)
        self.ui.updateButton.setEnabled(True)
    
    def AutoSet(self):
        self.oscilloscope.write(':AUTOSet EXECUTE')
        
    def triggerForced(self):
        self.oscilloscope.write(':TRIGger FORCe')
        
    def triggerSourceChanged(self, source):
        self.oscilloscope.write(':TRIGger:MAIn:EDGE:SOURce ' + source)
        
    def set_triggerLevel(self):
        trigger_str = str(self.trigger_value)
        self.oscilloscope.write('TRIGger:MAIn:LEVel ' + trigger_str)
        
    def triggerLevelChanged_Scroll(self,trigger_value):
        self.trigger_value = (trigger_value - 500 ) * self.trigger_mul / 1000
        self.ui.TriggerLevelText.setValue(self.trigger_value)
        print(self.trigger_value)
        
    def triggerLevelChanged_TextBox(self,trigger_value):
        self.trigger_value = trigger_value
        self.ui.TriggerLevelScroll.setValue(max(min(500 + round(self.trigger_value * 1000 / self.trigger_mul), 1000),0))
        print(self.trigger_value)
        
    def ScrollTriggerMulInc(self):
        self.trigger_mul = self.trigger_mul + 1
        self.ui.TriggerLevelMul.display(self.trigger_mul)
        print(self.trigger_mul)
        
    def ScrollTriggerMulDec(self):
        if self.trigger_mul > 1:
            self.trigger_mul = self.trigger_mul - 1
            self.ui.TriggerLevelMul.display(self.trigger_mul)
        else:
            print('trigger_mul should be bigger or equal to 1')
            
        print(self.trigger_mul)
            
    def set_Ch1(self):
        if self.ui.pushButton_Ch1.isChecked():
            self.oscilloscope.channelOn[0] = True
            self.oscilloscope.write(':SELECT:CH1 ON')
        else:
            self.oscilloscope.channelOn[0] = False
            self.oscilloscope.write(':SELECT:CH1 OFF')
            
    def set_Ch2(self):
        if self.ui.pushButton_Ch2.isChecked():
            self.oscilloscope.channelOn[1] = True
            self.oscilloscope.write(':SELECT:CH2 ON')
        else:
            self.oscilloscope.channelOn[1] = False
            self.oscilloscope.write(':SELECT:CH2 OFF')
            
    def CH1_VoltsScaleIncrease(self):
        if self.current_CH1_volts_scale[0] == 2 and \
            self.current_CH1_volts_scale[1] == len(self.volts_scale_list):
            return
        
        self.current_CH1_volts_scale[0] = self.current_CH1_volts_scale[0] + 1
        if self.current_CH1_volts_scale[0] > 2:
            self.current_CH1_volts_scale[0] = 0
            self.current_CH1_volts_scale[1] = self.current_CH1_volts_scale[1] + 1
        
        self.oscilloscope.write(':CH1:SCALE '+self.volts_scale_list[2][self.current_CH1_volts_scale[0]]\
                                +self.volts_scale_list[3][self.current_CH1_volts_scale[1]]+';')
        
        self.ui.CH1_VoltsScale_Val.display(self.volts_scale_list[0][self.current_CH1_volts_scale[0]] *
                                       self.volts_scale_list[1][self.current_CH1_volts_scale[1]])
    def CH1_VoltsScaleDecrease(self):
        if self.current_CH1_volts_scale[0] == 2 and self.current_CH1_volts_scale[1] == 0:
            return
        
        self.current_CH1_volts_scale[0] = self.current_CH1_volts_scale[0] - 1
        if self.current_CH1_volts_scale[0] < 0:
            self.current_CH1_volts_scale[0] = 2
            self.current_CH1_volts_scale[1] = self.current_CH1_volts_scale[1] - 1
        
        self.oscilloscope.write(':CH1:SCALE '+self.volts_scale_list[2][self.current_CH1_volts_scale[0]]\
                                +self.volts_scale_list[3][self.current_CH1_volts_scale[1]]+';')
        
        self.ui.CH1_VoltsScale_Val.display(self.volts_scale_list[0][self.current_CH2_volts_scale[0]] *
                                       self.volts_scale_list[1][self.current_CH2_volts_scale[1]])
    def CH2_VoltsScaleIncrease(self):
        if self.current_CH2_volts_scale[0] == 2 and \
            self.current_CH2_volts_scale[1] == len(self.volts_scale_list):
            return
        
        self.current_CH2_volts_scale[0] = self.current_CH2_volts_scale[0] + 1
        if self.current_CH2_volts_scale[0] > 2:
            self.current_CH2_volts_scale[0] = 0
            self.current_CH2_volts_scale[1] = self.current_CH2_volts_scale[1] + 1
        
        self.oscilloscope.write(':CH2:SCALE '+self.volts_scale_list[2][self.current_CH2_volts_scale[0]]\
                                +self.volts_scale_list[3][self.current_CH2_volts_scale[1]]+';')
        
        self.ui.CH2_VoltsScale_Val.display(self.volts_scale_list[0][self.current_CH2_volts_scale[0]] *
                                       self.volts_scale_list[1][self.current_CH2_volts_scale[1]])
    def CH2_VoltsScaleDecrease(self):
        if self.current_CH2_volts_scale[0] == 2 and self.current_CH2_volts_scale[1] == 0:
            return
        
        self.current_CH2_volts_scale[0] = self.current_CH2_volts_scale[0] - 1
        if self.current_CH2_volts_scale[0] < 0:
            self.current_CH2_volts_scale[0] = 2
            self.current_CH2_volts_scale[1] = self.current_CH2_volts_scale[1] - 1
        
        self.oscilloscope.write(':CH2:SCALE '+self.volts_scale_list[2][self.current_CH2_volts_scale[0]]\
                                +self.volts_scale_list[3][self.current_CH2_volts_scale[1]]+';')
        
        self.ui.CH2_VoltsScale_Val.display(self.volts_scale_list[0][self.current_CH2_volts_scale[0]] *
                                       self.volts_scale_list[1][self.current_CH2_volts_scale[1]])
    def HorizontalScaleDecrease(self):
        if self.current_horizontal_scale[0] == 2 and self.current_horizontal_scale[1] == 0:
            return
        
        self.current_horizontal_scale[0] = self.current_horizontal_scale[0] - 1
        if self.current_horizontal_scale[0] < 0:
            self.current_horizontal_scale[0] = 2
            self.current_horizontal_scale[1] = self.current_horizontal_scale[1] - 1
        
        self.oscilloscope.write(':HORIZONTAL:SCALE '+self.horizontal_scale_list[2][self.current_horizontal_scale[0]]\
                                +self.horizontal_scale_list[3][self.current_horizontal_scale[1]]+';')
        
        self.ui.CH2_VoltsScale_Val.display(self.horizontal_scale_list[0][self.current_horizontal_scale[0]] *
                                       self.horizontal_scale_list[1][self.current_horizontal_scale[1]])
    
    def HorizontalScaleIncrease(self):
        if self.current_horizontal_scale[1] == len(self.horizontal_scale_list[1]) - 1 \
            and self.current_horizontal_scale[0] == len(self.horizontal_scale_list[0]) - 1:
            return
        
        self.current_horizontal_scale[0] = self.current_horizontal_scale[0] + 1
        if self.current_horizontal_scale[0] > 2:
            self.current_horizontal_scale[0] = 0
            self.current_horizontal_scale[1] = self.current_horizontal_scale[1] + 1
        
        self.oscilloscope.write(':HORIZONTAL:SCALE '+self.horizontal_scale_list[2][self.current_horizontal_scale[0]]\
                                +self.horizontal_scale_list[3][self.current_horizontal_scale[1]]+';')
        
        self.ui.HorizontalScale_Val.display(self.horizontal_scale_list[0][self.current_horizontal_scale[0]] *
                                       self.horizontal_scale_list[1][self.current_horizontal_scale[1]])
            
    def set_CH1_AC(self):
        self.oscilloscope.write(':CH1:COUPLing AC;')
    def set_CH1_DC(self):
        self.oscilloscope.write(':CH1:COUPLing DC;')
    def set_CH1_GND(self):
        self.oscilloscope.write(':CH1:COUPLing GND;')
    def set_CH2_AC(self):
        self.oscilloscope.write(':CH2:COUPLing AC;')
    def set_CH2_DC(self):
        self.oscilloscope.write(':CH2:COUPLing DC;')
    def set_CH2_GND(self):
        self.oscilloscope.write(':CH2:COUPLing GND;')
    def Log_Start(self):
        if not self.logger.log_running():
            for button in self.buttonList_:
                if not button == self.ui.LOG_START:
                    button.setDisabled(True)
            self.logger.start_log()
            #auto update code should be updated
            self.ui.setText('LOGGING')
        else:
            self.logger.end_log()
            for button in self.buttonList_:
                if not button == self.ui.LOG_START:
                    button.setDisabled(False)
            self.ui.setText('STOP')

    def attachPlotToQWidget(self):
        self.fig = Figure(figsize=(4,3), dpi=100)
        self.axes = self.fig.add_subplot(111)

        self.axes.set_xlim(0, self.xpoints)
        # xpoints value?
        self.axes.set_ylim(-256, 256)

        self.axes.set_xticks(np.arange(0, self.xpoints+1, self.xpoints/10))
        self.axes.set_yticks(np.arange(-257, 257, 32))

        self.axes.set_xticklabels([])
        self.axes.set_yticklabels([])

        self.axes.grid(which='both')

        # Adding curve to the plot
        self.line1 = Line2D(range(0, self.xpoints), [128]*self.xpoints, color='r')
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

    def autoUpdate(self, checked):
        if checked:       
            self.event.set()
            self.autoUpdate = True
            self.ui.autoUpdateButton.setChecked(True)
            for button in self.buttonList_:
                if not button == self.ui.autoUpdateButton:
                    button.setDisabled(True)
        else:
            self.event.clear()
            self.autoUpdate = False
            self.ui.autoUpdateButton.setChecked(False)
            for button in self.buttonList_:
                if not button == self.ui.autoUpdateButton:
                    button.setDisabled(False)
                
    def updatePlot_caller(self):
        index_ = 0
        while True:
            self.event.wait()
            if index_ == 0:
                time.sleep(self.ui.updateIntervalSpinBox.value() - \
                           math.floor(self.ui.updateIntervalSpinBox.value()))
                self.updatePlot()
            else:
                time.sleep(1)
            index_ = ( index_ + 1 ) % math.floor(self.ui.updateIntervalSpinBox.value() + 1)

        
    def updatePlot(self):
        if self.autoUpdate == False:
            for button in self.buttonList_:
                button.setDisabled(True)
            self.ui.autoUpdateButton.setDisabled(True)
            
        self.oscilloscope.readAllActiveData()
        self.drawPlot()
        
        if float(self.oscilloscope.chan1Freq) > 1e9:
            chan1FreqString = self.oscilloscope.chan1Freq
        else:
            chan1FreqString = makeFrequencyString(float(self.oscilloscope.chan1Freq))
            
        if float(self.oscilloscope.chan2Freq) > 1e9:
            chan2FreqString = self.oscilloscope.chan2Freq
        else:
            chan2FreqString = makeFrequencyString(float(self.oscilloscope.chan2Freq))
        
        text = ('Ch1 Freq: %s\n' % chan1FreqString) + \
            ('Ch1 VPk2Pk: %s\n' % makeVoltageString(float(self.oscilloscope.chan1VPP))) + \
            ('Ch2 Freq: %s\n' % chan2FreqString) + \
            ('Ch2 VPk2Pk: %s\n' % makeVoltageString(float(self.oscilloscope.chan2VPP)))
        self.ui.MeasurementLabel.setText(text)
        
        if self.autoUpdate == False:
            for button in self.buttonList_:
                button.setDisabled(False)
            self.ui.autoUpdateButton.setDisabled(False)
    
    def drawPlot(self):
        xscale = self.oscilloscope.xscale
        self.ui.timebase.setText('    %s/' % makeTimeString(xscale, 0))
            
        for n in range(2):
            chYscale = self.oscilloscope.yscale[n]
            chLine = self.lineList[n]
            if self.buttonList[n].isChecked():
                self.scaleList[n].setText('%s/DIV' % makeVoltageString(chYscale, 0))
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
        
    oscilloscope = TDS220(defaultIPAddress = '10.1.1.141', defaultTCPPort = 3034)
    MainWindow = TDS220_Widget(None, oscilloscope)
    MainWindow.show()
    sys.exit(app.exec_())

