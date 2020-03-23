# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Jeffrey Smith\Desktop\main_menu.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_main_window(object):
    def setupUi(self, main_window):
        main_window.setObjectName("main_window")
        main_window.resize(1300, 900)
        self.centralwidget = QtWidgets.QWidget(main_window)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(460, 70, 351, 141))
        font = QtGui.QFont()
        font.setPointSize(42)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(400, 320, 471, 41))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.name_box = QtWidgets.QTextEdit(self.centralwidget)
        self.name_box.setGeometry(QtCore.QRect(400, 370, 471, 61))
        font = QtGui.QFont()
        font.setPointSize(28)
        self.name_box.setFont(font)
        self.name_box.setObjectName("name_box")
        self.host_game_button = QtWidgets.QPushButton(self.centralwidget)
        self.host_game_button.setGeometry(QtCore.QRect(400, 470, 471, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.host_game_button.setFont(font)
        self.host_game_button.setObjectName("host_game_button")
        self.join_game_button = QtWidgets.QPushButton(self.centralwidget)
        self.join_game_button.setGeometry(QtCore.QRect(400, 560, 471, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.join_game_button.setFont(font)
        self.join_game_button.setObjectName("join_game_button")
        main_window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(main_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1300, 21))
        self.menubar.setObjectName("menubar")
        main_window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(main_window)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)

        self.retranslateUi(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslateUi(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("main_window", "MainWindow"))
        self.label.setText(_translate("main_window", "Main Menu"))
        self.label_2.setText(_translate("main_window", "Name"))
        self.name_box.setHtml(_translate("main_window", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:28pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; text-align:center ;margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.host_game_button.setText(_translate("main_window", "Host Game"))
        self.join_game_button.setText(_translate("main_window", "Join Game"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    ui = Ui_main_window()
    ui.setupUi(main_window)
    main_window.show()
    sys.exit(app.exec_())

