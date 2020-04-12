# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uic/main-menu.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TPRMainMenu(object):
    def setupUi(self, TPRMainMenu):
        TPRMainMenu.setObjectName("TPRMainMenu")
        TPRMainMenu.resize(400, 400)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(TPRMainMenu.sizePolicy().hasHeightForWidth())
        TPRMainMenu.setSizePolicy(sizePolicy)
        TPRMainMenu.setMinimumSize(QtCore.QSize(400, 400))
        TPRMainMenu.setMaximumSize(QtCore.QSize(400, 400))
        self.MainMenuWidget = QtWidgets.QWidget(TPRMainMenu)
        self.MainMenuWidget.setObjectName("MainMenuWidget")
        self.txt_username = QtWidgets.QLineEdit(self.MainMenuWidget)
        self.txt_username.setGeometry(QtCore.QRect(60, 150, 281, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.txt_username.setFont(font)
        self.txt_username.setAlignment(QtCore.Qt.AlignCenter)
        self.txt_username.setPlaceholderText("")
        self.txt_username.setObjectName("txt_username")
        self.btn_join_game = QtWidgets.QPushButton(self.MainMenuWidget)
        self.btn_join_game.setGeometry(QtCore.QRect(60, 220, 281, 51))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.btn_join_game.setFont(font)
        self.btn_join_game.setObjectName("btn_join_game")
        self.btn_host_game = QtWidgets.QPushButton(self.MainMenuWidget)
        self.btn_host_game.setGeometry(QtCore.QRect(60, 300, 281, 51))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.btn_host_game.setFont(font)
        self.btn_host_game.setObjectName("btn_host_game")
        self.lbl_main_menu = QtWidgets.QLabel(self.MainMenuWidget)
        self.lbl_main_menu.setGeometry(QtCore.QRect(60, 30, 281, 71))
        self.lbl_main_menu.setMinimumSize(QtCore.QSize(181, 51))
        font = QtGui.QFont()
        font.setPointSize(38)
        self.lbl_main_menu.setFont(font)
        self.lbl_main_menu.setTextFormat(QtCore.Qt.PlainText)
        self.lbl_main_menu.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_main_menu.setObjectName("lbl_main_menu")
        self.label = QtWidgets.QLabel(self.MainMenuWidget)
        self.label.setGeometry(QtCore.QRect(70, 120, 260, 20))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        TPRMainMenu.setCentralWidget(self.MainMenuWidget)
        self.statusbar = QtWidgets.QStatusBar(TPRMainMenu)
        self.statusbar.setObjectName("statusbar")
        TPRMainMenu.setStatusBar(self.statusbar)

        self.retranslateUi(TPRMainMenu)
        QtCore.QMetaObject.connectSlotsByName(TPRMainMenu)

    def retranslateUi(self, TPRMainMenu):
        _translate = QtCore.QCoreApplication.translate
        TPRMainMenu.setWindowTitle(_translate("TPRMainMenu", "Tiny PyRPG"))
        self.btn_join_game.setText(_translate("TPRMainMenu", "Join Game"))
        self.btn_host_game.setText(_translate("TPRMainMenu", "Host Game"))
        self.lbl_main_menu.setText(_translate("TPRMainMenu", "Main Menu"))
        self.label.setText(_translate("TPRMainMenu", "Username"))
