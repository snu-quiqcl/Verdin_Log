# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'connectionDialog\connectionUI_v1_01.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ConnectionDialog(object):
    def setupUi(self, ConnectionDialog):
        ConnectionDialog.setObjectName("ConnectionDialog")
        ConnectionDialog.resize(293, 188)
        self.gridLayout = QtWidgets.QGridLayout(ConnectionDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.connectButton = QtWidgets.QPushButton(ConnectionDialog)
        self.connectButton.setObjectName("connectButton")
        self.gridLayout.addWidget(self.connectButton, 4, 0, 1, 2)
        self.label_2 = QtWidgets.QLabel(ConnectionDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(ConnectionDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.TCPPortEdit = QtWidgets.QLineEdit(ConnectionDialog)
        self.TCPPortEdit.setText("")
        self.TCPPortEdit.setObjectName("TCPPortEdit")
        self.gridLayout.addWidget(self.TCPPortEdit, 1, 1, 1, 1)
        self.IPAddressEdit = QtWidgets.QLineEdit(ConnectionDialog)
        self.IPAddressEdit.setObjectName("IPAddressEdit")
        self.gridLayout.addWidget(self.IPAddressEdit, 0, 1, 1, 1)
        self.statusLabel = QtWidgets.QLabel(ConnectionDialog)
        self.statusLabel.setObjectName("statusLabel")
        self.gridLayout.addWidget(self.statusLabel, 2, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(ConnectionDialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.deviceInfo = QtWidgets.QTextEdit(ConnectionDialog)
        self.deviceInfo.setReadOnly(True)
        self.deviceInfo.setObjectName("deviceInfo")
        self.gridLayout.addWidget(self.deviceInfo, 3, 0, 1, 2)

        self.retranslateUi(ConnectionDialog)
        self.connectButton.clicked.connect(ConnectionDialog.connectButtonClicked)
        QtCore.QMetaObject.connectSlotsByName(ConnectionDialog)

    def retranslateUi(self, ConnectionDialog):
        _translate = QtCore.QCoreApplication.translate
        ConnectionDialog.setWindowTitle(_translate("ConnectionDialog", "Connection setting"))
        self.connectButton.setText(_translate("ConnectionDialog", "Connect"))
        self.label_2.setText(_translate("ConnectionDialog", "TCP port:"))
        self.label.setText(_translate("ConnectionDialog", "IP address:"))
        self.IPAddressEdit.setText(_translate("ConnectionDialog", "10.1.1.141"))
        self.statusLabel.setText(_translate("ConnectionDialog", "Status"))
        self.label_3.setText(_translate("ConnectionDialog", "Status:"))
        self.deviceInfo.setHtml(_translate("ConnectionDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Gulim\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ConnectionDialog = QtWidgets.QDialog()
    ui = Ui_ConnectionDialog()
    ui.setupUi(ConnectionDialog)
    ConnectionDialog.show()
    sys.exit(app.exec_())

