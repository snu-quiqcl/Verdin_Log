##################################################################
# v1_0: 2017.12.24 - This version started from v1_2 of python2
##################################################################

import datetime

class dataLogger():
    def __init__(self, filePrefix = 'log', \
                 newLogfileInterval = datetime.timedelta(days=1), \
                 max_write_count_to_flush = 10,\
                 max_interval_to_flush = datetime.timedelta(minutes=5), \
                 skipData = 0, \
                 printExcelTimeConversionHintAtBeginning = True):
        self.fileFormat = filePrefix + '-%4d%02d%02d-%02d%02d%02d.csv' ;
        self.newLogfileInterval = newLogfileInterval
        self.max_write_count_to_flush = max_write_count_to_flush
        self.max_interval_to_flush = max_interval_to_flush
        if skipData < 0:
            print('skipData cannot be negative (%d). Setting to 0...' % skipData)
            self.skipData = 0
        else:
            self.skipData = skipData
        self.remainingCount = self.skipData
        self.newFile()
        if printExcelTimeConversionHintAtBeginning:
            self.rawWrite('"To convert ISO format to Excel time,'\
                          +'=DATEVALUE(MID(A2,1,10))+TIMEVALUE(MID(A2,12,8)) '\
                          +'and change the cell format of the entire column to TIME type."\n')

    def rawWrite(self, data):
        self.currentFile.write(data)

    def write(self, data):
        if self.remainingCount > 0:
            self.remainingCount = self.remainingCount - 1
            return
        else:
            self.remainingCount = self.skipData
        
        now = datetime.datetime.now();
        if (now - self.currentFileEnd) > datetime.timedelta():
            self.currentFile.close()
            self.newFile()
            
        self.currentFile.write('%s, %s\n' % (datetime.datetime.now().isoformat(), data) )
        self.count_wo_flush = self.count_wo_flush + 1
        if (self.count_wo_flush >= self.max_write_count_to_flush) or \
            ((datetime.datetime.now() - self.last_flush_time) > self.max_interval_to_flush):
            self.currentFile.flush()
            self.count_wo_flush = 0
            self.last_flush_time = datetime.datetime.now()
    
    
    
    def newFile(self):
        now = datetime.datetime.now();
        self.filename = self.fileFormat % (now.year, now.month, now.day, now.hour, now.minute, now.second)
        self.currentFile = open(self.filename, 'a+');
        self.currentFileEnd = now + self.newLogfileInterval
        self.count_wo_flush = 0
        self.last_flush_time = datetime.datetime.now()
        
    def close(self):
        self.currentFile.close()
        
