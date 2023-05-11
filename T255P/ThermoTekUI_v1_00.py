# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ThermoTek\ThermoTekUI_v1_00.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ChillerControlDialog(object):
    def setupUi(self, ChillerControlDialog):
        ChillerControlDialog.setObjectName("ChillerControlDialog")
        ChillerControlDialog.resize(242, 267)
        self.verticalLayout = QtWidgets.QVBoxLayout(ChillerControlDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(ChillerControlDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.statusLabel = QtWidgets.QLabel(ChillerControlDialog)
        self.statusLabel.setObjectName("statusLabel")
        self.gridLayout.addWidget(self.statusLabel, 0, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(ChillerControlDialog)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)
        self.alarmLabel = QtWidgets.QLabel(ChillerControlDialog)
        self.alarmLabel.setObjectName("alarmLabel")
        self.gridLayout.addWidget(self.alarmLabel, 1, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(ChillerControlDialog)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)
        self.chillerLabel = QtWidgets.QLabel(ChillerControlDialog)
        self.chillerLabel.setObjectName("chillerLabel")
        self.gridLayout.addWidget(self.chillerLabel, 2, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(ChillerControlDialog)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 3, 0, 1, 1)
        self.dryerStatus = QtWidgets.QLabel(ChillerControlDialog)
        self.dryerStatus.setObjectName("dryerStatus")
        self.gridLayout.addWidget(self.dryerStatus, 3, 1, 1, 1)
        self.label_11 = QtWidgets.QLabel(ChillerControlDialog)
        self.label_11.setObjectName("label_11")
        self.gridLayout.addWidget(self.label_11, 4, 0, 1, 1)
        self.curTempLabel = QtWidgets.QLabel(ChillerControlDialog)
        self.curTempLabel.setObjectName("curTempLabel")
        self.gridLayout.addWidget(self.curTempLabel, 4, 1, 1, 1)
        self.label_10 = QtWidgets.QLabel(ChillerControlDialog)
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 5, 0, 1, 1)
        self.setTempButton = QtWidgets.QPushButton(ChillerControlDialog)
        self.setTempButton.setObjectName("setTempButton")
        self.gridLayout.addWidget(self.setTempButton, 5, 2, 1, 1)
        self.chillerRunButton = QtWidgets.QPushButton(ChillerControlDialog)
        self.chillerRunButton.setObjectName("chillerRunButton")
        self.gridLayout.addWidget(self.chillerRunButton, 2, 2, 1, 1)
        self.setTempBox = QtWidgets.QDoubleSpinBox(ChillerControlDialog)
        self.setTempBox.setDecimals(1)
        self.setTempBox.setMinimum(18.0)
        self.setTempBox.setMaximum(25.0)
        self.setTempBox.setSingleStep(0.1)
        self.setTempBox.setObjectName("setTempBox")
        self.gridLayout.addWidget(self.setTempBox, 5, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.updateButton = QtWidgets.QPushButton(ChillerControlDialog)
        self.updateButton.setObjectName("updateButton")
        self.verticalLayout.addWidget(self.updateButton)
        self.buttonBox = QtWidgets.QDialogButtonBox(ChillerControlDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(ChillerControlDialog)
        self.buttonBox.accepted.connect(ChillerControlDialog.accept)
        self.buttonBox.rejected.connect(ChillerControlDialog.reject)
        self.chillerRunButton.clicked.connect(ChillerControlDialog.chillerRunButtonClicked)
        self.setTempButton.clicked.connect(ChillerControlDialog.setTempButtonClicked)
        self.updateButton.clicked.connect(ChillerControlDialog.updateButtonClicked)
        QtCore.QMetaObject.connectSlotsByName(ChillerControlDialog)

    def retranslateUi(self, ChillerControlDialog):
        _translate = QtCore.QCoreApplication.translate
        ChillerControlDialog.setWindowTitle(_translate("ChillerControlDialog", "ThermoTek Control"))
        self.label.setText(_translate("ChillerControlDialog", "Status:"))
        self.statusLabel.setText(_translate("ChillerControlDialog", "TextLabel"))
        self.label_4.setText(_translate("ChillerControlDialog", "Alarm:"))
        self.alarmLabel.setText(_translate("ChillerControlDialog", "TextLabel"))
        self.label_5.setText(_translate("ChillerControlDialog", "Chiller:"))
        self.chillerLabel.setText(_translate("ChillerControlDialog", "TextLabel"))
        self.label_8.setText(_translate("ChillerControlDialog", "Dryer:"))
        self.dryerStatus.setText(_translate("ChillerControlDialog", "Text"))
        self.label_11.setText(_translate("ChillerControlDialog", "Current\n"
"Temp:"))
        self.curTempLabel.setText(_translate("ChillerControlDialog", "Text"))
        self.label_10.setText(_translate("ChillerControlDialog", "Set\n"
"Temp:"))
        self.setTempButton.setText(_translate("ChillerControlDialog", "Set"))
        self.chillerRunButton.setText(_translate("ChillerControlDialog", "On"))
        self.updateButton.setText(_translate("ChillerControlDialog", "Update"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ChillerControlDialog = QtWidgets.QDialog()
    ui = Ui_ChillerControlDialog()
    ui.setupUi(ChillerControlDialog)
    ChillerControlDialog.show()
    sys.exit(app.exec_())

