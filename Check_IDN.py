# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 05:38:58 2023

@author: alexi
"""
import serial
com = serial.Serial('COM7', baudrate=19200, timeout=1, \
    parity='N', bytesize=8, stopbits=2, xonxoff=False, \
    rtscts=False, dsrdtr=False, writeTimeout = 0 )
string_to_send = '*IDN?\r\n'.encode('latin-1')
com.write(string_to_send)
a = com.readline()
print(a)
a = com.readline()
print(a)

string_to_send = '?F\r\n'.encode('latin-1')
#string_to_send = 'PRINT FAULTS\r\n'.encode('latin-1')
com.write(string_to_send)
a = com.readline()
print(a)
a = com.readline()
print(a)

string_to_send = 'PRINT FAULT HISTORY\r\n'.encode('latin-1')
com.write(string_to_send)
a = com.readline()
print(a)
a = com.readline()
print(a)

string_to_send = 'BAUDRATE = 19200\r\n'.encode('latin-1')
com.write(string_to_send)
a = com.readline()
print(a)
a = com.readline()
print(a)
com.close()