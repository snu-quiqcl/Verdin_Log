# -*- coding: utf-8 -*-
"""
Created on Fri May 12 19:47:50 2023

@author: alexi
"""
import time
import sys
import os
import numpy as np
import matplotlib
# Make sure that we are using QT5
matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.lines import Line2D

sys.path.insert(0, '..')
#from Ui_TEST_Widget_v1_00 import Ui_TEST_Widget

class FIG_MAKE(QtWidgets.QWidget):
    def __init__(self, parent):
        #QtWidgets.QWidget.__init__(self)        
        #self.ui = Ui_TEST_Widget()
        #self.ui.setupUi(self)
        self.parent = parent
        self.xpoints = 1000
        
    def attach_plot(self):
        self.fig = Figure(figsize=(4,3), dpi=100)
        self.axes = self.fig.add_subplot(111)
    
        self.axes.set_xlim(0, self.xpoints)
        self.axes.set_ylim(0, 256)
    
        self.axes.set_xticks(np.arange(0, self.xpoints+1, self.xpoints/10))
        self.axes.set_yticks(np.arange(0, 257, 32))
    
        self.axes.set_xticklabels([])
        self.axes.set_yticklabels([])
    
        self.axes.grid(which='both')
    
        # Adding curve to the plot
        self.line1 = Line2D(range(0, self.xpoints), [128]*self.xpoints, color='y')
        # http://matplotlib.org/api/artist_api.html#matplotlib.lines.Line2D
        self.axes.add_line(self.line1)
        self.line2 = Line2D(range(0, self.xpoints), [128]*self.xpoints, color='g')
        self.axes.add_line(self.line2)
    
        self.lineList = (self.line1, self.line2)
        #self.scaleList = (self.ui.ch1Y, self.ui.ch2Y)
        #self.buttonList = (self.ui.pushButton_Ch1, self.ui.pushButton_Ch2)
    
        self.canvas1 = FigureCanvas(self.fig)
        #self.canvas1.setParent(self.ui.widget)
        #self.canvas1.draw()
        self.canvas1.show()
        
if __name__ == "__main__":
    a = FIG_MAKE(None)
    a.attach_plot()