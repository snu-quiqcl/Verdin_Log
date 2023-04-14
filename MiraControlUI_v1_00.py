# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MiraControlUI_v1_00.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(874, 586)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 874, 21))
        self.menubar.setObjectName("menubar")
        self.menuChiller = QtWidgets.QMenu(self.menubar)
        self.menuChiller.setObjectName("menuChiller")
        self.menuVerdi = QtWidgets.QMenu(self.menubar)
        self.menuVerdi.setObjectName("menuVerdi")
        self.menuOscilloscope = QtWidgets.QMenu(self.menubar)
        self.menuOscilloscope.setObjectName("menuOscilloscope")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionFront_Panel = QtWidgets.QAction(MainWindow)
        self.actionFront_Panel.setEnabled(False)
        self.actionFront_Panel.setObjectName("actionFront_Panel")
        self.actionLaser_Status = QtWidgets.QAction(MainWindow)
        self.actionLaser_Status.setEnabled(False)
        self.actionLaser_Status.setObjectName("actionLaser_Status")
        self.actionDiode_Parameters = QtWidgets.QAction(MainWindow)
        self.actionDiode_Parameters.setEnabled(False)
        self.actionDiode_Parameters.setObjectName("actionDiode_Parameters")
        self.actionFault_Status = QtWidgets.QAction(MainWindow)
        self.actionFault_Status.setEnabled(False)
        self.actionFault_Status.setObjectName("actionFault_Status")
        self.actionServo_Status = QtWidgets.QAction(MainWindow)
        self.actionServo_Status.setEnabled(False)
        self.actionServo_Status.setObjectName("actionServo_Status")
        self.actionConnection_to_Verdi = QtWidgets.QAction(MainWindow)
        self.actionConnection_to_Verdi.setObjectName("actionConnection_to_Verdi")
        self.actionConnection_to_Chiller = QtWidgets.QAction(MainWindow)
        self.actionConnection_to_Chiller.setObjectName("actionConnection_to_Chiller")
        self.actionChiller_Control = QtWidgets.QAction(MainWindow)
        self.actionChiller_Control.setEnabled(False)
        self.actionChiller_Control.setObjectName("actionChiller_Control")
        self.menuChiller.addAction(self.actionConnection_to_Chiller)
        self.menuChiller.addSeparator()
        self.menuChiller.addAction(self.actionChiller_Control)
        self.menuVerdi.addAction(self.actionConnection_to_Verdi)
        self.menuVerdi.addSeparator()
        self.menuVerdi.addAction(self.actionFront_Panel)
        self.menuVerdi.addSeparator()
        self.menuVerdi.addAction(self.actionLaser_Status)
        self.menuVerdi.addAction(self.actionServo_Status)
        self.menuVerdi.addAction(self.actionDiode_Parameters)
        self.menuVerdi.addAction(self.actionFault_Status)
        self.menubar.addAction(self.menuChiller.menuAction())
        self.menubar.addAction(self.menuVerdi.menuAction())
        self.menubar.addAction(self.menuOscilloscope.menuAction())

        self.retranslateUi(MainWindow)
        self.actionFront_Panel.triggered.connect(MainWindow.openVerdiFrontPanel)
        self.actionLaser_Status.triggered.connect(MainWindow.openVerdiLaserStatus)
        self.actionDiode_Parameters.triggered.connect(MainWindow.openVerdiDiodeParameters)
        self.actionFault_Status.triggered.connect(MainWindow.openVerdiFaultStatus)
        self.actionServo_Status.triggered.connect(MainWindow.openVerdiServoStatus)
        self.actionConnection_to_Verdi.triggered.connect(MainWindow.openVerdiConnection)
        self.actionConnection_to_Chiller.triggered.connect(MainWindow.openChillerConnection)
        self.actionChiller_Control.triggered.connect(MainWindow.openChillerControlPanel)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Mira Control"))
        self.menuChiller.setTitle(_translate("MainWindow", "Chiller"))
        self.menuVerdi.setTitle(_translate("MainWindow", "Verdi"))
        self.menuOscilloscope.setTitle(_translate("MainWindow", "Oscilloscope"))
        self.actionFront_Panel.setText(_translate("MainWindow", "Front Panel"))
        self.actionLaser_Status.setText(_translate("MainWindow", "Laser Status"))
        self.actionDiode_Parameters.setText(_translate("MainWindow", "Diode Parameters"))
        self.actionFault_Status.setText(_translate("MainWindow", "Fault Status"))
        self.actionServo_Status.setText(_translate("MainWindow", "Servo Status"))
        self.actionConnection_to_Verdi.setText(_translate("MainWindow", "Connection to Verdi"))
        self.actionConnection_to_Chiller.setText(_translate("MainWindow", "Connection to Chiller"))
        self.actionChiller_Control.setText(_translate("MainWindow", "Chiller Control"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

