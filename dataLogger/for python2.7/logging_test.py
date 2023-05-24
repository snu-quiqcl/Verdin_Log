import dataLogger_v1_0 as dataLogger
import datetime
import time

logfile = dataLogger.dataLogger(newLogfileInterval=datetime.timedelta(minutes=1))
while (1):
    logfile.write('test')
    time.sleep(1)
    
##        ofile.write('%s, %s\n' % (value[1:10], datetime.datetime.now().isoformat()))
##        count=count+1;
##        if count > flushInterval:
##            ofile.flush()
##            count=0
##
##        time.sleep(interval)
##
##    except:
##        break


##
##        
##        
##interval=1;
##now=datetime.datetime.now();
##filename = "T:\Data\wavelength\log-%4d%02d%02d-%02d%02d%02d-%s.csv"%(now.year, now.month, now.day, now.hour, now.minute, now.second);
##ofile=open(filename,'a+')
##ofile.write('Format: datetime, ch0 on(1) or off(0), ch0 freq., ch1 on(1) or off(0), ch1 freq.,'% (datetime.datetime.now().isoformat(), interval))
##flushInterval=30/interval;
##count=flushInterval;
##while (1):
##    try:
##        # data acquisition
##        ofile.write('%s, %s\n' % (value[1:10], datetime.datetime.now().isoformat()))
##        count=count+1;
##        if count > flushInterval:
##            ofile.flush()
##            count=0
##
##        time.sleep(interval)
##
##    except:
##        break
##ofile.close()
##sock.close()
