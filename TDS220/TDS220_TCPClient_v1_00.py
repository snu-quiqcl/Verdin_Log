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


class TDS220(QtCore.QObject):

    def __init__(self, defaultIPAddress = '172.22.22.86', defaultTCPPort = 3034):
        super().__init__()  

        self.deviceOpened = False        
        self.IPAddress = defaultIPAddress
        self.TCPPort = defaultTCPPort

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
        self.socket.send(bytes('w:'+commandWithoutNewline, 'latin-1'))

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
        self.socket.send(bytes('q:' + messageWithoutNewline, 'latin-1'))
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
        totalQuery = ':MEASure:FREQuency? CHANnel1;' + \
            ':MEASure:VPP? CHANnel1;' + \
            ':MEASure:DELay? CHANnel2, CHANnel3;'

        totalQuery += ':TIMebase:SCALe?;'
        for n in range(2):
            ch = n+1
            totalQuery += ':CHANnel%d:DISPlay?;' % ch
            totalQuery += ':CHAN%d:SCAL?;' % ch


        for n in range(2):
            ch = n + 1
            totalQuery += ':WAVeform:SOURce CHANnel%d;:WAVeform:DATA?;' % ch
        reply = self.query(totalQuery)
        #print(len(reply))
        data = reply.split(';', 4+1+8)
        #print(data[:4+1+8])

        (self.chan1Freq, self.chan1VPP, self.chan3DelayWRTChan2,\
         self.chan4DelayWRTChan2, self.xscale) = list(map(float, data[:4+1]))
        
        self.channelOn = []
        self.yscale = []
        for n in range(2):
            self.channelOn.append(float(data[4 + 1 + 2*n]))
            self.yscale.append(float(data[4 + 1 + 2*n + 1]))
         

        self.ydata = []


        binaryBlocks = data[4+1+8]

        stringStream = io.StringIO(binaryBlocks)
        
        for n in range(2):
            self.ydata.append(self.read_binary_block(stringStream))
            nextChar = stringStream.read(1)
            if (len(nextChar) == 0):
                if (n != 1):
                    print('Not enough data from Waveform')
                    break
            elif nextChar != ';':
                print('Wrong Binary Transfer Format: blocks are separted by ' + nextChar)




    def read_binary_block(self, stream):
        """ Reads binary data block in Binary Transfer Format (IEEE 488.2 # format) from the device 
            http://na.support.keysight.com/pna/help/latest/Programming/Learning_about_GPIB/Getting_Data_from_the_Analyzer.htm#block

        Args:
            None
        
        Returns:
            byte string: received binary data only (header is removed)
        """

        # For large information such as PNG file, it takes a while before the
        # output becomes ready, so timeout is set to have enough waiting time.
        # In principle, this change of timeout should not affect the performance
        # at all because it requests exact number of bytes based on header 
        # information.
        header = stream.read(2)
        
        if header[0] != '#':
            raise Exception('Wrong Binary Transfer Format', \
                            'Starts with %c instead of #.' % header[0])

        header = stream.read(int(header[1]))
        dataLength = int(header)
        
        #print(dataLength)

        return list(map(ord, stream.read(dataLength)))


        
    def triggerAuto(self, mode = True):
        """ Select Auto or Normal trigger.
        
        Args:
            mode (bool): True==Auto, False==Normal
        
        Returns:
            None
        """
        if (mode):
            self.write(':TRIGger:SWEep AUTO')
        else:
            self.write(':TRIGger:SWEep NORMal')




import time
import socket

if __name__ == "__main__":    
    osc = TDS220(None)
    osc.openDevice()
    print(osc.readID())

    #osc.write(':MEASure:DEFine DELay,+0,+0') # Delay will be measured between two channels' first rising edges
    #osc.write(':MEASure:DEFine THResholds,PERCent,+90.0,+50.0,+10.0') # Setting delay measurement threshold

    #triggerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #triggerSocket.connect(('10.1.1.141', 23452))
    #triggerSocket.settimeout(1) # unit in second

    """
    :TRIGger:FORCe
    :TRIGger:EDGE:SOURce
    
    # The following precedure will clear the machine
    osc.write(':SINGle') # When TDS220 goes to Single, trigger mode is automatically reset to Normal
    time.sleep(0.5)
    osc.triggerAuto(False) # Once trigger mode is changed, then all the data seems to be erased
    osc.read()
    
    while True:
        try:
    osc.write(':SINGle')
    time.sleep(0.5)
    triggerSocket.send(b't')
    

    triggerEventRegister = osc.query(':TER?')
    print(triggerEventRegister)
    while triggerEventRegister == '+0':
        triggerEventRegister = osc.query(':TER?')
        print(triggerEventRegister)

            tstart = time.time()                
            totalQuery = ':MEASure:FREQuency? CHANnel1;' + \
                         ':MEASure:VPP? CHANnel1;' + \
                         ':MEASure:DELay? CHANnel2, CHANnel3;' + \
                         ':MEASure:DELay? CHANnel2, CHANnel4'
            #print(osc.query(totalQuery))
            osc.query(totalQuery)
            tstop = time.time()
            
            print(tstop - tstart)
                
            tstart = time.time(); osc.readAllActiveData(); print(time.time() - tstart)
            time.sleep(0.5)

        except KeyboardInterrupt: # This will catch only Ctrl-C, and by-pass all other exceptions
            print("Keyboard interrupted")
            break

    
    osc.closeDevice()
    triggerSocket.close()
    
    #osc.resetUSB() 
    
    
    """


"""
fig = plt.figure()
ax = fig.add_subplot(1,1,1)

ax.set_xticks(np.arange(0, 641, 64))
ax.set_yticks(np.arange(0, 257, 25.6))

ax.set_xticklabels([])
ax.set_yticklabels([])

ax.grid(which='both')

plotColor = ['y', 'g', 'b', 'r']
for n in range(4):
    if ydata[n] is not None:
        ax.plot(ydata[n], plotColor[n])
        
ax.set_ylim(0, 256)
ax.set_xlim(0, 640)

plt.show()

inst.close()
"""
