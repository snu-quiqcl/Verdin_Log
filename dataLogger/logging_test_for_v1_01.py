import dataLogger_v1_1 as dataLogger
import datetime
import time

logfile = dataLogger.dataLogger(filePrefix = '/media/IonTrap/Data/BakingTemp/BakingOvenLog', \
                                newLogfileInterval=datetime.timedelta(minutes=1))
while (1):
    try:
        logfile.write('test')
        time.sleep(1)
    except: # This will catch Ctrl-C
        break

logfile.close()
    
