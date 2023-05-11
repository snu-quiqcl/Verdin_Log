#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
This script is stored in O:\Device Manuals and Data\???

Change log
v0_00: Initial version

"""
import ImportForSpyderAndQt5

import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt

from MiraControlUI_v1_02 import Ui_MainWindow

#Verdi CW green laser
from VerdiConnection_v1_00 import VerdiConnectDialog
from FrontPanel.FrontPanel_v1_00 import FrontPanelDialog
from InformationDialog.InformationDialog_v1_00 import InformationDialog
import V18.Verdi_v1_02 as Verdi

#ThermoTek Chiller
from ThermoTekConnection_v1_00 import ThermoTekConnectDialog
from ThermoTek.ThermoTek_v1_00 import ChillerControlDialog
import ThermoTek.ThermoTek_T255P_v1_00 as T255P

from ConnectionDialogWidget_v1_00 import ConnectDialog
#Oscilloscope
from TDS220.TDS220_TCPClient_v1_00 import TDS220
from TDS220.TDS220_Widget_v1_02 import TDS220_Widget
from V18.Verdi_logger_v1_02 import Verdi_Logger

#import BME280.Adafruit_BME280 as AF_BME280
#from meteocalc import Temp as TemperatureClass
#from meteocalc import dew_point as calcuateDewpoint

DEBUG = True
Verdi.DEBUG = False
T255P.DEBUG = False




class MiraControlMainWindow(QtWidgets.QMainWindow):
    
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        ###################################################################
        ## Settings for Coherent Verdi-18
        ###################################################################
        self.verdiMenuActionList = [self.ui.actionDiode_Parameters, \
            self.ui.actionFault_Status, self.ui.actionFront_Panel, \
            self.ui.actionLaser_Status, self.ui.actionServo_Status,\
            self.ui.actionVerdi_Log_Start, self.ui.menuVerdi_Log]
        
        self.verdi = Verdi.Verdi()

        self.verdiConnectionDialog = VerdiConnectDialog(self)    
        self.frontPanelDialog = FrontPanelDialog(self)
        self.informationDialog = InformationDialog(self)
        self.verdi_Logger = Verdi_Logger(self)

        ###################################################################
        ## Settings for ThermoTek chiller
        ###################################################################
        self.chillerMenuActionList = [self.ui.actionChiller_Control]
        
        self.chiller = T255P.T255P()

        self.chillerConnectionDialog = ThermoTekConnectDialog(self)
        self.chillerControlDialog = ChillerControlDialog(self)
        
        ###################################################################
        ## Settings for DSO-X-3034A
        ###################################################################
        
        #self.oscilloscope = DSO_X_3034A(defaultIPAddress = '10.1.1.141', defaultTCPPort = 3034)
        #self.oscilloscopeConnectionDialog = ConnectDialog(self, windowTitle = 'Connection to DSO3034A')
        #self.oscilloscopeConnectionDialog.setDevice(self.oscilloscope, 'DSO_X_3034A_TCPServer_v2_00.py')
        #self.oscilloscopeConnectionDialog.setMenuActionList([self.ui.actionOscilloscopeControl])
        #self.oscilloscopeWidget = DSO_X_3034A_Widget(self, self.oscilloscope)
        #self.oscilloscope.setWidget(self.oscilloscopeWidget)
        #self.oscilloscopeWidget.hide()
        
        ###################################################################
        ## Settings for TDS220
        ###################################################################
        
        self.oscilloscope = TDS220(defaultIPAddress = '172.22.22.86', defaultTCPPort = 3034)
        self.oscilloscopeConnectionDialog = ConnectDialog(self, windowTitle = 'Connection to DSO3034A')
        self.oscilloscopeConnectionDialog.setDevice(self.oscilloscope, 'TDS220_TCPServer_v2_00.py')
        self.oscilloscopeConnectionDialog.setMenuActionList([self.ui.actionOscilloscopeControl])
        self.oscilloscopeWidget = TDS220_Widget(self, self.oscilloscope)
        self.oscilloscope.setWidget(self.oscilloscopeWidget)
        self.oscilloscopeWidget.hide()
        

    ###################################################################
    ## Methods related to Coherent Verdi-18
    ###################################################################
        
    def openVerdiConnection(self):
        #print('openVerdiConnection called')
        self.verdiConnectionDialog.updateParameterStatus()
        #self.verdiConnectionDialog.exec_()
        self.verdiConnectionDialog.show()
        
        
    def openVerdiFrontPanel(self):
        self.frontPanelDialog.updateParameterStatus()
        #self.frontPanelDialog.exec_()
        self.frontPanelDialog.show()
    
    def openVerdiLaserStatus(self):
        self.informationDialog.updateLaserStatus()
        self.informationDialog.exec_()
        
    def openVerdiDiodeParameters(self):
        self.informationDialog.updateDiodeParameters()
        self.informationDialog.exec_()
        
    def openVerdiFaultStatus(self):
        self.informationDialog.updateFaultStatus()
        self.informationDialog.exec_()
        
    def openVerdiServoStatus(self):
        self.informationDialog.updateServoStatus()
        self.informationDialog.exec_()
        
    def openVerdi_Log_Start(self):
        print('Verdi Log Start')
        self.verdi_Logger.start_log()
        self.ui.actionVerdi_Log_Start.setEnabled(False)
        self.ui.actionVerdi_Log_End.setEnabled(True)
        
    def openVerdi_Log_End(self):
        print('Verdi Log End')
        self.verdi_Logger.end_log()
        self.ui.actionVerdi_Log_End.setEnabled(False)
        self.ui.actionVerdi_Log_Start.setEnabled(True)


    ###################################################################
    ## Methods related to ThermoTek chiller
    ###################################################################
    def openChillerConnection(self):
        self.chillerConnectionDialog.updateParameterStatus()
        #self.chillerConnectionDialog.exec_()
        self.chillerConnectionDialog.show()
        
    def openChillerControlPanel(self):
        self.chillerControlDialog.updateParameterStatus()
        #self.chillerControlDialog.exec_()
        self.chillerControlDialog.show()

    ###################################################################
    ## Methods related to DSO-X-3034A
    ###################################################################
    def openTDS220_Connection(self):
        self.oscilloscopeConnectionDialog.updateParameterStatus()
        self.oscilloscopeConnectionDialog.show()
        #self.oscilloscopeConnectionDialog.exec_()
 
       
    def openOscilloscopeControl(self):
        self.oscilloscopeWidget.updateParameterStatus()
        self.oscilloscopeWidget.show()


    ###################################################################
    ## Methods common to all devices
    ###################################################################
    def enableSubMenus(self, menuActionList, enable = True):
        for eachAction in menuActionList:
            eachAction.setEnabled(enable)
        
        if enable == False:
            self.ui.actionVerdi_Log_Start.setEnabled(True)
        
        if enable == True:
            self.ui.actionVerdi_Log_End.setEnabled(False)
        

        
    def closeEvent(self, event):
        if self.verdi_Logger.log_running():
            buttonReply = QtWidgets.QMessageBox.question(self, 'Warning', \
                'Logging thread is are still open.' +\
                ' Do you really want to close the window?', \
                QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
            if buttonReply == QtWidgets.QMessageBox.Yes:
                if self.verdi_Logger.log_running():
                    self.verdi_Logger.end_log()
            else:
                event.ignore()
                return
            
        if (self.verdi.isConnected() or self.chiller.isConnected() \
            or self.oscilloscope.isConnected()):
            buttonReply = QtWidgets.QMessageBox.question(self, 'Warning', \
                'Some of the connections are still open.' +\
                ' Do you really want to close the window?', \
                QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
            if buttonReply == QtWidgets.QMessageBox.Yes:
                if self.verdi.isConnected():
                    self.verdi.disconnect()
                if self.chiller.isConnected():
                    self.chiller.disconnect()
                if self.oscilloscope.isConnected():
                    self.oscilloscope.disconnect()
            else:
                event.ignore()
                return
        QtWidgets.QMainWindow.closeEvent(self, event)


#%%        
if __name__ == '__main__':
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication([])
    
    MainWindow = MiraControlMainWindow()
    #dc = MyDynamicMplCanvas(ui.widget, width=5, height=4, dpi=100)
    MainWindow.show()
    app.exec_()
    sys.exit(app.exec_())
        

