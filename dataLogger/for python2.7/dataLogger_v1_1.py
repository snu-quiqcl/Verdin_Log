##################################################################
# v1_1: Added skipData option
##################################################################

import datetime

class dataLogger():
    def __init__(self, filePrefix = 'log', newLogfileInterval = datetime.timedelta(days=1), flushInterval = 10, skipData = 0):
        self.fileFormat = filePrefix + '-%4d%02d%02d-%02d%02d%02d.csv' ;
        self.newLogfileInterval = newLogfileInterval
        self.flushInterval = flushInterval
        if skipData < 0:
            print 'skipData cannot be negative (%d). Setting to 0...' % skipData
            self.skipData = 0
        else:
            self.skipData = skipData
        self.remainingCount = self.skipData
        self.newFile()

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
        self.countForFlush = self.countForFlush + 1
        if self.countForFlush >= self.flushInterval:
            self.currentFile.flush()
            self.countForFlush = 0

    def newFile(self):
        now = datetime.datetime.now();
        self.currentFile = open(self.fileFormat % (now.year, now.month, now.day, now.hour, now.minute, now.second), 'a+');
        self.currentFileEnd = now + self.newLogfileInterval
        self.countForFlush = 0
        
    def close(self):
        self.currentFile.close()
        
