# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'InformationDialog\InformationDialogUI_v1_00.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_informationDialog(object):
    def setupUi(self, informationDialog):
        informationDialog.setObjectName("informationDialog")
        informationDialog.resize(593, 292)
        self.verticalLayout = QtWidgets.QVBoxLayout(informationDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textEdit = QtWidgets.QTextEdit(informationDialog)
        font = QtGui.QFont()
        font.setFamily("Monospac821 BT")
        font.setPointSize(10)
        self.textEdit.setFont(font)
        self.textEdit.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)
        self.buttonBox = QtWidgets.QDialogButtonBox(informationDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(informationDialog)
        self.buttonBox.accepted.connect(informationDialog.accept)
        self.buttonBox.rejected.connect(informationDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(informationDialog)

    def retranslateUi(self, informationDialog):
        _translate = QtCore.QCoreApplication.translate
        informationDialog.setWindowTitle(_translate("informationDialog", "Dialog"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    informationDialog = QtWidgets.QDialog()
    ui = Ui_informationDialog()
    ui.setupUi(informationDialog)
    informationDialog.show()
    sys.exit(app.exec_())

