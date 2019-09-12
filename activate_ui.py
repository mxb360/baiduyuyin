# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'activate.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(904, 254)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(510, 210, 101, 31))
        self.pushButton.setObjectName("pushButton")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(60, 140, 831, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("color: rgb(0, 0, 255);")
        self.label_6.setObjectName("label_6")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(370, 10, 161, 51))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(50, 60, 131, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.lineEdit_input = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_input.setGeometry(QtCore.QRect(50, 100, 801, 41))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.lineEdit_input.setFont(font)
        self.lineEdit_input.setText("")
        self.lineEdit_input.setObjectName("lineEdit_input")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(750, 210, 101, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(60, 170, 831, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("color: rgb(0, 0, 255);")
        self.label_7.setObjectName("label_7")
        self.pushButton_reg = QtWidgets.QPushButton(Dialog)
        self.pushButton_reg.setGeometry(QtCore.QRect(630, 210, 101, 31))
        self.pushButton_reg.setObjectName("pushButton_reg")

        self.retranslateUi(Dialog)
        self.pushButton_2.clicked.connect(Dialog.close)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "激活"))
        self.label_6.setText(_translate("Dialog", "激活码是通过注册后获得的，如果你注册成功，该激活码会自动发送到你注册时留下的邮箱中，如果你已"))
        self.label.setText(_translate("Dialog", "激活软件"))
        self.label_5.setText(_translate("Dialog", "请输入激活码："))
        self.pushButton_2.setText(_translate("Dialog", "取消"))
        self.label_7.setText(_translate("Dialog", "经注册，请查看你的邮箱，如果未注册，请注册"))
        self.pushButton_reg.setText(_translate("Dialog", "注册"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

