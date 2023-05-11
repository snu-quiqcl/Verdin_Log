# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'OscilloscopeWidgetUI_v1_02.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_OscilloscopeWidget(object):
    def setupUi(self, OscilloscopeWidget):
        OscilloscopeWidget.setObjectName("OscilloscopeWidget")
        OscilloscopeWidget.resize(947, 512)
        self.gridLayout_3 = QtWidgets.QGridLayout(OscilloscopeWidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(OscilloscopeWidget)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 2, 1, 1)
        self.autoUpdateButton = QtWidgets.QPushButton(OscilloscopeWidget)
        self.autoUpdateButton.setCheckable(True)
        self.autoUpdateButton.setObjectName("autoUpdateButton")
        self.gridLayout_2.addWidget(self.autoUpdateButton, 0, 3, 2, 1)
        self.updateIntervalSpinBox = QtWidgets.QDoubleSpinBox(OscilloscopeWidget)
        self.updateIntervalSpinBox.setMinimum(1.5)
        self.updateIntervalSpinBox.setMaximum(100.0)
        self.updateIntervalSpinBox.setSingleStep(0.5)
        self.updateIntervalSpinBox.setObjectName("updateIntervalSpinBox")
        self.gridLayout_2.addWidget(self.updateIntervalSpinBox, 1, 2, 1, 1)
        self.updateButton = QtWidgets.QPushButton(OscilloscopeWidget)
        self.updateButton.setObjectName("updateButton")
        self.gridLayout_2.addWidget(self.updateButton, 0, 1, 2, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 2, 1, 1, 1)
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
        self.verticalLayout.addLayout(self.buttonLayout)
        self.gridLayout_3.addLayout(self.verticalLayout, 0, 0, 3, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(OscilloscopeWidget)
        self.groupBox_2.setMinimumSize(QtCore.QSize(0, 300))
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.MeasurementLabel = QtWidgets.QLabel(self.groupBox_2)
        self.MeasurementLabel.setText("")
        self.MeasurementLabel.setObjectName("MeasurementLabel")
        self.gridLayout_4.addWidget(self.MeasurementLabel, 0, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")
        self.gridLayout_4.addWidget(self.label_5, 1, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox_2, 1, 1, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.triggerStatus = QtWidgets.QLabel(OscilloscopeWidget)
        self.triggerStatus.setText("")
        self.triggerStatus.setObjectName("triggerStatus")
        self.gridLayout.addWidget(self.triggerStatus, 0, 3, 1, 1)
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
        self.verticalLayout_3.addWidget(self.triggerSourceComboBox)
        self.gridLayout.addLayout(self.verticalLayout_3, 1, 3, 1, 1)
        self.runStopButton = QtWidgets.QPushButton(OscilloscopeWidget)
        self.runStopButton.setCheckable(True)
        self.runStopButton.setChecked(False)
        self.runStopButton.setObjectName("runStopButton")
        self.gridLayout.addWidget(self.runStopButton, 0, 0, 1, 1)
        self.runStopStatus = QtWidgets.QLabel(OscilloscopeWidget)
        self.runStopStatus.setObjectName("runStopStatus")
        self.gridLayout.addWidget(self.runStopStatus, 0, 1, 1, 1)
        self.singleButton = QtWidgets.QPushButton(OscilloscopeWidget)
        self.singleButton.setCheckable(True)
        self.singleButton.setObjectName("singleButton")
        self.gridLayout.addWidget(self.singleButton, 0, 2, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout.addLayout(self.verticalLayout_2, 1, 0, 1, 1)
        self.triggerForceButton = QtWidgets.QPushButton(OscilloscopeWidget)
        self.triggerForceButton.setObjectName("triggerForceButton")
        self.gridLayout.addWidget(self.triggerForceButton, 1, 2, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout, 0, 1, 1, 1)

        self.retranslateUi(OscilloscopeWidget)
        self.updateButton.clicked.connect(OscilloscopeWidget.updatePlot)
        self.runStopButton.clicked['bool'].connect(OscilloscopeWidget.runStop)
        self.triggerForceButton.clicked.connect(OscilloscopeWidget.triggerForced)
        self.triggerSourceComboBox.activated['QString'].connect(OscilloscopeWidget.triggerSourceChanged)
        self.singleButton.clicked.connect(OscilloscopeWidget.single)
        self.autoUpdateButton.clicked['bool'].connect(OscilloscopeWidget.autoUpdate)
        QtCore.QMetaObject.connectSlotsByName(OscilloscopeWidget)

    def retranslateUi(self, OscilloscopeWidget):
        _translate = QtCore.QCoreApplication.translate
        OscilloscopeWidget.setWindowTitle(_translate("OscilloscopeWidget", "Oscilloscope"))
        self.label.setText(_translate("OscilloscopeWidget", "Interval (s)"))
        self.autoUpdateButton.setText(_translate("OscilloscopeWidget", "Auto\n"
"update"))
        self.updateButton.setText(_translate("OscilloscopeWidget", "Update"))
        self.ch1Label.setText(_translate("OscilloscopeWidget", "1"))
        self.ch1Y.setText(_translate("OscilloscopeWidget", "ch1"))
        self.ch2Label.setText(_translate("OscilloscopeWidget", "2"))
        self.ch2Y.setText(_translate("OscilloscopeWidget", "ch2"))
        self.timebase.setText(_translate("OscilloscopeWidget", "timebase"))
        self.pushButton_Ch1.setText(_translate("OscilloscopeWidget", "Ch1"))
        self.pushButton_Ch2.setText(_translate("OscilloscopeWidget", "Ch2"))
        self.groupBox_2.setTitle(_translate("OscilloscopeWidget", "Measurements"))
        self.label_4.setText(_translate("OscilloscopeWidget", "Source"))
        self.triggerSourceComboBox.setItemText(0, _translate("OscilloscopeWidget", "CHAN1"))
        self.triggerSourceComboBox.setItemText(1, _translate("OscilloscopeWidget", "CHAN2"))
        self.triggerSourceComboBox.setItemText(2, _translate("OscilloscopeWidget", "EXT"))
        self.runStopButton.setText(_translate("OscilloscopeWidget", "RUN/\n"
"STOP"))
        self.runStopStatus.setText(_translate("OscilloscopeWidget", "STOP"))
        self.singleButton.setText(_translate("OscilloscopeWidget", "Single"))
        self.triggerForceButton.setText(_translate("OscilloscopeWidget", "Trigger\n"
"Force"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    OscilloscopeWidget = QtWidgets.QWidget()
    ui = Ui_OscilloscopeWidget()
    ui.setupUi(OscilloscopeWidget)
    OscilloscopeWidget.show()
    sys.exit(app.exec_())

