#!/usr/bin/python3
## -*- coding: utf-8 -*-

# This script is stored in O:\Device Manuals and Data\Coherent Mira HP-D and Verdi-V18\Monitoring Scripts\python3.5\RS232TCPServer

# Revision history
# 1.00: initial version for python3
# TO-DO list
# - Introduce authentication mechanmism. Under the current situation, some malicious person can send a damaging command to the controller
# - Convert to a service by making a daemon process

import time
import threading
import socketserver
import datetime
import sys
import getopt

import socket
import struct

import visa
#import serial
instDefaultTimeout = 2*1000 # unit in miliseconds?

#Changed to TDS220 device name
defaultVISADevice = 'ASRL/dev/ttyUSB3::INSTR'
#defaultSerialDevice = ''

defaultTCPPort = 3034

def printUsage(programName):
    print('Usage:')
    print('%s [options]\tStarts a TCP daemon to forward communication ' + \
          'to VISA device' % programName)
    print('\nOptions:')
    print('-s <device> \tspecifies the VISA device name. ' + \
          'The default device is %s.' % defaultVISADevice)
    print('-p <port> \tspecifies the TCP port. The default port is %d.' % \
          defaultTCPPort)
    print('-h, --help \tshows this message')
    


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        global inst, instLock, activeClientSocket
        clientSocket = self.request
        clientAddress = clientSocket.getpeername()
        print("%s: Connection request from %s" % \
              (datetime.datetime.now().isoformat(), clientAddress))
        if (threading.activeCount() > 2):
            activeClientAddress = activeClientSocket.getpeername()
            clientSocket.sendall(bytes('A:%s:%d' % activeClientAddress, 'latin-1'))
            clientSocket.close()
            print("%s: Refused connection from %s due to active connection with %s" % \
                  (datetime.datetime.now().isoformat(), 
                   clientAddress, activeClientAddress))
            return
        else:
            activeClientSocket = clientSocket
            clientSocket.sendall(bytes('C:', 'latin-1'))
            print('\nConnection from (%s,%d) became active connection\n' % clientAddress)

        try:
            data = clientSocket.recv(1024).decode('latin-1')
            #print('Received:', data)
            while len(data):
                instLock.acquire()
                if data[0:2] == 'w:':
                    success = False
                    failcount = 0
                    while not success:
                        try:
                            inst.write(data[2:])
                            success = True
                        except:
                            if failcount > 5:
                                inst.close()
                                server.shutdown()
                                raise Exception('Communication error between Oscilloscope and RPI')
                                return
                            failcount = failcount + 1
                            print('Failed ' + str(failcount))
                            instLock.release()
                            self.reboot_system()
                            instLock.acquire()
                            
                    instLock.release()
                    
                elif data[0:2] == 'q:':
                    success = False
                    failcount = 0
                    while not success:
                        try:
                            reply=inst.query(data[2:], None)
                            success = True
                        except:
                            if failcount > 5:
                                inst.close()
                                server.shutdown()
                                raise Exception('Communication error between Oscilloscope and RPI')
                                return
                            failcount = failcount + 1
                            print('Failed ' + str(failcount))
                            instLock.release()
                            self.reboot_system()
                            instLock.acquire()
                            
                    instLock.release()
                    print('Send:', reply)
                    clientSocket.sendall(bytes(reply, 'latin-1'))
                    
                elif data[0:3] == 'rr:':
                    success = False
                    failcount = 0
                    while not success:
                        try:
                            inst.write(data[3:])
                            reply = inst.read_raw(16)
                            success = True
                        except:
                            if failcount > 5:
                                inst.close()
                                server.shutdown()
                                raise Exception('Communication error between Oscilloscope and RPI')
                                return
                            failcount = failcount + 1
                            print('Failed ' + str(failcount))
                            instLock.release()
                            self.reboot_system()
                            instLock.acquire()
                            
                    print('Send:', reply)
                    #you should not encode reply, since it is raw data
                    clientSocket.sendall(reply)
                    instLock.release()
                
                data = clientSocket.recv(1024).decode('latin-1')
                #print('Received:', data)
                
            print("%s: Connection closed from %s" % \
                  (datetime.datetime.now().isoformat(), clientAddress))
        except IOError as e:
            print("%s: I/O error(%d): %s from %s" % (datetime.datetime.now().isoformat(), \
                                 e.errno, e.strerror, clientAddress))
            print("%s: Connection closed from %s" % \
                  (datetime.datetime.now().isoformat(), clientAddress))
            
        except:
            print("Unexpected error:", sys.exc_info()[0])
            print("%s: Connection closed from %s" % \
                  (datetime.datetime.now().isoformat(), clientAddress))
            print('\nActive connection is closed. Waiting for a new active connection...\n')
            raise
        print('\nActive connection is closed. Waiting for a new active connection...\n')
    
    def reboot_system(self):
        global inst, rm, VISADevice
        time.sleep(2)
        inst.close()
        rm.close()
        rm.visalib._registry.clear()
        rm = visa.ResourceManager('@py')
        print(rm.list_resources())
        inst = rm.open_resource(VISADevice)
        inst.encoding = 'latin-1'
        time.sleep(4)
        

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


import fcntl 
# This module is unique to Unix. To use this script on Windows machine, I 
# should remove get_ip_address() function and change the print statement in main()
# On raspberry pi, ip just shows up as 0.0.0.0 meaning all ethernet adapter.
# https://stackoverflow.com/questions/24196932/how-can-i-get-the-ip-address-of-eth0-in-python

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15].encode('utf-8'))
    )[20:24])



if __name__ == "__main__":
    global inst, instLock, activeClientSocket, rm, VISADevice
    argv = sys.argv
    try:
        opts, args = getopt.getopt(argv[1:],"s:p:h",['help'])
    except getopt.GetoptError:
        printUsage(argv[0])
        sys.exit(2)
    #print repr(opts)
#    serialDevice = defaultSerialDevice
    VISADevice = defaultVISADevice
    TCPPort = defaultTCPPort
    
    activeClientSocket = None

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            printUsage(argv[0])
            sys.exit()
        elif opt == '-s':
            VISADevice = arg
        elif opt == '-p':
            TCPPort = int(arg)


    rm = visa.ResourceManager('@py')
    print(rm.list_resources())
    
    # rm.list_resources() # Only possible as a root
    # To access the USB device as a normal user, the following file should be
    # added.
    # /etc/udev/rules.d/50-usb-oscilloscope.rules 
    
    # Agilent DSO-X 3034A
    # SUBSYSTEMS=="usb", ACTION=="add", ATTRS{idVendor}=="0957", ATTRS{idProduct}=="17a4", GROUP="plugdev", MODE="0660"
    #
    # RIGOL TECHNOLOGIES DS1074Z
    # ACTION=="add", SUBSYSTEMS=="usb", ATTRS{idVendor}=="1ab1", ATTRS{idProduct}=="04ce", MODE="660", GROUP="plugdev"

    # Open VISA device
    inst = rm.open_resource(VISADevice)
    inst.encoding = 'latin-1'
    # https://stackoverflow.com/questions/27451942/importing-visa-waveform-from-an-oscilloscope-into-python
 
    # Agilent DSO-X 3034A
    #inst = rm.open_resource('USB0::2391::6052::MY51361466::0::INSTR')
    # RIGOL TECHNOLOGIES DS1074Z
    #inst=rm.open_resource('USB0::6833::1230::DS1ZA173719337::0::INSTR')
    
#     Open serial port
#    ser=serial.Serial(serialDevice, baudrate=19200, bytesize=8, parity='N',\
#        stopbits=1, timeout=0.2)

    
    # Create a lock for multiple threads
    instLock = threading.Lock()
    
    # Port 0 means to select an arbitrary unused port
    #HOST, PORT = "localhost", 11232
    HOST = ''                 # Symbolic name meaning all available interfaces
    PORT = TCPPort

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address
    

    #print("Host IP:", ip, "Port:", port, "Serial device:", serialDevice)
    print("Host IP:", get_ip_address('eth0'), "Port:", port, "VISA device:", VISADevice)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass

    inst.close()
#    ser.close()



