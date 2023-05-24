import dataLogger_v1_02 as dataLogger
import datetime
import time

import os, sys
filename = os.path.abspath(__file__)
dirname = os.path.dirname(filename)

logfile = dataLogger.dataLogger(filePrefix = dirname + '\\log_test', \
                                max_write_count_to_flush = 60,\
                                max_interval_to_flush = datetime.timedelta(seconds=20), \
                                newLogfileInterval=datetime.timedelta(minutes=10))
n = 0
while (1):
    try:
        n += 1
        logfile.write('test %d' % n)
        time.sleep(2)
    except: # This will catch Ctrl-C
        break

logfile.close()
    
