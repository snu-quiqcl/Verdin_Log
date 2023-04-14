#!/usr/bin/python3
# -*- coding: utf-8 -*-

# This script is stored in O:\Device Manuals and Data\Coherent Mira HP-D and Verdi-V18\Monitoring Scripts\...

# Change log
# v1_0: Initial version

import socket
import time
import sys
import getopt
import datetime

DEBUG = True

def main(argv):
    global v18
    verbose = True
    try:
        opts, args = getopt.getopt(argv[1:],"hs:t:q",['help', 'Start', 'Stop'])
    except getopt.GetoptError:
        printUsage(argv[0])
        sys.exit(2)
        
    v18 = Verdi()
    
class Verdi:
    servoStatusMsg = {'0': 'OPEN', '1': 'LOCKED', '2': 'SEEKING',\
        '3': 'FAULT', '4': 'OPTIMIZING'} # ?ESS, ?VSS don't have '4'
    faultStatusMsg = {\
        1: 'Head Emission Lamp Fault', 21: 'Diode 1 Over Volt Fault',\
        2: 'External Interlock Fault', 22: 'Diode 2 Over Volt Fault',\
        3: 'PS Cover Interlock Fault', 25: 'Diode 1 EEPROM Fault', \
        4: 'LBO Temperature Fault', 26: 'Diode 2 EEPROM Fault', \
        5: 'LBO Not Locked at Set Temp', 27: 'Laser Head EEPROM Fault', \
        6: 'Vanadate Temp. Fault', 28: 'Power Supply EEPROM Fault', \
        7: 'Etalon Temp. Fault', 29: 'PS-Head Mismatch Fault', \
        8: 'Diode 1 Temp. Fault', 31: 'Shutter State Mismatch', \
        9: 'Diode 2 Temp. Fault', 36: 'CPU PROM Range Fault', \
        10: 'Baseplate Temp. Fault', 37: 'Head PROM Range Fault', \
        11: 'Heatsink 1 Temp. Fault', 38: 'Diode 1 PROM Range Fault', \
        12: 'Heatsink 2 Temp. Fault', 39: 'Diode 2 PROM Range Fault', \
        16: 'Diode 1 Over Current Fault', 40: 'Head Diode Mismatch Fault', \
        17: 'Diode 2 Over Current Fault', 43: 'Lost Serial Link Fault', \
        18: 'Over Current Fault', 44: 'Vanadate 2 Temp. Fault', \
        19: 'Diode 1 Under Volt Fault', 47: '', \
        20: 'Diode 2 Under Volt Fault', 48: 'Head Communication Fault'}

    def __init__(self, defaultIPAddress = '10.1.1.141', defaultTCPPort = 18181):
        self.IPAddress = defaultIPAddress
        self.TCPPort = defaultTCPPort
        self.socket = None
        
    def isConnected(self):
        if self.socket != None:
            if self.socket.fileno() != -1:
                return True
        
        return False

    def connectToVerdi(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.IPAddress, self.TCPPort))
        self.socket.settimeout(5)
        """
        serial.Serial('/dev/serial/by-id/usb-FTDI_Dual_RS232-HS-if00-port0', \
            baudrate=19200, bytesize=8, parity='N', \
            stopbits=1, timeout=0.2)
        # If the timeout is less than 0.1second, there is communication error with some command
        """ 


    def disconnect(self):
        self.socket.close()
            
    def __del__(self):
        self.disconnect()

        
# Change the status of the Verdi
       
    def turnOffPrompt(self):
        self.command('>=0')

    def turnOffEcho(self):
        self.command('E=0')

    def closeShutter(self):
        self.command('S=0')

    def openShutter(self):
        self.command('S=1')
        
    def turnOffLaser(self):
        self.command('L=0')

    def turnOnLaser(self):
        self.command('L=1')
        
    def reduceSetPower(self, newPowerInWatt):
        newPowerInWatt = float(newPowerInWatt)
        currentPowerInWatt = float(self.query('SP')[1])
        if newPowerInWatt > currentPowerInWatt:
            print( ('Error: current set power: %07.4f W, requested set power:'\
                + ' %07.4f W. Only reducing power is allowed remotely.') % \
                (currentPowerInWatt, newPowerInWatt))
        else:
            self.command('P=%07.4f' % newPowerInWatt)
            
        return float(self.query('SP')[1])

    def _changePower(self, newPowerInWatt):
        newPowerInWatt = float(newPowerInWatt)
        if newPowerInWatt > 15:
            print( 'To increase the power more than 15 W, '\
                + 'change it locally.' )
        else:
            self.command('P=%07.4f' % newPowerInWatt)
            
        return float(self.query('SP')[1])

# Monitoring status of the Verdi
        
    def getKeyswitchStatus(self):
        response = self.query('K')[1]
        if response == '0':
            print('Keyswitch is OFF')
        else:
            print('Keyswitch is ON')

    def getLaserStatus(self):
        response = self.query('L')[1]
        if response == '0':
            if DEBUG:
                print('The laser is OFF (STANDBY)')
            return 'OFF'
        elif response == '1':
            if DEBUG:
                print('The laser is ON (ENABLE)')
            return 'ON'
        elif response == '2':
            if DEBUG:
                print('The laser is OFF due to fault (check fauts or falut history)')
            return 'OFF with fault'
        else:
            if DEBUG:
                print('The laser status is unknown')
            return 'Unknown'

    def getShutterStatus(self):
        response = self.query('S')[1]
        if DEBUG:
            if response == '0':
                print('Shutter: CLOSED')
            elif response == '1':
                print('Shutter: OPEN')
            else:
                print('The shutter status is unknown')
        return response

    def getFaultHistory(self):
        """ Returns a list of fault history. Each fault type can be found with
        faultStatusMsg dictionary. When there is no fault, empty list
        will be returned.
        
        Args:
            None
        
        Returns:
            list of integers: each integer represents the index of faultStatusMsg
                dictionary
        """
        response = self.query('FH')[1]
        if response == 'SYSTEM OK':
            if DEBUG:
                print(response)
            return []
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
            if DEBUG:
                print('Faults have occurred: ' + response)
                for eachFault in faultList:
                    print (self.faultStatusMsg[eachFault])
            return faultList
        

    def printSummary(self):
        laserLocked = False
        if self.query('K')[1] == '0':
            print('STANDBY by the keyswitch')
        elif self.query('L')[1] == '0':
            print('STANDBY by the RS232')
        elif self.query('S')[1] == '0':
            print('Shutter is closed')
        else:
            laserServoStatus = self.query('LRS')[1]
            if laserServoStatus == '2':
                print("LASER Seeking")
            elif laserServoStatus  == '1':
                laserLocked = True

        print('Set Power: %s (W), Actual Power: %s (W)' % (self.query('SP')[1]\
            , self.query('P')[1]))
        print('Diode current:', self.query('C')[1])
            
    def getServoInfo(self, statusQuery, getQuery, driveQuery,\
        setQuery):
        return (Verdi.servoStatusMsg[self.query(statusQuery)[1]],\
            self.query(getQuery)[1], self.query(driveQuery)[1], \
            self.query(setQuery)[1])

    def printServoStatus(self):
        print('** SERVO STATUS **')
        print ('   Laser: %-10s %6sW %8s %7sW' % \
            self.getServoInfo('LRS', 'P', 'C', 'SP'))

        print('     LBO: %-10s %6sC %8s %7sC' % \
            self.getServoInfo('LBOSS', 'LBOT', 'LBOD', 'LBOST'))

        print('VANADATE: %-10s %6sC %8s %7sC' % \
            self.getServoInfo('VSS', 'VT', 'VD', 'VST'))

        print('  ETALON: %-10s %6sC %8s %7sC' % \
            self.getServoInfo('ESS', 'ET', 'ED', 'EST'))

        print('  DIODE1: %-10s %6sC %8s %7sC' % \
            self.getServoInfo('D1SS', 'D1T', 'D1TD', 'D1ST'))

        print('  DIODE2: %-10s %6sC %8s %7sC' % \
            self.getServoInfo('D2SS', 'D2T', 'D2TD', 'D2ST'))

    def printDiodeParameters(self):
        print('** DIODE PARAMETERS **')
#        print 'Diode 1 Voltage  :  ??.??V'
        print('Diode 1 Current  :  %sA' % self.query('D1C')[1])
        print('Diode 1 Photocell:  %sV' % self.query('D1PC')[1])
#        print 'Diode 2 Voltage  :  ??.??V'
        print('Diode 2 Current  :  %sA' % self.query('D2C')[1])
        print('Diode 2 Photocell:  %sV' % self.query('D2PC')[1])

    def printLaserStatus(self):
        print('** LASER STATUS **')
        print('P/S Ver: %s' % self.query('SV')[1])
#        print ' Hd Ver: 1.03,02/21/10 812148261'
        print(' Baseplate Temp:   %sC' % self.query('BT')[1])
        print('Heatsink Temp 1:   %sC  2:   %sC' % (self.query('D1HST')[1],\
            self.query('D2HST')[1]))
        print(' Hd Hrs:  %s' % self.query('HH')[1])
        print(' D1 Hrs:  %s, I: %sA' % (self.query('D1H')[1],\
            self.query('D1C')[1]))
        print(' D2 Hrs:  %s, I: %sA' % (self.query('D2H')[1],\
            self.query('D2C')[1]))
        print('Power Suply Hrs: %s' % self.query('PSH')[1])


    def command(self, cmd):
        self.socket.send(bytes(cmd+'\r\n', 'utf-8'))
        response = self.socket.recv(100)[:-2].decode('utf-8')
        if DEBUG:
            print('Raw response:', response)
        if len(response) == 0:
            return 0
        if response == 'Error, invalid command':
            return 1
        if response == 'Error, data out of range':
            return 2
        if DEBUG:
            print('Unknown response:', response)
        self.lastErrorMessage = response
        return 3
        
        
    def query(self, queryString):
        self.socket.send(bytes('?%s\r\n' % queryString, 'utf-8'))
        response = self.socket.recv(100)[:-2].decode('utf-8')
        if DEBUG:
            print('Raw response:', response)
        if response == 'Error, invalid command':
            return (1, response)
        return (0, response)
        

if __name__ == "__main__":
    main(sys.argv)        
 
