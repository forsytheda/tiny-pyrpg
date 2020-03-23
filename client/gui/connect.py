# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Jeffrey Smith\Desktop\connect.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_connect_window(object):
    def setupUi(self, connect_window):
        connect_window.setObjectName("connect_window")
        connect_window.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(connect_window)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(310, 170, 161, 61))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.ip_box = QtWidgets.QTextEdit(self.centralwidget)
        self.ip_box.setGeometry(QtCore.QRect(220, 240, 351, 71))
        font = QtGui.QFont()
        font.setPointSize(30)
        self.ip_box.setFont(font)
        self.ip_box.setObjectName("ip_box")
        self.connect_button = QtWidgets.QPushButton(self.centralwidget)
        self.connect_button.setGeometry(QtCore.QRect(340, 340, 121, 61))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.connect_button.setFont(font)
        self.connect_button.setObjectName("connect_button")
        connect_window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(connect_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        connect_window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(connect_window)
        self.statusbar.setObjectName("statusbar")
        connect_window.setStatusBar(self.statusbar)

        self.retranslateUi(connect_window)
        QtCore.QMetaObject.connectSlotsByName(connect_window)

    def retranslateUi(self, connect_window):
        _translate = QtCore.QCoreApplication.translate
        connect_window.setWindowTitle(_translate("connect_window", "MainWindow"))
        self.label.setText(_translate("connect_window", "Host IP"))
        self.ip_box.setPlaceholderText(_translate("connect_window", "255.255.255.255"))
        self.connect_button.setText(_translate("connect_window", "connect"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    connect_window = QtWidgets.QMainWindow()
    ui = Ui_connect_window()
    ui.setupUi(connect_window)
    connect_window.show()
    sys.exit(app.exec_())

