# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 19:55:23 2023

@author: alexi
"""

import pyvisa

rm = pyvisa.ResourceManager()
print(rm.list_resources())
"""
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

inst.close()
"""
