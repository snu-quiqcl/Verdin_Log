# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 11:41:13 2017

@author: 1109282
"""
import ImportForSpyderAndQt5


from PyQt5 import QtWidgets
from connectionDialog.connectionUI_v1_00 import Ui_ConnectionDialog

class ThermoTekConnectDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = Ui_ConnectionDialog()    
        self.ui.setupUi(self)
        self.setWindowTitle('Connection to Chiller')
        
        self.parent = parent
        
    def updateParameterStatus(self):
        chiller = self.parent.chiller
        self.ui.IPAddressEdit.setText(chiller.IPAddress)
        self.ui.TCPPortEdit.setText(str(chiller.TCPPort))
        if chiller.isConnected():
            buttonText = 'Disconnect'
            self.ui.statusLabel.setText('Connected')
        else:
            buttonText = 'Connect'
            self.ui.statusLabel.setText('Disconnected')
        self.ui.connectButton.setText(buttonText)
        
    def connectButtonClicked(self):
        chiller = self.parent.chiller
        if chiller.isConnected():
            chiller.disconnect()
            self.parent.enableSubMenus(self.parent.chillerMenuActionList, False)
            buttonText = 'Connect'
            self.ui.statusLabel.setText('Disconnected')
        else:
            chiller.IPAddress = self.ui.IPAddressEdit.text()
            chiller.TCPPort = int(self.ui.TCPPortEdit.text())
            try:
                chiller.connectToThermoTek()
            except ConnectionRefusedError:
                QtWidgets.QMessageBox.critical(self, 'Error during connection', \
                    'Connection refused. Please check if the ThermoTekTCPServer is' +\
                    ' running and check IP address and port number.')
                return
            self.parent.enableSubMenus(self.parent.chillerMenuActionList, True)
            buttonText = 'Disonnect'
            self.ui.statusLabel.setText('Connected')
        self.ui.connectButton.setText(buttonText)

        #print('connectButtonClicked called')
        
        
