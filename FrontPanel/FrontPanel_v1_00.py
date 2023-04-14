# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 11:41:13 2017

@author: 1109282
"""

from PyQt5 import QtWidgets
from .FrontPanelUI_v1_00 import Ui_FrontPanelDialog

class FrontPanelDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, maxPower=13.0):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = Ui_FrontPanelDialog()
        self.ui.setupUi(self)
        self.ui.powerSetValue.setMaximum(maxPower)
        
        self.parent = parent

        
    def shutterButtonPressed(self):
        if self.ui.shutterStatusLabel.text() == 'Closed':
            self.parent.verdi.openShutter()
            self.ui.shutterStatusLabel.setText('Open')
            self.ui.shutterButton.setText('Close')
        else:
            self.parent.verdi.closeShutter()
            self.ui.shutterStatusLabel.setText('Closed')
            self.ui.shutterButton.setText('Open')
            
        #print('shutterButtonPressed called')
        
    def laserEnableButtonPressed(self):
        verdi = self.parent.verdi
        if verdi.query('K')[1] == '0':
            buttonReply = QtWidgets.QMessageBox.question(self, 'Warning', \
                'When key status is Off, laser actually does not start.' +\
                ' Do you still want to change laser status remotely?', \
                QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
            if buttonReply == QtWidgets.QMessageBox.No:
                return
            
        if self.ui.laserEnableStatus.text() == 'On':
            verdi.turnOffLaser()
            self.ui.laserEnableStatus.setText('Off')
            self.ui.laserEnableButton.setText('Turn on')
        else:
            verdi.turnOnLaser()
            self.ui.laserEnableStatus.setText('On')
            self.ui.laserEnableButton.setText('Turn off')
        #print('laserEnableButtonPressed called')
        
    def updateButtonPressed(self):
        self.updateParameterStatus()
        #print('updateButtonPressed')
        
    def powerSetButtonPressed(self):
        verdi = self.parent.verdi
        newPower = verdi._changePower(self.ui.powerSetValue.value())
        self.ui.powerSetValue.setValue(newPower)
        #print('powerSetButtonPressed')


    def updateParameterStatus(self):
        statusMessage = ''
        verdi = self.parent.verdi
        
        keyStatusText = 'On'
        laserEnableText = 'On'
        shutterText = 'Closed'

        laserLocked = False
        if verdi.query('K')[1] == '0':
            statusMessage += 'STANDBY by the keyswitch\n'
            keyStatusText = 'Off'
            laserEnableText = 'Off'
        elif verdi.query('L')[1] == '0':
            statusMessage += 'STANDBY by the RS232\n'
            laserEnableText = 'Off'
        elif verdi.query('S')[1] == '0':
            statusMessage += 'Shutter is closed\n'
        else:
            shutterText = 'Open'
            laserServoStatus = verdi.query('LRS')[1]
            if laserServoStatus == '2':
                statusMessage += "LASER Seeking\n"
            elif laserServoStatus  == '1':
                laserLocked = True

        self.ui.keyStatusLabel.setText(keyStatusText)
        self.ui.laserEnableStatus.setText(laserEnableText)
        if laserEnableText == 'On':
            self.ui.laserEnableButton.setText('Turn off')
        else:
            self.ui.laserEnableButton.setText('Turn on')
        self.ui.shutterStatusLabel.setText(shutterText)
        if shutterText == 'Closed':
            self.ui.shutterButton.setText('Open')
        else:
            self.ui.shutterButton.setText('Close')

        setPower = verdi.query('SP')[1]
        
        self.ui.powerSetValue.setValue(float(setPower))

        statusMessage += ('Set Power: %s (W)\nActual Power: %s (W)\n' % \
                          (setPower, verdi.query('P')[1]))
        statusMessage += ('Diode current: %s (A)\n' % verdi.query('C')[1])
        
        self.ui.textEdit.setText(statusMessage)

