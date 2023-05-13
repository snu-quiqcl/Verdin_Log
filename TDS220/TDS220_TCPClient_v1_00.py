#!/usr/bin/python3
## -*- coding: latin-1 -*-

# This script is stored in O:/media/IonTrap/Device Control Scripts/Agilent DSO-X 3034A/new

# Change log
# v1_00: Initial version
# v2_00: To execute TDS220 object in a separate thread, QT signal is
#   added, and the structure is modified to accomodate separate thread


from PyQt5 import QtCore

import os
import subprocess
import io
import time
import socket
import numpy as np
from struct import unpack


class TDS220(QtCore.QObject):

    def __init__(self, defaultIPAddress = '172.22.22.86', defaultTCPPort = 3034):
        super().__init__()  

        self.deviceOpened = False        
        self.IPAddress = defaultIPAddress
        self.TCPPort = defaultTCPPort
        self.ydata = []
        self.chan1VPP = 0
        self.chan2VPP = 0
        self.chan1Freq = 0
        self.chan2Freq = 0

    def setWidget(self, widget):
        self.widget = widget        


    def connect(self):
        """ Opens the device.
        
        Args:
            None
        
        Returns:
            None
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.IPAddress, self.TCPPort))
        self.socket.settimeout(5)
        connectionInfo = self.socket.recv(100).decode('latin-1').split(':')
        if connectionInfo[0] == 'C': # Connected
            self.deviceOpened = True
            return None
        elif connectionInfo[0] == 'A': # Other active connection information is returned
            hostname = socket.gethostbyaddr(connectionInfo[1])[0]
            message = ('TCPServer is occupied by an active connection with ' +\
                       '(%s(%s), %s). Please disconnect the active ' +\
                       'connection first.') \
                       % (hostname, connectionInfo[1], connectionInfo[2])
            self.deviceOpened = False
            return message
        
        
    def disconnect(self):
        if self.widget.isSingleRun:
            self.widget.singleClean('Aborted')
        self.socket.close()
        self.deviceOpened = False

    def isConnected(self):
        return self.deviceOpened

    def write(self, commandWithoutNewline):
        """ Send the command.
        
        Args:
            commandWithoutNewline (unicode string): '\n' is automatically added,
                so it should not be added to the argument
        
        Returns:
            None
        """
        self.socket.send(bytes(commandWithoutNewline, 'latin-1'))

        #self.inst.write(commandWithoutNewline)
        
        

    def read(self):
        """ Reads data from the device.
        
        Args:
            None
        
        Returns:
            unicode string: received string
        """
        return (self.socket.recv(10000).decode('latin-1'))[:-1]
        #return (self.inst.read())[:-1] # Stripping '\n'
    

    def read_raw(self, size=None):
        """ Reads data from the device .
            
        Args:
            size (int): intented length to read
        
        Returns:
            byte string: received string
        """

        return (self.socket.recv(10000).decode('latin-1'))[:-1]
        #return self.inst.read_raw(size)        

    def query(self, messageWithoutNewline, delay = None):
        """ Send the message and read the reply.
        
        Args:
            messageWithoutNewline (unicode string): '\n' is automatically added,
                so it should not be added to the argument
        
        Returns:
            unicode string: reply string
        """
        self.socket.send(bytes(messageWithoutNewline, 'latin-1'))
        return (self.socket.recv(10000).decode('latin-1'))[:-1] # Stripping '\n'

        #reply = self.inst.query(messageWithoutNewline, delay)
        #return reply[:-1] # Stripping '\n'




    def readID(self):
        """ Reads device information.
        
        Args:
            None
        
        Returns:
            string: device information
        """

        return self.query("*IDN?")

    def readAllActiveData(self):
        """ Reads data from active channels and stores the data in data 
        attributes. Available data attributes are as follows:
            
        self.xscale (float): time scale in seconds.
        
        self.xpoints[0~1] (list of integer): number of points in each channel
        
        self.yscale[0~1] (list of float): yscale of each channel. If the channel
        is off, it is 0.
        
        self.ydata[0~1] (list of integer array): ydata of each channel. If the
        chanel is off, it is None.
        
        Args:
            None
        
        Returns:
            None
        """
        if self.channelOn[0] == True:
            self.write('SELECT:CH1 ON')
            self.write('ACQUire:MODe SAMPLE')
            self.write('ACQUire:STOPAFTER SEQUENCE')
            self.write('ACQUire:STATE ON')
            self.write('MEASUrement:IMMed:TYPe FREQuency')
            self.write('MEASUrement:IMMed:SOUrce CH1')  
            self.write('MEASUrement:IMMed:VALUE?')
            self.chan1Freq = float(self.read())
            self.write('MEASUrement:IMMed:TYPe PK2pk') 
            self.write('MEASUrement:IMMed:SOUrce CH1')  
            self.write('MEASUrement:IMMed:VALUE?')
            self.chan1VPP = float(self.read())/2
        
        if self.channelOn[1] == True:
            self.write('SELECT:CH2 ON')
            self.write('ACQUire:MODe SAMPLE')
            self.write('ACQUire:STOPAFTER SEQUENCE')
            self.write('ACQUire:STATE ON')
            self.write('MEASUrement:IMMed:TYPe FREQuency')
            self.write('MEASUrement:IMMed:SOUrce CH2')  
            self.write('MEASUrement:IMMed:VALUE?')
            self.chan2Freq = float(self.read())
            self.write('MEASUrement:IMMed:TYPe PK2pk') 
            self.write('MEASUrement:IMMed:SOUrce CH2')  
            self.write('MEASUrement:IMMed:VALUE?')
            self.chan2VPP = float(self.read())/2
        else:
            self.channelOn[1] = False
        
        self.write('WFMPre:NR_PT?')
        self.xscale = self.read()   
            
        for n in range(2):
            ch = n+1
            if self.channelOn[n] == True:
                self.write('DATA:SOU CH%d' % ch)
                self.write('DATA:WIDTH 1')
                self.write('DATA:ENC RPB')
                
                self.write('WFMPRE:YMULT?')
                ans = self.read()
                ymult = float(ans)
                
                self.write('WFMPRE:YZERO?')
                ans = self.read()
                yzero = float(ans)
                
                self.write('WFMPRE:YOFF?')
                ans = self.read()
                yoff = float(ans)
                
                self.write('WFMPRE:XINCR?')
                ans = self.read()
                xincr = float(ans)
                
                
                self.write('ACQuire:MODe:SAMPLE')
                self.write('CURVE?')
                data = self.read_raw(16)
                headerlen = 2 + int(data[1])
                header = data[:headerlen]
                ADC_wave = data[headerlen:-1]
                
                ADC_wave = np.array(unpack('%sB' % len(ADC_wave),ADC_wave))
                ADC_wave = ADC_wave[0:len(ADC_wave)-2]
                
                Volts = (ADC_wave - yoff) * ymult  + yzero
                
                Time = np.arange(0, xincr * len(Volts), xincr)
                
                Volts = Volts.tolist()
                Time = Time.tolist()
                self.ydata.append(Volts)




if __name__ == "__main__":    
    osc = TDS220(None)
    osc.openDevice()
    print(osc.readID())
