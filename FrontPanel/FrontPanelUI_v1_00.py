# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FrontPanelUI_v1_00.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FrontPanelDialog(object):
    def setupUi(self, FrontPanelDialog):
        FrontPanelDialog.setObjectName("FrontPanelDialog")
        FrontPanelDialog.resize(264, 308)
        self.verticalLayout = QtWidgets.QVBoxLayout(FrontPanelDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.keyStatusLabel = QtWidgets.QLabel(FrontPanelDialog)
        self.keyStatusLabel.setObjectName("keyStatusLabel")
        self.gridLayout.addWidget(self.keyStatusLabel, 2, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(FrontPanelDialog)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)
        self.laserEnableButton = QtWidgets.QPushButton(FrontPanelDialog)
        self.laserEnableButton.setObjectName("laserEnableButton")
        self.gridLayout.addWidget(self.laserEnableButton, 1, 2, 1, 1)
        self.laserEnableStatus = QtWidgets.QLabel(FrontPanelDialog)
        self.laserEnableStatus.setObjectName("laserEnableStatus")
        self.gridLayout.addWidget(self.laserEnableStatus, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(FrontPanelDialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.shutterButton = QtWidgets.QPushButton(FrontPanelDialog)
        self.shutterButton.setObjectName("shutterButton")
        self.gridLayout.addWidget(self.shutterButton, 0, 2, 1, 1)
        self.shutterStatusLabel = QtWidgets.QLabel(FrontPanelDialog)
        self.shutterStatusLabel.setObjectName("shutterStatusLabel")
        self.gridLayout.addWidget(self.shutterStatusLabel, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(FrontPanelDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(FrontPanelDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)
        self.powerSetButton = QtWidgets.QPushButton(FrontPanelDialog)
        self.powerSetButton.setObjectName("powerSetButton")
        self.gridLayout.addWidget(self.powerSetButton, 3, 2, 1, 1)
        self.powerSetValue = QtWidgets.QDoubleSpinBox(FrontPanelDialog)
        self.powerSetValue.setDecimals(4)
        self.powerSetValue.setMinimum(0.01)
        self.powerSetValue.setMaximum(15.0)
        self.powerSetValue.setSingleStep(0.1)
        self.powerSetValue.setObjectName("powerSetValue")
        self.gridLayout.addWidget(self.powerSetValue, 3, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.updateButton = QtWidgets.QPushButton(FrontPanelDialog)
        self.updateButton.setObjectName("updateButton")
        self.verticalLayout.addWidget(self.updateButton)
        self.textEdit = QtWidgets.QTextEdit(FrontPanelDialog)
        self.textEdit.setReadOnly(True)
        self.textEdit.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)

        self.retranslateUi(FrontPanelDialog)
        self.shutterButton.clicked.connect(FrontPanelDialog.shutterButtonPressed)
        self.laserEnableButton.clicked.connect(FrontPanelDialog.laserEnableButtonPressed)
        self.updateButton.clicked.connect(FrontPanelDialog.updateButtonPressed)
        self.powerSetButton.clicked.connect(FrontPanelDialog.powerSetButtonPressed)
        QtCore.QMetaObject.connectSlotsByName(FrontPanelDialog)

    def retranslateUi(self, FrontPanelDialog):
        _translate = QtCore.QCoreApplication.translate
        FrontPanelDialog.setWindowTitle(_translate("FrontPanelDialog", "Verdi Front Panel"))
        self.keyStatusLabel.setText(_translate("FrontPanelDialog", "On"))
        self.label_5.setText(_translate("FrontPanelDialog", "KEY STATUS"))
        self.laserEnableButton.setText(_translate("FrontPanelDialog", "Turn on"))
        self.laserEnableStatus.setText(_translate("FrontPanelDialog", "Off"))
        self.label_3.setText(_translate("FrontPanelDialog", "LASER ENABLE"))
        self.shutterButton.setText(_translate("FrontPanelDialog", "Open"))
        self.shutterStatusLabel.setText(_translate("FrontPanelDialog", "Closed"))
        self.label.setText(_translate("FrontPanelDialog", "SHUTTER"))
        self.label_2.setText(_translate("FrontPanelDialog", "Power"))
        self.powerSetButton.setText(_translate("FrontPanelDialog", "Set"))
        self.updateButton.setText(_translate("FrontPanelDialog", "Update status"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    FrontPanelDialog = QtWidgets.QDialog()
    ui = Ui_FrontPanelDialog()
    ui.setupUi(FrontPanelDialog)
    FrontPanelDialog.show()
    sys.exit(app.exec_())

