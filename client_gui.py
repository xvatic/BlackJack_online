# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'client_gui.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(885, 676)
        self.groupBox_LogIn = QtWidgets.QGroupBox(Form)
        self.groupBox_LogIn.setGeometry(QtCore.QRect(320, 280, 241, 121))
        self.groupBox_LogIn.setObjectName("groupBox_LogIn")
        self.lineEdit_login = QtWidgets.QLineEdit(self.groupBox_LogIn)
        self.lineEdit_login.setGeometry(QtCore.QRect(30, 30, 181, 21))
        self.lineEdit_login.setObjectName("lineEdit_login")
        self.lineEdit_2_password = QtWidgets.QLineEdit(self.groupBox_LogIn)
        self.lineEdit_2_password.setGeometry(QtCore.QRect(30, 60, 181, 21))
        self.lineEdit_2_password.setObjectName("lineEdit_2_password")
        self.pushButton_connect = QtWidgets.QPushButton(self.groupBox_LogIn)
        self.pushButton_connect.setGeometry(QtCore.QRect(0, 80, 113, 32))
        self.pushButton_connect.setObjectName("pushButton_connect")
        self.pushButton_register = QtWidgets.QPushButton(self.groupBox_LogIn)
        self.pushButton_register.setGeometry(QtCore.QRect(120, 80, 113, 32))
        self.pushButton_register.setObjectName("pushButton_register")
        self.groupBox_Enter = QtWidgets.QGroupBox(Form)
        self.groupBox_Enter.setGeometry(QtCore.QRect(230, 140, 431, 150))
        self.groupBox_Enter.setObjectName("groupBox_Enter")
        self.comboBox = QtWidgets.QComboBox(self.groupBox_Enter)
        self.comboBox.setGeometry(QtCore.QRect(30, 0, 181, 61))
        self.comboBox.setObjectName("comboBox")
        self.pushButton_creategame = QtWidgets.QPushButton(self.groupBox_Enter)
        self.pushButton_creategame.setGeometry(QtCore.QRect(110, 50, 113, 32))
        self.pushButton_creategame.setObjectName("pushButton_creategame")
        self.pushButton_choosegame = QtWidgets.QPushButton(self.groupBox_Enter)
        self.pushButton_choosegame.setGeometry(QtCore.QRect(0, 50, 113, 32))
        self.pushButton_choosegame.setObjectName("pushButton_choosegame")
        self.lineEdit_gamename = QtWidgets.QLineEdit(self.groupBox_Enter)
        self.lineEdit_gamename.setGeometry(QtCore.QRect(30, 80, 181, 21))
        self.lineEdit_gamename.setObjectName("lineEdit_gamename")
        self.lineEdit_gamepassword = QtWidgets.QLineEdit(self.groupBox_Enter)
        self.lineEdit_gamepassword.setGeometry(QtCore.QRect(30, 110, 181, 21))
        self.lineEdit_gamepassword.setObjectName("lineEdit_gamename")
        self.lineEdit_code = QtWidgets.QLineEdit(self.groupBox_Enter)
        self.lineEdit_code.setGeometry(QtCore.QRect(220, 70, 121, 21))
        self.lineEdit_code.setObjectName("lineEdit_code")
        self.label_money = QtWidgets.QLabel(self.groupBox_Enter)
        self.label_money.setGeometry(QtCore.QRect(340, 30, 131, 21))
        self.label_money.setObjectName("label_money")
        self.pushButton_activate = QtWidgets.QPushButton(self.groupBox_Enter)
        self.pushButton_activate.setGeometry(QtCore.QRect(220, 30, 113, 32))
        self.pushButton_activate.setObjectName("pushButton_activate")
        self.groupBox_Game = QtWidgets.QGroupBox(Form)
        self.groupBox_Game.setGeometry(QtCore.QRect(50, 20, 791, 631))
        self.groupBox_Game.setObjectName("groupBox_Game")
        self.label_message2 = QtWidgets.QLabel(self.groupBox_Game)
        self.label_message2.setGeometry(QtCore.QRect(440, 40, 131, 21))
        self.label_message2.setObjectName("label_message2")
        self.label_player2 = QtWidgets.QLabel(self.groupBox_Game)
        self.label_player2.setGeometry(QtCore.QRect(200, 190, 131, 21))
        self.label_player2.setObjectName("label_player2")
        self.label_Player_pic_2 = QtWidgets.QLabel(self.groupBox_Game)
        self.label_Player_pic_2.setGeometry(QtCore.QRect(320, 70, 131, 141))
        self.label_Player_pic_2.setText("")
        self.label_Player_pic_2.setPixmap(QtGui.QPixmap("Files/playericon.png"))
        self.label_Player_pic_2.setScaledContents(True)
        self.label_Player_pic_2.setObjectName("label_Player_pic_2")
        self.label_message3 = QtWidgets.QLabel(self.groupBox_Game)
        self.label_message3.setGeometry(QtCore.QRect(630, 180, 131, 21))
        self.label_message3.setObjectName("label_message3")
        self.label_player3 = QtWidgets.QLabel(self.groupBox_Game)
        self.label_player3.setGeometry(QtCore.QRect(590, 370, 131, 21))
        self.label_player3.setObjectName("label_player3")
        self.label_Player_pic_3 = QtWidgets.QLabel(self.groupBox_Game)
        self.label_Player_pic_3.setGeometry(QtCore.QRect(580, 210, 131, 141))
        self.label_Player_pic_3.setText("")
        self.label_Player_pic_3.setPixmap(QtGui.QPixmap("Files/playericon.png"))
        self.label_Player_pic_3.setScaledContents(True)
        self.label_Player_pic_3.setObjectName("label_Player_pic_3")
        self.label_message1 = QtWidgets.QLabel(self.groupBox_Game)
        self.label_message1.setGeometry(QtCore.QRect(20, 190, 131, 21))
        self.label_message1.setObjectName("label_message1")
        self.label_player1 = QtWidgets.QLabel(self.groupBox_Game)
        self.label_player1.setGeometry(QtCore.QRect(20, 370, 131, 21))
        self.label_player1.setObjectName("label_player1")
        self.label_Player_pic = QtWidgets.QLabel(self.groupBox_Game)
        self.label_Player_pic.setGeometry(QtCore.QRect(40, 220, 131, 141))
        self.label_Player_pic.setText("")
        self.label_Player_pic.setPixmap(QtGui.QPixmap("Files/playericon.png"))
        self.label_Player_pic.setScaledContents(True)
        self.label_Player_pic.setObjectName("label_Player_pic")
        self.pushButton_enough = QtWidgets.QPushButton(self.groupBox_Game)
        self.pushButton_enough.setGeometry(QtCore.QRect(390, 410, 131, 51))
        self.pushButton_enough.setObjectName("pushButton_enough")
        self.pushButton_take = QtWidgets.QPushButton(self.groupBox_Game)
        self.pushButton_take.setGeometry(QtCore.QRect(240, 410, 131, 51))
        self.pushButton_take.setObjectName("pushButton_take")
        self.pushButton_send = QtWidgets.QPushButton(self.groupBox_Game)
        self.pushButton_send.setGeometry(QtCore.QRect(170, 500, 113, 32))
        self.pushButton_send.setObjectName("pushButton_send")
        self.lineEdit_message = QtWidgets.QLineEdit(self.groupBox_Game)
        self.lineEdit_message.setGeometry(QtCore.QRect(160, 550, 121, 21))
        self.lineEdit_message.setObjectName("lineEdit_message")
        self.pushButton_leave = QtWidgets.QPushButton(self.groupBox_Game)
        self.pushButton_leave.setGeometry(QtCore.QRect(10, 530, 113, 32))
        self.pushButton_leave.setObjectName("pushButton_leave")
        self.lineEdit_bet = QtWidgets.QLineEdit(self.groupBox_Game)
        self.lineEdit_bet.setGeometry(QtCore.QRect(540, 460, 121, 21))
        self.lineEdit_bet.setObjectName("lineEdit_bet")
        self.pushButton = QtWidgets.QPushButton(self.groupBox_Game)
        self.pushButton.setGeometry(QtCore.QRect(540, 500, 113, 32))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox_LogIn.setTitle(_translate("Form", "GroupBox_LogIn"))
        self.pushButton_connect.setText(_translate("Form", "Connect"))
        self.pushButton_register.setText(_translate("Form", "Register"))
        self.groupBox_Enter.setTitle(_translate("Form", "GroupBox"))
        self.pushButton_creategame.setText(_translate("Form", "Create"))
        self.pushButton_choosegame.setText(_translate("Form", "Enter"))
        self.label_money.setText(_translate("Form", "BALANCE"))
        self.pushButton_activate.setText(_translate("Form", "PushButton"))
        self.groupBox_Game.setTitle(_translate("Form", "GroupBox"))
        self.label_message2.setText(_translate("Form", "m2"))
        self.label_player2.setText(_translate("Form", "player2"))
        self.label_message3.setText(_translate("Form", "m3"))
        self.label_player3.setText(_translate("Form", "player3"))
        self.label_message1.setText(_translate("Form", "m1"))
        self.label_player1.setText(_translate("Form", "player1"))
        self.pushButton_enough.setText(_translate("Form", "ENOUGH"))
        self.pushButton_take.setText(_translate("Form", "TAKE"))
        self.pushButton_send.setText(_translate("Form", "Send"))
        self.pushButton_leave.setText(_translate("Form", "Leave"))
        self.pushButton.setText(_translate("Form", "Bet"))
