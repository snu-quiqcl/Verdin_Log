#-------------------------------------------------------------------------------
#  Get a screen catpure from DPO4000 series scope and save it to a file

# python        2.7         (http://www.python.org/)
# pyvisa        1.4         (http://pyvisa.sourceforge.net/)
# numpy         1.6.2       (http://numpy.scipy.org/)
# MatPlotLib    1.0.1       (http://matplotlib.sourceforge.net/)
#-------------------------------------------------------------------------------

import pyvisa
import numpy as np
from struct import unpack
import pylab

def read_all(devicehandle):
    VI_SUCCESS_DEV_NPRESENT = None
    VI_SUCCESS_MAX_CNT = None
    with devicehandle.ignore_warning(VI_SUCCESS_DEV_NPRESENT, VI_SUCCESS_MAX_CNT):

        try:
            data , status = devicehandle.visalib.read(devicehandle.session, devicehandle.bytes_in_buffer)
        except:
            pass
    return data


if __name__ == "__main__":
    rm = pyvisa.ResourceManager()
    scope = rm.open_resource('ASRL4')
    
    
    scope.write('DATA:SOU CH1')
    scope.write('DATA:WIDTH 1')
    scope.write('DATA:ENC RPB')
    
    scope.write('WFMPRE:YMULT?')
    ans = scope.read()
    ymult = float(ans)
    
    scope.write('WFMPRE:YZERO?')
    ans = scope.read()
    yzero = float(ans)
    
    scope.write('WFMPRE:YOFF?')
    ans = scope.read()
    yoff = float(ans)
    
    scope.write('WFMPRE:XINCR?')
    ans = scope.read() 
    xincr = float(ans)
    
    scope.write('ACQuire:MODe:SAMPLE')
    scope.write('CURVE?')
    data = scope.read_raw(16)
    #data = read_all(scope)
    headerlen = 2 + int(data[1])
    header = data[:headerlen]
    ADC_wave = data[headerlen:-1]
    
    ADC_wave = np.array(unpack('%sB' % len(ADC_wave),ADC_wave))
    
    Volts = (ADC_wave - yoff) * ymult  + yzero
    
    Time = np.arange(0, xincr * len(Volts), xincr)
    
    pylab.plot(Time, Volts)
    pylab.show()


