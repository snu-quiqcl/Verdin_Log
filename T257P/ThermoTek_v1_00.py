# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 11:41:13 2017

@author: 1109282
"""
import ImportForSpyderAndQt5

from PyQt5 import QtWidgets
from .ThermoTekUI_v1_00 import Ui_ChillerControlDialog

class ChillerControlDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = Ui_ChillerControlDialog()
        self.ui.setupUi(self)
        
        self.parent = parent


    def chillerRunButtonClicked(self):
        chiller = self.parent.chiller
        if self.ui.chillerRunButton.text() == 'On':
            chiller.run()
            self.ui.chillerLabel.setText('Chiller ON')
            self.ui.chillerRunButton.setText('Off')
            QtWidgets.QMessageBox.information(self, 'Warning', \
                'Note: If the chiller status is requested right after the ' + \
                'chiller is turned on, IndexError exception is thrown. ' + \
                'Wait for about 10 seconds before requesting status.')
        else:
            chiller.standBy()
            self.ui.chillerLabel.setText('Chiller OFF')
            self.ui.chillerRunButton.setText('On')
            
        
    def setTempButtonClicked(self):
        chiller = self.parent.chiller
        newTemp = self.ui.setTempBox.value()
        chiller.setTemperature(newTemp)
            
        
    def updateButtonClicked(self):
        self.updateParameterStatus()


    def updateParameterStatus(self):
        """
        Note: If the status is requested right after the chiller is turn on,
            IndexError exception is thrown. Wait for at least 10 seconds
            before the status is requested.
        """

        chiller = self.parent.chiller
        
        status = chiller.query('U')
        self.ui.statusLabel.setText(chiller.statusMessage[status[0]])
        
        if status[1] == '0':
            self.ui.alarmLabel.setText('No Alarms')
        else:
            self.ui.alarmLabel.setText('Alarm ON')
            
        if status[2] == '0':
            self.ui.chillerLabel.setText('Chiller OFF')
            self.ui.chillerRunButton.setText('On')
        else:
            self.ui.chillerLabel.setText('Chiller ON')
            self.ui.chillerRunButton.setText('Off')

        if status[3] == '0':
            self.ui.dryerStatus.setText('Dryer OFF')
        else:
            self.ui.dryerStatus.setText('Dryer ON')

        self.ui.curTempLabel.setText(str(chiller.getCurrentTemperature()))
        self.ui.setTempBox.setValue(chiller.getSetTemperature())
        
