# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DSO_X_3034A\OscilloscopeWidgetUI_v1_00.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_OscilloscopeWidget(object):
    def setupUi(self, OscilloscopeWidget):
        OscilloscopeWidget.setObjectName("OscilloscopeWidget")
        OscilloscopeWidget.resize(665, 389)
        self.gridLayout_2 = QtWidgets.QGridLayout(OscilloscopeWidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(OscilloscopeWidget)
        self.frame.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMaximumSize(QtCore.QSize(16777215, 50))
        self.frame.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.ch1Label = QtWidgets.QLabel(self.frame)
        self.ch1Label.setEnabled(False)
        self.ch1Label.setStyleSheet("color: rgb(255, 255, 0);")
        self.ch1Label.setTextFormat(QtCore.Qt.AutoText)
        self.ch1Label.setObjectName("ch1Label")
        self.horizontalLayout_3.addWidget(self.ch1Label)
        self.ch1Y = QtWidgets.QLabel(self.frame)
        self.ch1Y.setStyleSheet("color: rgb(255, 255, 255);")
        self.ch1Y.setObjectName("ch1Y")
        self.horizontalLayout_3.addWidget(self.ch1Y)
        self.ch2Label = QtWidgets.QLabel(self.frame)
        self.ch2Label.setStyleSheet("color: rgb(36, 127, 13);")
        self.ch2Label.setTextFormat(QtCore.Qt.AutoText)
        self.ch2Label.setObjectName("ch2Label")
        self.horizontalLayout_3.addWidget(self.ch2Label)
        self.ch2Y = QtWidgets.QLabel(self.frame)
        self.ch2Y.setStyleSheet("color: rgb(255, 255, 255);")
        self.ch2Y.setObjectName("ch2Y")
        self.horizontalLayout_3.addWidget(self.ch2Y)
        self.ch3Label = QtWidgets.QLabel(self.frame)
        self.ch3Label.setStyleSheet("color: rgb(0, 85, 255);")
        self.ch3Label.setTextFormat(QtCore.Qt.AutoText)
        self.ch3Label.setObjectName("ch3Label")
        self.horizontalLayout_3.addWidget(self.ch3Label)
        self.ch3Y = QtWidgets.QLabel(self.frame)
        self.ch3Y.setStyleSheet("color: rgb(255, 255, 255);")
        self.ch3Y.setObjectName("ch3Y")
        self.horizontalLayout_3.addWidget(self.ch3Y)
        self.ch4Label = QtWidgets.QLabel(self.frame)
        self.ch4Label.setStyleSheet("color: rgb(255, 0, 127);")
        self.ch4Label.setTextFormat(QtCore.Qt.AutoText)
        self.ch4Label.setObjectName("ch4Label")
        self.horizontalLayout_3.addWidget(self.ch4Label)
        self.ch4Y = QtWidgets.QLabel(self.frame)
        self.ch4Y.setStyleSheet("color: rgb(255, 255, 255);")
        self.ch4Y.setObjectName("ch4Y")
        self.horizontalLayout_3.addWidget(self.ch4Y)
        self.timebase = QtWidgets.QLabel(self.frame)
        self.timebase.setEnabled(False)
        self.timebase.setStyleSheet("color: rgb(255, 255, 255);")
        self.timebase.setObjectName("timebase")
        self.horizontalLayout_3.addWidget(self.timebase)
        self.verticalLayout.addWidget(self.frame)
        self.widget = QtWidgets.QWidget(OscilloscopeWidget)
        self.widget.setMinimumSize(QtCore.QSize(400, 300))
        self.widget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.widget.setObjectName("widget")
        self.verticalLayout.addWidget(self.widget)
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.buttonLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.buttonLayout.setObjectName("buttonLayout")
        self.pushButton_Ch1 = QtWidgets.QPushButton(OscilloscopeWidget)
        self.pushButton_Ch1.setCheckable(True)
        self.pushButton_Ch1.setChecked(True)
        self.pushButton_Ch1.setObjectName("pushButton_Ch1")
        self.buttonLayout.addWidget(self.pushButton_Ch1)
        self.pushButton_Ch2 = QtWidgets.QPushButton(OscilloscopeWidget)
        self.pushButton_Ch2.setCheckable(True)
        self.pushButton_Ch2.setChecked(False)
        self.pushButton_Ch2.setObjectName("pushButton_Ch2")
        self.buttonLayout.addWidget(self.pushButton_Ch2)
        self.pushButton_Ch3 = QtWidgets.QPushButton(OscilloscopeWidget)
        self.pushButton_Ch3.setCheckable(True)
        self.pushButton_Ch3.setObjectName("pushButton_Ch3")
        self.buttonLayout.addWidget(self.pushButton_Ch3)
        self.pushButton_Ch4 = QtWidgets.QPushButton(OscilloscopeWidget)
        self.pushButton_Ch4.setCheckable(True)
        self.pushButton_Ch4.setObjectName("pushButton_Ch4")
        self.buttonLayout.addWidget(self.pushButton_Ch4)
        self.verticalLayout.addLayout(self.buttonLayout)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 3, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.runStopButton = QtWidgets.QPushButton(OscilloscopeWidget)
        self.runStopButton.setCheckable(True)
        self.runStopButton.setChecked(False)
        self.runStopButton.setObjectName("runStopButton")
        self.horizontalLayout.addWidget(self.runStopButton)
        self.runStopStatus = QtWidgets.QLabel(OscilloscopeWidget)
        self.runStopStatus.setObjectName("runStopStatus")
        self.horizontalLayout.addWidget(self.runStopStatus)
        self.singleButton = QtWidgets.QPushButton(OscilloscopeWidget)
        self.singleButton.setCheckable(True)
        self.singleButton.setObjectName("singleButton")
        self.horizontalLayout.addWidget(self.singleButton)
        self.triggerStatus = QtWidgets.QLabel(OscilloscopeWidget)
        self.triggerStatus.setText("")
        self.triggerStatus.setObjectName("triggerStatus")
        self.horizontalLayout.addWidget(self.triggerStatus)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_3 = QtWidgets.QLabel(OscilloscopeWidget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.sweepModeComboBox = QtWidgets.QComboBox(OscilloscopeWidget)
        self.sweepModeComboBox.setObjectName("sweepModeComboBox")
        self.sweepModeComboBox.addItem("")
        self.sweepModeComboBox.addItem("")
        self.verticalLayout_2.addWidget(self.sweepModeComboBox)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.triggerForceButton = QtWidgets.QPushButton(OscilloscopeWidget)
        self.triggerForceButton.setObjectName("triggerForceButton")
        self.horizontalLayout_2.addWidget(self.triggerForceButton)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_4 = QtWidgets.QLabel(OscilloscopeWidget)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_3.addWidget(self.label_4)
        self.triggerSourceComboBox = QtWidgets.QComboBox(OscilloscopeWidget)
        self.triggerSourceComboBox.setObjectName("triggerSourceComboBox")
        self.triggerSourceComboBox.addItem("")
        self.triggerSourceComboBox.addItem("")
        self.triggerSourceComboBox.addItem("")
        self.triggerSourceComboBox.addItem("")
        self.triggerSourceComboBox.addItem("")
        self.verticalLayout_3.addWidget(self.triggerSourceComboBox)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.gridLayout.addLayout(self.verticalLayout_4, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 1, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(OscilloscopeWidget)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2.addWidget(self.groupBox, 1, 1, 1, 1)
        self.updateButton = QtWidgets.QPushButton(OscilloscopeWidget)
        self.updateButton.setObjectName("updateButton")
        self.gridLayout_2.addWidget(self.updateButton, 2, 1, 1, 1)

        self.retranslateUi(OscilloscopeWidget)
        self.updateButton.clicked.connect(OscilloscopeWidget.updatePlot)
        self.runStopButton.clicked['bool'].connect(OscilloscopeWidget.runStop)
        self.sweepModeComboBox.activated['QString'].connect(OscilloscopeWidget.sweepModeChanged)
        self.triggerForceButton.clicked.connect(OscilloscopeWidget.triggerForced)
        self.triggerSourceComboBox.activated['QString'].connect(OscilloscopeWidget.triggerSourceChanged)
        self.singleButton.clicked.connect(OscilloscopeWidget.single)
        QtCore.QMetaObject.connectSlotsByName(OscilloscopeWidget)

    def retranslateUi(self, OscilloscopeWidget):
        _translate = QtCore.QCoreApplication.translate
        OscilloscopeWidget.setWindowTitle(_translate("OscilloscopeWidget", "Oscilloscope"))
        self.ch1Label.setText(_translate("OscilloscopeWidget", "1"))
        self.ch1Y.setText(_translate("OscilloscopeWidget", "ch1"))
        self.ch2Label.setText(_translate("OscilloscopeWidget", "2"))
        self.ch2Y.setText(_translate("OscilloscopeWidget", "ch2"))
        self.ch3Label.setText(_translate("OscilloscopeWidget", "3"))
        self.ch3Y.setText(_translate("OscilloscopeWidget", "ch3"))
        self.ch4Label.setText(_translate("OscilloscopeWidget", "4"))
        self.ch4Y.setText(_translate("OscilloscopeWidget", "ch4"))
        self.timebase.setText(_translate("OscilloscopeWidget", "timebase"))
        self.pushButton_Ch1.setText(_translate("OscilloscopeWidget", "Ch1"))
        self.pushButton_Ch2.setText(_translate("OscilloscopeWidget", "Ch2"))
        self.pushButton_Ch3.setText(_translate("OscilloscopeWidget", "Ch3"))
        self.pushButton_Ch4.setText(_translate("OscilloscopeWidget", "Ch4"))
        self.runStopButton.setText(_translate("OscilloscopeWidget", "RUN/\n"
"STOP"))
        self.runStopStatus.setText(_translate("OscilloscopeWidget", "STOP"))
        self.singleButton.setText(_translate("OscilloscopeWidget", "Single"))
        self.label_3.setText(_translate("OscilloscopeWidget", "Sweep mode"))
        self.sweepModeComboBox.setItemText(0, _translate("OscilloscopeWidget", "AUTO"))
        self.sweepModeComboBox.setItemText(1, _translate("OscilloscopeWidget", "NORM"))
        self.triggerForceButton.setText(_translate("OscilloscopeWidget", "Trigger\n"
"Force"))
        self.label_4.setText(_translate("OscilloscopeWidget", "Source"))
        self.triggerSourceComboBox.setItemText(0, _translate("OscilloscopeWidget", "CHAN1"))
        self.triggerSourceComboBox.setItemText(1, _translate("OscilloscopeWidget", "CHAN2"))
        self.triggerSourceComboBox.setItemText(2, _translate("OscilloscopeWidget", "CHAN3"))
        self.triggerSourceComboBox.setItemText(3, _translate("OscilloscopeWidget", "CHAN4"))
        self.triggerSourceComboBox.setItemText(4, _translate("OscilloscopeWidget", "EXT"))
        self.updateButton.setText(_translate("OscilloscopeWidget", "Update"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    OscilloscopeWidget = QtWidgets.QWidget()
    ui = Ui_OscilloscopeWidget()
    ui.setupUi(OscilloscopeWidget)
    OscilloscopeWidget.show()
    sys.exit(app.exec_())
