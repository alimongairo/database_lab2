from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_StudentDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 228)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(-10, 180, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.lineEdit_name = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_name.setGeometry(QtCore.QRect(100, 20, 220, 22))
        self.lineEdit_name.setObjectName("lineEdit_name")
        self.label_name = QtWidgets.QLabel(Dialog)
        self.label_name.setGeometry(QtCore.QRect(30, 20, 55, 16))
        self.label_name.setObjectName("label_name")
        self.lineEdit_phone = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_phone.setGeometry(QtCore.QRect(100, 100, 220, 22))
        self.lineEdit_phone.setObjectName("lineEdit_phone")
        self.label_phone = QtWidgets.QLabel(Dialog)
        self.label_phone.setGeometry(QtCore.QRect(30, 100, 55, 16))
        self.label_phone.setObjectName("label_phone")
        self.lineEdit_surname = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_surname.setGeometry(QtCore.QRect(100, 60, 220, 22))
        self.lineEdit_surname.setObjectName("lineEdit_surname")
        self.label_surname = QtWidgets.QLabel(Dialog)
        self.label_surname.setGeometry(QtCore.QRect(30, 60, 55, 16))
        self.label_surname.setObjectName("label_surname")
        self.label_note = QtWidgets.QLabel(Dialog)
        self.label_note.setGeometry(QtCore.QRect(30, 140, 55, 16))
        self.label_note.setObjectName("label_note")
        self.lineEdit_note = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_note.setGeometry(QtCore.QRect(100, 140, 220, 22))
        self.lineEdit_note.setObjectName("lineEdit_note")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept) # type: ignore
        self.buttonBox.rejected.connect(Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Student"))
        self.label_name.setText(_translate("Dialog", "Name"))
        self.label_phone.setText(_translate("Dialog", "Phone"))
        self.label_surname.setText(_translate("Dialog", "Surname"))
        self.label_note.setText(_translate("Dialog", "Note"))
