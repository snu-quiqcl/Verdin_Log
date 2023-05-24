#!/usr/bin/python3
## -*- coding: utf-8 -*-

# This script is stored in O:\Device Manuals and Data\Coherent Mira HP-D and Verdi-V18\Monitoring Scripts\python3.5\RS232TCPServer

# Revision history
# 1.00: initial version for python3
# TO-DO list
# - Introduce authentication mechanmism. Under the current situation, some malicious person can send a damaging command to the controller
# - Convert to a service by making a daemon process

import serial
import time
import threading
import socketserver
import datetime
import sys
import getopt

import socket
import struct


#defaultSerialDevice = '/dev/serial/by-id/' + \
#    'usb-FTDI_Dual_RS232-HS-if00-port0'
defaultSerialDevice = '/dev/serial/by-id/' + \
    'usb-Prolific_Technology_Inc._USB-Serial_Controller_CSAHb111216-if00-port0'
defaultTCPPort = 18181

def printUsage(programName):
    print('Usage:')
    print('%s [options]\tStarts a TCP daemon to forward communication ' + \
          'to serial port' % programName)
    print('\nOptions:')
    print('-s <device> \tspecifies the serial port device name. ' + \
          'The default device is %s.' % defaultSerialDevice)
    print('-p <port> \tspecifies the TCP port. The default port is %d.' % \
          defaultTCPPort)
    print('-h, --help \tshows this message')
    


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        global ser, serLock
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
            data = clientSocket.recv(1024)
            while len(data):
                serLock.acquire()
                ser.write(data)
                time.sleep(0.1)
                value = ser.read(100)
                serLock.release()
                clientSocket.sendall(value)
                data = clientSocket.recv(1024)
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
            raise

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
    global ser, serLock
    argv = sys.argv
    try:
        opts, args = getopt.getopt(argv[1:],"s:p:h",['help'])
    except getopt.GetoptError:
        printUsage(argv[0])
        sys.exit(2)
    #print repr(opts)
    serialDevice = defaultSerialDevice
    TCPPort = defaultTCPPort

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            printUsage(argv[0])
            sys.exit()
        elif opt == '-s':
            serialDevice = arg
        elif opt == '-p':
            TCPPort = int(arg)
 
    
    # Open serial port
    ser=serial.Serial(serialDevice, baudrate=19200, bytesize=8, parity='N',\
        stopbits=1, timeout=0.2) 

    # Create a lock for multiple threads
    serLock = threading.Lock()
    
    # Port 0 means to select an arbitrary unused port
    #HOST, PORT = "localhost", 11232
    HOST = ''                 # Symbolic name meaning all available interfaces
    PORT = TCPPort

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address
    

    #print("Host IP:", ip, "Port:", port, "Serial device:", serialDevice)
    print("Host IP:", get_ip_address('eth0'), "Port:", port, "Serial device:", serialDevice)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass

    ser.close()



