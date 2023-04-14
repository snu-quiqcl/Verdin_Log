#!/usr/bin/python3
# -*- coding: utf-8 -*-

# This script is stored in O:\Device Manuals and Data\Coherent Mira HP-D and Verdi-V18\Monitoring Scripts

# Change log
# v1_00: Initial version

email_recipient = ['thkimatmit@gmail.com', 'junki.kim.q@gmail.com']

import os
import time
import sys
import traceback
import math

workingDirectory = os.path.dirname(os.path.abspath(__file__))
os.chdir(workingDirectory) # I need to change the working directory to 
    #recognize all the customized import files
sys.path.insert(0, '..')

from sendEmail_v1_01 import sendmail

import V18.Verdi_v1_01 as Verdi
import ThermoTek.ThermoTek_T255P_v1_00 as T255P
import BME280.Adafruit_BME280 as AF_BME280
from meteocalc import Temp as TemperatureClass
from meteocalc import dew_point as calcuateDewpoint

DEBUG = False
Verdi.DEBUG = False
T255P.DEBUG = False

flagsDirectory = workingDirectory + '/flags'

import subprocess
nodeName = (subprocess.Popen('/bin/uname -n', shell=True, stdout=\
    subprocess.PIPE).stdout.read()[:-1]).decode('utf-8')
warningSubject = 'Warning from Coherent pulse laser manager (%s.sktsdc.com)' \
    % nodeName
errorSubject = 'Error from Coherent pulse laser manager (%s.sktsdc.com)' \
    % nodeName
reminderSubject = ('Reminder from Coherent pulse laser manager '
    '(%s.sktsdc.com)') % nodeName
accessErrorMsgTemplate = '%s.sktsdc.com is trying to access %s, ' + \
    'but exception has occurred during access. Please check the problem.\n\n'

def main(argv):
    global v18, chiller

    deviceOpenErrorType = 'deviceOpenError'
    try:
        v18 = Verdi.Verdi()
        v18.connectToVerdi()
        
        chiller = T255P.T255P()
        chiller.connectToThermoTek()
        
        sensor = AF_BME280.BME280(mode = AF_BME280.BME280_OSAMPLE_8)
        # If there is a flag file created from the previous error, remove it.
        removeFileIfItExists(flagsDirectory + ('/%sFlag' % deviceOpenErrorType))
    except:
        sendEMailOnce(deviceOpenErrorType, warningSubject, ('%s.sktsdc.com '
            'is trying to open devices, but exception has occurred '
            'during access. Please check the problem.\n\n') % nodeName)
        return
        

    v18ErrorType = 'v18AccessError'
    try:
        v18Status = v18.getLaserStatus()
        v18Shutter = v18.getShutterStatus() #'0':closed, '1':open
        v18FaultList = list(v18.getCurrentFault())
        # If there is a flag file created from the previous error, remove it.
        removeFileIfItExists(flagsDirectory + ('/%sFlag' % v18ErrorType))
    except:
        sendEMailOnce(v18ErrorType, warningSubject, accessErrorMsgTemplate \
                      % (nodeName, 'Verdi-18'))
        return

    v18FaultType = 'v18Faults'
    if len(v18FaultList) > 0:
        msg = ('The following faults have been recorded by Verdi '
               '(%s.sktsdc.com):\n\n') % nodeName
        for eachFault in v18FaultList:
            msg += ' - %s\n' % Verdi.Verdi.faultStatusMsg[eachFault]
        msg += '\nPlease clear the faults history to receive the e-mail notification.\n'
        sendEMailOnce(v18FaultType, errorSubject, msg)
    else:
        removeFileIfItExists(flagsDirectory + ('/%sFlag' % v18FaultType))
        


    chillerErrorType = 'chillerAccessError'
    try:
        chiller_status_total = chiller.getChillerStatus()
        chillerStatus = chiller_status_total[0]
        # '0': 'Auto Start', '1': 'Stand By', '2': 'Chiller Run', '3': 'Safety Default'
        chiller_on = (chiller_status_total[2] == '1')

        chillerTargetTemperature = chiller.getSetTemperature()
        # If there is a flag file created from the previous error, remove it.
        removeFileIfItExists(flagsDirectory + ('/%sFlag' % chillerErrorType))
    except:
        sendEMailOnce(chillerErrorType, warningSubject, accessErrorMsgTemplate % \
            (nodeName, 'ThermoTek T255P'))
        return

    sensorErrorType = 'BME280AccessError'
    try:
        degrees = sensor.read_temperature()
        humidity = sensor.read_humidity()
        #pascals = sensor.read_pressure()
        #hectopascals = pascals / 100
        # If there is a flag file created from the previous error, remove it.
        removeFileIfItExists(flagsDirectory + ('/%sFlag' % sensorErrorType))
    except:
        sendEMailOnce(sensorErrorType, warningSubject, accessErrorMsgTemplate % \
            (nodeName, 'BME280 tempearature/humidity sensor'))
        return

    dewPoint = calcuateDewpoint(temperature=TemperatureClass(degrees, 'c'), \
                          humidity=humidity)

    if DEBUG:
        print('V18 status:', v18Status)
        if v18Shutter == '0':
            print('Shutter: CLOSED')
        elif v18Shutter == '1':
            print('Shutter: OPEN')
        else:
            print('The shutter status is unknown')
            
        statusMessage = {'0': 'Auto Start', '1': 'Stand By', \
        '2': 'Chiller Run', '3': 'Safety Default'}
        print('\nChiller status: ', statusMessage[chillerStatus])
        print('Chiller set temperature: %f C' % chillerTargetTemperature)

        print('\nTemperature: %f C' % degrees)
        print('Humidity: %f %%' % humidity)
        print('Dew point: %f C' % dewPoint.c)


    #########################################################################
    ### Cheking point: if chillerStatus is 'Auto Start', send an e-mail to 
    ### notify that the power of chiller was recycled automatically, 
    ### probably due to a brief power failure.
    #########################################################################
    chiller_auto_start_warning_type = 'auto_started'
    chiller_auto_start_flag_filename = flagsDirectory + ('/%sFlag' % \
        chiller_auto_start_warning_type)
    if chillerStatus == '0':
        warning_message = 'It seems that the power of the chiller (ThermoTek T255P) was ' + \
            'recycled automatically, probably due to a brief power failure.' + \
            'This is not an error message, but to provide you an information.'
        sendEMailOnce(chiller_auto_start_warning_type, warningSubject, warning_message )
    else:
        removeFileIfItExists(chiller_auto_start_flag_filename)


    #########################################################################
    ### Cheking point: if the chiller is on without any laser on, send
    ### a reminder e-mail.
    #########################################################################
    chillerRunningWarningType = 'chillerRunning'
    chillerRunningFlagFilename = flagsDirectory + ('/%sFlag' % \
        chillerRunningWarningType)
    if v18Status == 'OFF' and chiller_on:
        # Check if this condition was detected for the first time. No flag
        # file means that it was not detected before. The flag file contains
        # the time of the first detection in terms of seconds since the epoch.
        if not os.path.isfile(chillerRunningFlagFilename):
            with open(chillerRunningFlagFilename, 'w') as a:
                a.write('%f'%time.time())
        else:
            modifiedTime = os.stat(chillerRunningFlagFilename).st_mtime
            now = time.time()
            secondsSinceLastEmail = now - modifiedTime
            daysSinceLastEmail = math.floor(secondsSinceLastEmail/60/60/24)
#            daysSinceLastEmail = 2 # for debugging purpose. Remove later
            if DEBUG:
                print('Time since the last email was sent to remind that the '
                      'chiller is running w/o Verdi: %d seconds, %d days' %\
                      (secondsSinceLastEmail, daysSinceLastEmail))

            if daysSinceLastEmail >= 2:
                with open(chillerRunningFlagFilename, 'r') as a:
                    createdTime = float(a.read())
                secondsElapsed = time.time() - createdTime
                daysElapsed = math.floor(secondsElapsed/60/60/24)
                
                msg = ('The chiller is running without any laser on. This '
                    'is NOT an error, but the chiller was left on for %d '
                    'days without the laser running. Please consider cold '
                    'shutdown.\n') % daysElapsed
                if sendmail(email_recipient, reminderSubject, msg) == 0:
                    # Update the modified time of the flag file
                    with open(chillerRunningFlagFilename, 'a'):
                        os.utime(chillerRunningFlagFilename, None)
                else:
                    # local e-mail will be sent by the cron daemon
                    print("Failed in sending a reminder e-mail about %s" \
                          % chillerRunningWarningType)
    else:
        removeFileIfItExists(chillerRunningFlagFilename)
        

    #########################################################################
    ### Cheking point: when the laser is on, if the chiller is not running,
    ### turn off the laser and send a warning e-mail
    #########################################################################
    if v18Status == 'ON' and (not chiller_on):
        v18.turnOffLaser()
        msg = 'Verdi-18 is running without the chiller!!!\nThe mode of Verdi-18'\
              + ' will be changed to a stand-by.'
        sendEmail('v18RunningWithoutChller', msg)
        return

    #########################################################################
    ### Cheking point:
    ### * Case1:
    ### - Chiller: on, Chiller set temperature < (estimated dew point + 1.5)
    ### - Laser off or (laser on, but shutter closed)
    ### => Problem: water condensing on Ti:Sapphire crystal
    ### => Increase the chiller set temperature and send warning e-mail.
    ### ==> If the new set temperature should be higher than 21degC,
    ###     turn off the laser as well, and an additional warning e-mail.
    ### * Case2:
    ### - Chiller: on, Chiller set temperature < (estimated dew point + 1.5)
    ### - Laser: on and shutter open: send warning e-mail only.
    #########################################################################


    ### Needs to be fully implemented

    dewPointErrorType = 'dewPointError'
    minimumTargetTemp = dewPoint.c + 1.5
    # 2 degC margin corresponds to roughly +/-10% error in relative humidity around 70%
#    if chiller_on and chillerTargetTemperature < minimumTargetTemp:
    if chillerTargetTemperature < minimumTargetTemp: # To figure out the humidity situation
        msg = ('Estimated dew point is %.2f while the chiller target temperature'
               ' is %.2f. I prefer to increase the chiller target temperature'
               ' up to %.2f.')\
               % (dewPoint.c, chillerTargetTemperature, minimumTargetTemp)
        sendEMailOnce(dewPointErrorType, warningSubject, msg)
    else:
        removeFileIfItExists(flagsDirectory + ('/%sFlag' % dewPointErrorType))


def removeFileIfItExists(flagFilename):
    if os.path.isfile(flagFilename):
        os.remove(flagFilename)

def sendEmail(errorType, errorMsg):
    flagFilename = flagsDirectory + ('/%sFlag' % errorType)
    msg = errorMsg + traceback.format_exc() \
        +('\n\nOnce the problem is clear, PLEASE REMOVE ERROR ' \
        + 'FLAG FILE located at %s. IT WILL NOT BE REMOVED AUTOMATICALLY.') \
        % flagFilename
    if sendmail(email_recipient, warningSubject, msg) == 0:
        open(flagFilename, 'w').close()
    else:
        print("Failed in sending a warning e-mail about %s" % errorType)
        # local e-mail will be sent by the cron daemon
    

def sendEMailOnce(errorType, subject, errorMsg):
    flagFilename = flagsDirectory + ('/%sFlag' % errorType)
    if not os.path.isfile(flagFilename):
        msg = errorMsg + traceback.format_exc() \
            + (('\n\nOnce the problem is cleared, the flag file'\
            + ' located at %s will be automatically removed at the next'\
            + ' checking cycle, but please make sure that it is removed'\
            + ' properly because the warning e-mail won\'t be sent if'\
            + ' the flag file exists to avoid duplicate warning mails.')\
            % flagFilename)
        if sendmail(email_recipient, subject, msg) == 0:
            open(flagFilename, 'w').close()
        else:
            print("Failed in sending a warning e-mail about %s" % errorType)
            # local e-mail will be sent by the cron daemon


if __name__ == "__main__":
    main(sys.argv)        
 
