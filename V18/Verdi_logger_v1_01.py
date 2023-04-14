# -*- coding: utf-8 -*-
"""
Created on Wed May 23 11:08:39 2018

@author: 1109282

v1_01: Removed unit for the convenience of plotting
"""

from __future__ import unicode_literals
import os, sys
filename = os.path.abspath(__file__)
dirname = os.path.dirname(filename)

new_path_list = []
new_path_list.append(os.path.abspath(dirname + \
    '/../../../../../../Device Control Scripts/python libraries/dataLogger')) # To import dataLogger
# More paths can be added here...
for each_path in new_path_list:
    if not (each_path in sys.path):
        sys.path.append(each_path)

import dataLogger_v1_03 as dataLogger
log_filename_prefix = os.path.abspath(dirname + '/logs/vanadate_temp_')
import Verdi_v1_01 as Verdi
Verdi.DEBUG = False

import time, datetime

if __name__ == '__main__':
    v18 = Verdi.Verdi()
    v18.connectToVerdi()

    log_header = 'Data and time, Laser status, Laser current power (W), Laser current, Laser set power (W)'
    log_header += ', LBO status, LBO current temp (C), LBO current, LBO set temp (C)'
    log_header += ', VANADATE status, VANADATE current temp (C), VANADATE current, VANADATE set temp (C)'
    log_header += ', ETALON status, ETALON current temp (C), ETALON current, ETALON set temp (C)'
    log_header += ', DIODE1 status, DIODE1 current temp (C), DIODE1 temp current, DIODE1 set temp (C), DIODE1 current (A)'
    log_header += ', DIODE2 status, DIODE2 current temp (C), DIODE2 temp current, DIODE2 set temp (C), DIODE2 current (A)'
    log_header += ', Baseplate Temp (C), Heatsink Temp 1 (C), Heatsink Temp 2 (C)'
    
    #print(log_header)
    
    logfile = dataLogger.dataLogger(filePrefix = log_filename_prefix, \
                                max_write_count_to_flush = 60,\
                                max_interval_to_flush = datetime.timedelta(seconds=20), \
                                newLogfileInterval=datetime.timedelta(hours=12), \
                                header = log_header, print_header_at_new_file = True)
    
    while True:
        try:
            print('Collecting new data at', datetime.datetime.now().isoformat())
            log_line = ('%s, %s, %s, %s' % v18.getServoInfo('LRS', 'P', 'C', 'SP'))
            log_line += (', %s, %s, %s, %s' % v18.getServoInfo('LBOSS', 'LBOT', 'LBOD', 'LBOST'))
            log_line += (', %s, %s, %s, %s' % v18.getServoInfo('VSS', 'VT', 'VD', 'VST'))
            log_line += (', %s, %s, %s, %s' % v18.getServoInfo('ESS', 'ET', 'ED', 'EST'))
            log_line += (', %s, %s, %s, %s' % v18.getServoInfo('D1SS', 'D1T', 'D1TD', 'D1ST'))
            log_line += (', %s' % v18.query('D1C')[1])
            log_line += (', %s, %s, %s, %s' % v18.getServoInfo('D2SS', 'D2T', 'D2TD', 'D2ST'))
            log_line += (', %s' % v18.query('D2C')[1])
            log_line += (', %s, %s, %s' % (v18.query('BT')[1], v18.query('D1HST')[1], v18.query('D2HST')[1]))
            logfile.write(log_line)
    
            #print(log_line)
            
            time.sleep(60)
        except KeyboardInterrupt:
            break
    
    
    v18.disconnect()
    logfile.close()
    
    
                                

