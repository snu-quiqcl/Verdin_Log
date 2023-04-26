# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 16:30:35 2017

@author: 1109282
"""

from PyQt5 import QtWidgets
from .InformationDialogUI_v1_00 import Ui_informationDialog

class InformationDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = Ui_informationDialog()
        self.ui.setupUi(self)
        
        self.parent = parent

    def updateLaserStatus(self):
        self.setWindowTitle('Laser Status')
        statusMessage = ''
        verdi = self.parent.verdi

        statusMessage += ('P/S Ver: %s\n' % verdi.query('SV')[1])
        statusMessage += (' Baseplate Temp:   %sC\n' % verdi.query('BT')[1])
        statusMessage += ('Heatsink Temp 1:   %sC  2:   %sC\n' % (verdi.query('D1HST')[1],\
            verdi.query('D2HST')[1]))
        statusMessage += (' Hd Hrs:  %s\n' % verdi.query('HH')[1])
        statusMessage += (' D1 Hrs:  %s, I: %sA\n' % (verdi.query('D1H')[1],\
            verdi.query('D1C')[1]))
        statusMessage += (' D2 Hrs:  %s, I: %sA\n' % (verdi.query('D2H')[1],\
            verdi.query('D2C')[1]))
        statusMessage += ('Power Suply Hrs: %s\n' % verdi.query('PSH')[1])
        
        self.ui.textEdit.setText(statusMessage)



    def updateDiodeParameters(self):
        self.setWindowTitle('Diode Parameters')
        statusMessage = ''
        verdi = self.parent.verdi
        statusMessage += ('Diode 1 Current  :  %sA\n' % verdi.query('D1C')[1])
        statusMessage += ('Diode 1 Photocell:  %sV\n' % verdi.query('D1PC')[1])
        statusMessage += ('Diode 2 Current  :  %sA\n' % verdi.query('D2C')[1])
        statusMessage += ('Diode 2 Photocell:  %sV\n' % verdi.query('D2PC')[1])
        
        self.ui.textEdit.setText(statusMessage)

        
    def updateFaultStatus(self):
        self.setWindowTitle('Fault History')
        statusMessage = ''
        verdi = self.parent.verdi
        
        response = verdi.query('FH')[1]
        if response == 'SYSTEM OK':
            statusMessage = 'SYSTEM OK'
        else:
            faultList = map(int, response.split(','))
            #faultList = map(int, response.split('&'))
            """
            According to the manual, the list will be separated &, but it was
            not correct. Those numbers were separated by comma, and '?F'
            returned string list separated by &. See the following:
            - '?F' returns '4&6&7&10&44&48'
            - '?FH' returns '48,10,4,7,6,44'
            """
            for eachFault in faultList:
                    statusMessage += (verdi.faultStatusMsg[eachFault]+'\n')
        self.ui.textEdit.setText(statusMessage)


        
    def updateServoStatus(self):
        self.setWindowTitle('Servo Status')
        statusMessage = ''
        verdi = self.parent.verdi
        
        statusMessage += ('   Laser: %-10s %6sW %8s %7sW\n' % \
            verdi.getServoInfo('LRS', 'P', 'C', 'SP'))

        statusMessage += ('     LBO: %-10s %6sC %8s %7sC\n' % \
            verdi.getServoInfo('LBOSS', 'LBOT', 'LBOD', 'LBOST'))

        statusMessage += ('VANADATE: %-10s %6sC %8s %7sC\n' % \
            verdi.getServoInfo('VSS', 'VT', 'VD', 'VST'))

        statusMessage += ('  ETALON: %-10s %6sC %8s %7sC\n' % \
            verdi.getServoInfo('ESS', 'ET', 'ED', 'EST'))

        statusMessage += ('  DIODE1: %-10s %6sC %8s %7sC\n' % \
            verdi.getServoInfo('D1SS', 'D1T', 'D1TD', 'D1ST'))

        statusMessage += ('  DIODE2: %-10s %6sC %8s %7sC\n' % \
            verdi.getServoInfo('D2SS', 'D2T', 'D2TD', 'D2ST'))

        self.ui.textEdit.setText(statusMessage)


