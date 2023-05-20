# -*- coding: utf-8 -*-
"""
Created on Fri May 19 15:15:54 2023

@author: alexi
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
log_filename_prefix = os.path.abspath(dirname + '/logs/TDS220_temp_')

import time, datetime
from threading import Thread, Event
import math

class TDS220_Logger:
    def __init__(self, parent = None):
        self.parent = parent
        self.event = Event()
        self.event.clear()
        self.logger_thread = Thread(target=self.loging_func)
        self.logger_thread.start()
        
        
    def start_log(self):
        if self.logger_thread.is_alive():
            print('Already logging started')
        else:
            self.event.set()
        print('Start Log')
        
    def loging_func(self):
        oscilloscope = self.parent.oscilloscope
        index_ = 0
        while True:
            self.event.wait()
            index_ = 0
            if oscilloscope.isConnected():
                log_header = 'CH1 Freq, CH1 Pk2Pk, CH2 Freq, CH2 Pk2Pk'
                
                #print(log_header)
                
                logfile = dataLogger.dataLogger(filePrefix = log_filename_prefix, \
                                            max_write_count_to_flush = 60,\
                                            max_interval_to_flush = datetime.timedelta(seconds=20), \
                                            newLogfileInterval=datetime.timedelta(hours=12), \
                                            header = log_header, print_header_at_new_file = True)
                
                while True:
                    try:
                        if index_ == 0 :
                            time.sleep(self.parent.ui.updateIntervalSpinBox.value() - \
                                       math.floor(self.parent.ui.updateIntervalSpinBox.value()))
                            print('Collecting new data at', datetime.datetime.now().isoformat())
                            self.parent.updatePlot()
                            log_line = ''
                            log_line = self.parent.oscilloscope.chan1Freq +\
                                        self.parent.oscilloscope.chan1VPP +\
                                        self.parent.oscilloscope.chan2Freq +\
                                        self.parent.oscilloscope.chan2VPP
                            logfile.write(log_line)
                    
                            #print(log_line)
                        
                    except KeyboardInterrupt:
                        break
                    if not self.event.is_set():
                        print('Stop the log...')
                        logfile.close()
                        print('File saved...')
                        break
                    
                    time.sleep(1)
                    
                    index_ = ( index_ + 1 ) % math.floor(self.parent.ui.updateIntervalSpinBox.value() + 1)
                
                logfile.close()
            else:
                raise Exception('oscilloscope is not connected')
    
    def end_log(self):
        if self.logger_thread.is_alive():
            self.event.clear()
        else:
            raise Exception('Closing not opened thread')
            
    def log_running(self):
        return self.event.isSet()