#!/usr/bin/python3
# -*- coding: utf-8 -*-

# This script is stored in O:\Device Manuals and Data\Coherent Mira HP-D and Verdi-V18\Monitoring Scripts\

# Change log
# v1_0: Initial version

import socket
import time
import sys
import getopt
import datetime
from functools import reduce

DEBUG = True

def main(argv):
    global chiller
    verbose = True
    try:
        opts, args = getopt.getopt(argv[1:],"hs:t:q",['help', 'Start', 'Stop'])
    except getopt.GetoptError:
        printUsage(argv[0])
        sys.exit(2)
        
    chiller = T255P()
 
class T255P:
    statusMessage = {'0': 'Auto Start', '1': 'Stand By', \
        '2': 'Chiller Run', '3': 'Safety Default'}

    def __init__(self, defaultIPAddress = '10.1.1.141', defaultTCPPort = 18255):
        self.IPAddress = defaultIPAddress
        self.TCPPort = defaultTCPPort
        self.socket = None

    def isConnected(self):
        if self.socket != None:
            if self.socket.fileno() != -1:
                return True
        
        return False

    def connectToThermoTek(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.IPAddress, self.TCPPort))
        self.socket.settimeout(5)


    def disconnect(self):
        self.socket.close()
            
    def __del__(self):
        self.disconnect()



# Monitoring status of the chiller        

    def getCurrentTemperature(self):
        """ Returns the current temperature of the chiller. When it is 
        operating, the temperature will be close to the Set Temperature, but
        if it is in Stand By mode, the temperature will be close to the room
        temperature.
        
        Args:
            None
        
        Returns:
            float: current temperature in degree Celcius
        """
        return float(self.query('I'))/100

    def getSetTemperature(self):
        """ Returns the target temperature of the chiller.
        
        Args:
            None
        
        Returns:
            float: target temperature in degree Celcius
        """
        response = self.query('H0')
        setTemp, maxPower = response.split(',')
        if DEBUG:
            print('Set Temperature:', float(setTemp)/10)
        return float(setTemp)/10
        
    def getChillerStatus(self):
        """ Returns the status of the chiller.
            Note: If the status is requested right after the chiller is turn on,
            IndexError exception is thrown. Wait for at least 10 seconds
            before the status is requested.
        
        Args:
            None
        
        Returns:
            string(4 characters): each character represents  Chiller status,
            Alarm status, Chiller on/off, Dryer status
        """
        status = self.query('U')
        if DEBUG:
            print('Status: ', T255P.statusMessage[status[0]])
            if status[1] == '0':
                print('No Alarms')
            else:
                print('Alarm ON')
            if status[2] == '0':
                print('Chiller OFF')
            else:
                print('Chiller ON')
            if status[3] == '0':
                print('Dryer OFF')
            else:
                print('Dryer ON')
        return status
            
    def getAlarmState(self):
        status = self.query('J')
        if DEBUG:
            print("* Alarm State Flags *")
            if status[0] == '1': # fs flag
                print(" - Float Switch On")
            if status[1] == '1': # ha flag
                print(" - Hi Alarm On")
            if status[2] == '1': # la flag
                print(" - Low Alarm On")
            if status[3] == '1': # sa flag
                print(" - Sensor Alarm On")
            if status[4] == '1': # pa flag
                print(" - EEPROM Fail On")
            if status[5] == '1': # wa flag
                print(" - Watch dog On")
        return status
        

# Changing status of the chiller        
    def standBy(self):
        return self.modeSelect('0')
        
    def run(self):
        return self.modeSelect('1')

    def setTemperature(self, tempInDouble):
        """ Sets the target temperature of the chiller.
        
        Args:
            tempInDouble (double): target temperature in degree Celcius
        
        Returns:
            double: newly updated target temperature in degree Celcius
        """
        msg = 'M%+04d' % (tempInDouble * 10)
        responseText = self.command(msg)
        newTemperatureTimesTen = int(responseText)
        if int(tempInDouble * 10) != newTemperatureTimesTen:
            print("Newly set temperature is different from the requested temperature!")
            return
        return newTemperatureTimesTen/10.0


# Supporting methods for chiller monitoring

    def query(self, msg):
        """ Returns the various information about the chiller status.
        This method assumes that the response from the chiller will
        contain the full command at the beginning such as 'H0', 'I', 'J',
        'O', 'U'. Other types of command can be handled by "command"
        method.
        
        Args:
            msg (string): query string excluding the leading '.' and
                the following checksum and CR.
        
        Returns:
            string: response from the chiller (The leading '#', echo
                of the command, comm error status, the follwing checksum,
                and CR are removed.)
        """
        self.socket.send(bytes(self.makeMSG(msg), 'utf-8'))
        response = self.socket.recv(20).decode('utf-8')
        if DEBUG:
            print('Received message:', repr(response))
        responseText = self.extractReply(response)
        msgLength = len(msg)
        if msg != responseText[:msgLength]:
            print("Response does not contain original query!")
            return
        if responseText[msgLength] == '1':
            print("Checksum Error was reported by T255P")
            return
        elif responseText[msgLength] == '2':
            print("Bad Command Error was reported by T255P")
            return
        elif responseText[msgLength] == '3':
            print("Out of Bound Qualifier Error was reported by T255P")
            return
        return responseText[msgLength+1:]


# Supporting methods for chiller control

    def modeSelect(self, modeInChar):
        """ Either starts or stops the chiller. '0' puts the chiller
        into "Stand By" mode, and '1' puts the chiller into "Run" mode.
        
        Args:
            msg (single character): '0' => Stand By, '1' => Run Mode
        
        Returns: 
            int: 0 means the mode was changed successfully and 1 means
                that there was an error in mode change
        """
        msg = 'G'+modeInChar
        responseText = self.command(msg)
        if responseText != modeInChar:
            print("Requested mode is not set!")
            return 1
        return 0


    def command(self, msg):
        """ Returns the response of the chiller after it has excuted
        the given command. This method assumes that the response
        from the chiller will contain only the single command character
        such as 'G' and 'M'. Other types of query can be handled by
        "query" method.
        
        Args:
            msg (string): query string excluding the leading '.' and
                the following checksum and CR.
        
        Returns:
            string: response from the chiller (The leading '#', echo
                of the command, comm error status, the follwing checksum,
                and CR are removed.)
        """
        self.socket.send(bytes(self.makeMSG(msg), 'utf-8'))
        response = self.socket.recv(20).decode('utf-8')
        if DEBUG:
            print('Received message:', repr(response))
        responseText = self.extractReply(response)
        if responseText[0] != msg[0]:
            print("Response does not contain %s!" % msg[0])
            return
        if responseText[1] == '1':
            print("Checksum Error was reported by T255P")
            return
        elif responseText[1] == '2':
            print("Bad Command Error was reported by T255P")
            return
        elif responseText[1] == '3':
            print("Out of Bound Qualifier Error was reported by T255P")
            return
        return responseText[2:]

# Raw protocol implementation

    def checksum(self, st):
        return reduce(lambda x,y:x+y, map(ord, st)) % 256

    def makeMSG(self, msg):
        fullMSG = '.%s%02X\r' % (msg, self.checksum('.'+msg))
        if DEBUG:
            print('Write message   :', repr(fullMSG))
        return fullMSG

    def showInHex(self, msg):
        res=map(ord, self.makeMSG(msg))
        output = msg + ' => '
        for each in res:
            output += '%02X ' % each
        print(output)

    def extractReply(self, rawMSG):
        if rawMSG[0] != '#':
            return 1
        if rawMSG[-1:] != '\r':
            return 2
        cs = rawMSG[-3:-1]
        coreMSG=rawMSG[:-3]
        if ('%02X' % self.checksum(coreMSG)) != cs:
            return 3
        return coreMSG[1:]
    

        
if __name__ == "__main__":
    main(sys.argv)        
