# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 11:41:13 2017

@author: 1109282
"""
import ImportForSpyderAndQt5


from PyQt5 import QtWidgets
from connectionDialog.connectionUI_v1_01 import Ui_ConnectionDialog

class ConnectDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, windowTitle = 'Connection to ...'):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = Ui_ConnectionDialog()    
        self.ui.setupUi(self)
        self.setWindowTitle(windowTitle)
        self.parent = parent
        
    def setDevice(self, device, TCPServerName):
        self.device = device
        self.TCPServerName = TCPServerName
        
    def setMenuActionList(self, menuActionList):
        self.menuActionList = menuActionList
        
    def updateParameterStatus(self):
        self.ui.IPAddressEdit.setText(self.device.IPAddress)
        self.ui.TCPPortEdit.setText(str(self.device.TCPPort))
        if self.device.isConnected():
            buttonText = 'Disconnect'
            self.ui.statusLabel.setText('Connected')
        else:
            buttonText = 'Connect'
            self.ui.statusLabel.setText('Disconnected')
            self.ui.deviceInfo.setText('')
        self.ui.connectButton.setText(buttonText)

    def updateMessage(self, message):
        self.ui.deviceInfo.setText(message)
        
    def connectButtonClicked(self):
        if self.device.isConnected():
            self.device.disconnect()
            self.parent.enableSubMenus(self.menuActionList, False)
            self.ui.deviceInfo.setText('')
            self.ui.connectButton.setText('Connect')
            self.ui.statusLabel.setText('Disconnected')
        else:
            self.device.IPAddress = self.ui.IPAddressEdit.text()
            self.device.TCPPort = int(self.ui.TCPPortEdit.text())
            try:
                connectionErrorMessage = self.device.connect()
                if connectionErrorMessage != None:
                    QtWidgets.QMessageBox.critical(self, 'Error during connection', \
                    connectionErrorMessage)
                    return
            except ConnectionRefusedError:
                QtWidgets.QMessageBox.critical(self, 'Error during connection', \
                    'Connection refused. Please check if %s is' +\
                    ' running and check IP address and port number.' % self.TCPServerName)
                return
            
            self.parent.enableSubMenus(self.menuActionList, True)
            self.ui.deviceInfo.setText(self.device.readID())
            self.ui.connectButton.setText('Disonnect')
            self.ui.statusLabel.setText('Connected')

        
        
