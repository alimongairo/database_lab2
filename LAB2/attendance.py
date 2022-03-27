from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AttendanceDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 228)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(-10, 180, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.lineEdit_st_id = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_st_id.setGeometry(QtCore.QRect(100, 20, 220, 22))
        self.lineEdit_st_id.setObjectName("lineEdit_st_id")
        self.label_st_id = QtWidgets.QLabel(Dialog)
        self.label_st_id.setGeometry(QtCore.QRect(30, 20, 55, 16))
        self.label_st_id.setObjectName("label_st_id")
        self.lineEdit_cls_id = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_cls_id.setGeometry(QtCore.QRect(100, 100, 220, 22))
        self.lineEdit_cls_id.setObjectName("lineEdit_cls_id")
        self.label_cls_id = QtWidgets.QLabel(Dialog)
        self.label_cls_id.setGeometry(QtCore.QRect(30, 100, 55, 16))
        self.label_cls_id.setObjectName("label_cls_id")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept) # type: ignore
        self.buttonBox.rejected.connect(Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Attendance"))
        self.label_st_id.setText(_translate("Dialog", "Student ID"))
        self.label_cls_id.setText(_translate("Dialog", "Class ID"))
