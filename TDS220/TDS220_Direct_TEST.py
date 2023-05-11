# -*- coding: utf-8 -*-
"""
Created on Tue May  9 14:25:55 2023

@author: alexi
"""

import pyvisa

if __name__ == '__main__':
    rm = pyvisa.ResourceManager()
    
    inst = rm.open_resource('ASRL4')
    inst.encoding = 'latin-1'
    
    string_to_send = '*IDN?'
    inst.write(string_to_send)
    a = inst.read()
    print(a)
    
    string_to_send = 'ACQuire?'
    inst.write(string_to_send)
    a = inst.read()
    print(a)
    
    string_to_send = 'CH1:COUPling?'
    inst.write(string_to_send)
    a = inst.read()
    print(a)
    
    string_to_send = 'CURVE?'
    inst.write(string_to_send)
    data_raw = inst.read_raw()
    header_len = 2 + int(data_raw[1])
    header = data_raw[:header_len]
    print(a)
    
    
    """
    while True:
        string_to_send = input()
        if string_to_send == 'EXIT':
            break
        inst.write(string_to_send)
        a = inst.read()
        print(a)
    """
    
    
    inst.close()