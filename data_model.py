import datetime
import multiprocessing
import os.path
import time
import traceback
from gui import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
import sys
from PyQt5.QtWidgets import QMainWindow
import pandas as pd
import multiprocessing
from gui import Ui_MainWindow
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QBrush, QFont, QFontMetrics, QColor
from PyQt5.QtGui import QPixmap
import sys
from _thread import start_new_thread
from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView
import shutil

""""" 
sources
https://www.pythonguis.com/faq/editing-pyqt-tableview/?_gl=1*1wewnq0*_gcl_au*MTA2NDgyNTg0OS4xNzEzNjMyNjcz*_ga*MTIzMDQ0MjYwMy4xNzEzNjMyNjY3*_ga_MBTGG7KX5Y*MTcxOTg3Nzc5Mi40LjEuMTcxOTg3ODMyMS4wLjAuMA..
https://stackoverflow.com/questions/75444012/how-to-only-update-the-data-that-has-changed-in-qtableview-python?_gl=1*1wewnq0*_gcl_au*MTA2NDgyNTg0OS4xNzEzNjMyNjcz*_ga*MTIzMDQ0MjYwMy4xNzEzNjMyNjY3*_ga_MBTGG7KX5Y*MTcxOTg3Nzc5Mi40LjEuMTcxOTg3ODMyMS4wLjAuMA..
"""


class pandasModel(QAbstractTableModel):
    """
    data model to work with a TableViews
    """

    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data
        self.show_pass = True
        self.error_only = False

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():

            if role == Qt.DisplayRole or role == Qt.EditRole:
                if not self.show_pass and index.column() == 1:
                    value = self._data.iloc[index.row(), index.column()].split(':')[0]
                    return str(value)
                elif index.column() in [5, 6] and self._data.iloc[index.row(), index.column()] is None or str(
                        self._data.iloc[index.row(), index.column()]) == 'nan':
                    return '-'
                else:
                    value = self._data.iloc[index.row(), index.column()]
                    return str(value)
            try:
                if role == Qt.ForegroundRole:
                    if index.column() == 6:
                        if self._data.iloc[index.row(), index.column()] == 'ERROR':
                            return QtGui.QBrush(QtCore.Qt.red)
                        if self._data.iloc[index.row(), index.column()] == 'VALID':
                            return QtGui.QBrush(QtCore.Qt.green)
                        if self._data.iloc[index.row(), index.column()] == 'TIMEOUT':
                            return QBrush(QColor(255, 142, 40))
            except:
                print(traceback.format_exc())
                return QtGui.QBrush(QtCore.Qt.black)

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled

    def setData(self, index, value, role):
        if role == Qt.EditRole:
            self._data.iloc[index.row(), index.column()] = value
            if index.column() not in [0]:
                df_to_sql(self._data)
            return True

        return False
