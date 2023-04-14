# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 11:41:13 2017

@author: 1109282
"""
import ImportForSpyderAndQt5


from PyQt5 import QtWidgets
from connectionDialog.connectionUI_v1_00 import Ui_ConnectionDialog

class VerdiConnectDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = Ui_ConnectionDialog()    
        self.ui.setupUi(self)
        self.setWindowTitle('Connection to Verdi')
        
        self.parent = parent
        
    def updateParameterStatus(self):
        verdi = self.parent.verdi
        self.ui.IPAddressEdit.setText(verdi.IPAddress)
        self.ui.TCPPortEdit.setText(str(verdi.TCPPort))
        if verdi.isConnected():
            buttonText = 'Disconnect'
            self.ui.statusLabel.setText('Connected')
        else:
            buttonText = 'Connect'
            self.ui.statusLabel.setText('Disconnected')
        self.ui.connectButton.setText(buttonText)
        
    def connectButtonClicked(self):
        verdi = self.parent.verdi
        if verdi.isConnected():
            verdi.disconnect()
            self.parent.enableSubMenus(self.parent.verdiMenuActionList, False)
            buttonText = 'Connect'
            self.ui.statusLabel.setText('Disconnected')
        else:
            verdi.IPAddress = self.ui.IPAddressEdit.text()
            verdi.TCPPort = int(self.ui.TCPPortEdit.text())
            try:
                verdi.connectToVerdi()
            except ConnectionRefusedError:
                QtWidgets.QMessageBox.critical(self, 'Error during connection', \
                    'Connection refused. Please check if the VerdiTCPServer is' +\
                    ' running and check IP address and port number.')
                return
            
            self.parent.enableSubMenus(self.parent.verdiMenuActionList, True)
            buttonText = 'Disonnect'
            self.ui.statusLabel.setText('Connected')
        self.ui.connectButton.setText(buttonText)

        #print('connectButtonClicked called')
        
        
