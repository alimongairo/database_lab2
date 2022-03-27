import sys
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt


class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])


class TableViewWindow(QtWidgets.QMainWindow):
    def __init__(self,table_name):
        super().__init__()

        self.table = QtWidgets.QTableView()
        self.resize(600, 250)
        self.setWindowTitle(table_name)
        self.model = TableModel(pd.DataFrame([[]], columns = []))
        self.table.setModel(self.model)
        self.setCentralWidget(self.table)

    def setData(self, data):
        self.model = TableModel(data)
        self.table.setModel(self.model)

# app=QtWidgets.QApplication(sys.argv)
# window=TableViewWindow()
# window.show()
# app.exec_()


