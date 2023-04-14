# -*- coding: utf-8 -*-
"""
Created on Fri Dec 29 22:06:15 2017

@author: 1109282
"""
import os
import fcntl
import subprocess

# Code adapted from https://gist.github.com/PaulFurtado/fce98aef890469f34d51
def getAgilent():
    """
    Gets the devfs path to a "Agilent Technologies" by scraping the 
    output of the lsusb command
    
    The lsusb command outputs a list of USB devices attached to a 
    computer in the format:
        Bus 001 Device 004: ID 0957:17a4 Agilent Technologies, Inc.
    The devfs path to these devices is:
        /dev/bus/usb/<busnum>/<devnum>
    So for the above device, it would be:
        /dev/bus/usb/001/004
    This function generates that path.
    """
    proc = subprocess.Popen(['lsusb'], stdout=subprocess.PIPE)
    out = (proc.communicate()[0]).decode('utf-8')
    lines = out.split('\n')
    for line in lines:
        if 'Agilent' in line:
            parts = line.split()
            bus = parts[1]
            dev = parts[3][:3]
            return '/dev/bus/usb/%s/%s' % (bus, dev)


def resetUSB():
    """
    Sends the USBDEVFS_RESET IOCTL to a USB device.
    Hint from https://askubuntu.com/questions/645/how-do-you-reset-a-usb-device-from-the-command-line
    This function is useful for the following error:
        Exception: failed to set configuration
        [Errno 16] Resource busy
    """
    fd = os.open(getAgilent(), os.O_WRONLY)
    if (fd < 0):
        print("Error opening usb device in resetUSB")
        return

    # Equivalent of the _IO('U', 20) constant in the linux kernel.
    USBDEVFS_RESET = ord('U') << (4*2) | 20
    try:
        rc = fcntl.ioctl(fd, USBDEVFS_RESET, 0)
        if rc < 0:
            print('Error in ioctl in resetUSB')
    finally:
        os.close(fd)

if __name__ == "__main__":    
    resetUSB()
