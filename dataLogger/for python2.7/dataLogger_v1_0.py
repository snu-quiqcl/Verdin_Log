import datetime

class dataLogger():
    def __init__(self, filePrefix = 'log', newLogfileInterval = datetime.timedelta(days=1), flushInterval = 10):
        self.fileFormat = filePrefix + '-%4d%02d%02d-%02d%02d%02d.csv' ;
        self.newLogfileInterval = newLogfileInterval
        self.flushInterval = flushInterval
        self.newFile()

    def write(self, data):
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
        
