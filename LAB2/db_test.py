from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QInputDialog, QMessageBox
import sys
import time
import pandas as pd

import postgres_func
import ui_main_win
import createdb
import table_model
import student
import attendance


class main():
    def __init__(self):
        self.MainWin = QMainWindow()
        self.ui_mw = ui_main_win.UIMain()
        self.ui_mw.setupUi(self.MainWin)

    def createDB(self):
        ret = QMessageBox.question(self.MainWin, 'Message', "Are you sure to recreate DB?", QMessageBox.Yes | QMessageBox.Cancel)
        if ret == QMessageBox.Yes:
            postgres_func.create_db()

    def deleteDB(self):
        ret = QMessageBox.question(self.MainWin, 'Message', "Are you sure to delete DB?", QMessageBox.Yes | QMessageBox.Cancel)
        if ret == QMessageBox.Yes:
            postgres_func.delete_db()

    def deleteContent(self):
        table_name,ok = QInputDialog.getText(self.MainWin, 'Input Dialog', 'Enter table name:')
        if ok:
            ret = QMessageBox.question(self.MainWin, 'Message', "Are you sure to delete content?", QMessageBox.Yes | QMessageBox.Cancel)
            if ret == QMessageBox.Yes:
                postgres_func.delete_table(table_name)

    def deleteAllContent(self):
        ret = QMessageBox.question(self.MainWin, 'Message', "Are you sure to delete all content?", QMessageBox.Yes | QMessageBox.Cancel)
        if ret == QMessageBox.Yes:
            postgres_func.delete_table('students')
            postgres_func.delete_table('attendance')

    def showTable(self):
        t_name = 'teachers'
        data = postgres_func.get_teachers()
        self.table1 = table_model.TableViewWindow(t_name)
        if len(data) > 0:
            cols = dict(data[0]).keys()
            self.table1.setData(pd.DataFrame(data, columns = cols))
        self.table1.show()

        t_name = 'students'
        data = postgres_func.get_students()
        self.table2 = table_model.TableViewWindow(t_name)
        if len(data) > 0:
            cols = dict(data[0]).keys()
            self.table2.setData(pd.DataFrame(data, columns = cols))
        self.table2.show()

        t_name = 'attendance'
        data = postgres_func.get_attendance()
        self.table3 = table_model.TableViewWindow(t_name)
        if len(data) > 0:
            cols = dict(data[0]).keys()
            self.table3.setData(pd.DataFrame(data, columns = cols))
        self.table3.show()

        t_name = 'lessons'
        data = postgres_func.get_lessons()
        self.table4 = table_model.TableViewWindow(t_name)
        if len(data) > 0:
            cols = dict(data[0]).keys()
            self.table4.setData(pd.DataFrame(data, columns = cols))
        self.table4.show()

        t_name = 'timetable'
        data = postgres_func.get_timetable()
        self.table5 = table_model.TableViewWindow(t_name)
        if len(data) > 0:
            cols = dict(data[0]).keys()
            self.table5.setData(pd.DataFrame(data, columns = cols))
        self.table5.show()

    def addStudent(self):
        self.studentWin = QtWidgets.QDialog()
        self.st_ui = student.Ui_StudentDialog()
        self.st_ui.setupUi(self.studentWin)
        if self.studentWin.exec_():
            name = self.st_ui.lineEdit_name.text()
            surname = self.st_ui.lineEdit_surname.text()
            phone = self.st_ui.lineEdit_phone.text()
            postgres_func.add_student(name, surname, phone)

    def editStudent(self):
        stud_id, ok = QInputDialog.getText(self.MainWin, 'Input Dialog', 'Enter student id:')
        if ok:
            res = postgres_func.get_stud_by_id(stud_id)
        self.studentWin = QtWidgets.QDialog()
        self.st_ui = student.Ui_StudentDialog()
        self.st_ui.setupUi(self.studentWin)
        self.st_ui.lineEdit_name.setText(res[1])
        self.st_ui.lineEdit_surname.setText(res[2])
        self.st_ui.lineEdit_phone.setText(res[3])
        if self.studentWin.exec_():
            name = self.st_ui.lineEdit_name.text()
            surname = self.st_ui.lineEdit_surname.text()
            phone = self.st_ui.lineEdit_phone.text()
            postgres_func.edit_stud_by_id(stud_id, name, surname, phone)

    def addAttend(self):
        self.studentWin = QtWidgets.QDialog()
        self.atd_ui = attendance.Ui_AttendanceDialog()
        self.atd_ui.setupUi(self.studentWin)
        if self.studentWin.exec_():
            st_id = self.atd_ui.lineEdit_st_id.text()
            cls_id = self.atd_ui.lineEdit_cls_id.text()
            postgres_func.add_attendance(cls_id, st_id)

    def deleteAttend(self):
        stud_id, ok = QInputDialog.getText(self.MainWin, 'Input Dialog', 'Enter Class ID:')
        if ok:
            ret = QMessageBox.question(self.MainWin, 'Message', "Are you sure to delete class attendance?", QMessageBox.Yes | QMessageBox.Cancel)
            if ret == QMessageBox.Yes:
                postgres_func.delete_attendance(stud_id)

    def deleteStudent(self):
        stud_surname, ok = QInputDialog.getText(self.MainWin, 'Input Dialog', 'Enter student surname:')
        if ok:
            res = postgres_func.get_student_by_name(stud_surname)
            ret = QMessageBox.question(self.MainWin, 'Message', "Are you sure to delete student?", QMessageBox.Yes | QMessageBox.Cancel)
            if ret == QMessageBox.Yes:
                postgres_func.delete_student_by_name(res)

    def searchStudent(self):
        stud_surname, ok = QInputDialog.getText(self.MainWin, 'Input Dialog', 'Enter student surname:')
        if ok:
            t_name = 'search result'
            data = postgres_func.search_students_by_name(stud_surname)
            self.sres_table = table_model.TableViewWindow(t_name)
            if len(data) > 0:
                cols = dict(data[0]).keys()
                self.sres_table.setData(pd.DataFrame(data, columns=cols))
            self.sres_table.show()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    m = main()

    m.ui_mw.pushButton_create.clicked.connect(m.createDB)
    m.ui_mw.pushButton_delete.clicked.connect(m.deleteDB)

    m.ui_mw.pushButton_show.clicked.connect(m.showTable)
    m.ui_mw.pushButton_searchStudent.clicked.connect(m.searchStudent)
    m.ui_mw.pushButton_contDelete.clicked.connect(m.deleteContent)
    m.ui_mw.pushButton_allContDelete.clicked.connect(m.deleteAllContent)

    m.ui_mw.pushButton_addStudent.clicked.connect(m.addStudent)
    m.ui_mw.pushButton_editStudent.clicked.connect(m.editStudent)

    m.ui_mw.pushButton_addAttend.clicked.connect(m.addAttend)
    m.ui_mw.pushButton_deleteAttend.clicked.connect(m.deleteAttend)

    m.ui_mw.pushButton_deleteStudent.clicked.connect(m.deleteStudent)

    m.MainWin.show()

    sys.exit(app.exec_())
