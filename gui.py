# -*- coding: utf-8 -*-
import datetime

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *


"""
sources for GUI
https://biapol.github.io/blog/johannes_mueller/entry_user_interf2/Readme.html?_gl=1*zwtvqf*_gcl_au*MTA2NDgyNTg0OS4xNzEzNjMyNjcz*_ga*MTIzMDQ0MjYwMy4xNzEzNjMyNjY3*_ga_MBTGG7KX5Y*MTcxOTg3Nzc5Mi40LjEuMTcxOTg3Nzk5OS4wLjAuMA..
https://stackoverflow.com/questions/68316364/pyqt5-qgraphicsview-width-and-height?_gl=1*zwtvqf*_gcl_au*MTA2NDgyNTg0OS4xNzEzNjMyNjcz*_ga*MTIzMDQ0MjYwMy4xNzEzNjMyNjY3*_ga_MBTGG7KX5Y*MTcxOTg3Nzc5Mi40LjEuMTcxOTg3Nzk5OS4wLjAuMA..
https://gist.github.com/trin94/0b61a7476f276c1f7648172d950041a5?_gl=1*zwtvqf*_gcl_au*MTA2NDgyNTg0OS4xNzEzNjMyNjcz*_ga*MTIzMDQ0MjYwMy4xNzEzNjMyNjY3*_ga_MBTGG7KX5Y*MTcxOTg3Nzc5Mi40LjEuMTcxOTg3Nzk5OS4wLjAuMA..
https://stackoverflow.com/questions/52797269/having-trouble-opening-multiple-windows-in-pyqt5?_gl=1*zwtvqf*_gcl_au*MTA2NDgyNTg0OS4xNzEzNjMyNjcz*_ga*MTIzMDQ0MjYwMy4xNzEzNjMyNjY3*_ga_MBTGG7KX5Y*MTcxOTg3Nzc5Mi40LjEuMTcxOTg3Nzk5OS4wLjAuMA..
"""

"""
that's a GUI code, adaptive, based on Grids
"""


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1609, 760)

        font = QtGui.QFont()
        font.setFamily("Arial")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.hb_layout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.hb_layout.setObjectName("verticalLayout")
        self.v_layout = QtWidgets.QVBoxLayout()
        self.v2_layout = QtWidgets.QVBoxLayout()

        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")

        self.top_buttons_layout = QtWidgets.QHBoxLayout()
        self.Station_lb = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.Station_lb.setFont(font)
        self.Station_lb.setObjectName("label_24")
        self.Station_lb.setText("Station:")

        self.station_tb = QtWidgets.QTextEdit(self.centralwidget)
        self.station_tb.setTabChangesFocus(True)
        self.station_tb.setFont(font)
        self.station_tb.setMaximumHeight(30)
        self.station_tb.setObjectName("station_tv")

        self.max_empl_label = QtWidgets.QLabel(self.centralwidget)
        self.max_empl_label.setFont(font)
        self.max_empl_label.setObjectName("tag_label")
        self.max_empl_label.setText("Max Empl.:")

        self.max_empl_tb = QtWidgets.QTextEdit(self.centralwidget)
        self.max_empl_tb.setTabChangesFocus(True)
        self.max_empl_tb.setFont(font)
        self.max_empl_tb.setMaximumHeight(30)
        self.max_empl_tb.setObjectName("max_empl_tb")

        self.second_buttons_layput = QtWidgets.QHBoxLayout()

        font = QtGui.QFont()
        font.setPointSize(20)

        self.random_labor_btn = QtWidgets.QPushButton()
        self.random_labor_btn.setFont(font)
        self.random_labor_btn.setObjectName("create_event_btn")
        self.random_labor_btn.setText("Random Labor")

        self.export_to_excel = QtWidgets.QPushButton()
        self.export_to_excel.setFont(font)
        self.export_to_excel.setObjectName("export_to_excel")

        self.import_from_excel = QtWidgets.QPushButton()
        self.import_from_excel.setFont(font)
        self.import_from_excel.setObjectName("export_excel_btn")

        self.new_employee_btn = QtWidgets.QPushButton()
        self.new_employee_btn.setFont(font)
        self.new_employee_btn.setObjectName("new_employee_btn")

        self.delete_empl = QtWidgets.QPushButton()
        self.delete_empl.setFont(font)
        self.delete_empl.setObjectName("delete_empl")

        self.top_buttons_layout.addWidget(self.Station_lb)
        self.top_buttons_layout.addWidget(self.station_tb)
        self.top_buttons_layout.addWidget(self.max_empl_label)
        self.top_buttons_layout.addWidget(self.max_empl_tb)

        self.second_buttons_layput.addWidget(self.random_labor_btn)
        self.second_buttons_layput.addWidget(self.export_to_excel)
        self.second_buttons_layput.addWidget(self.import_from_excel)
        self.second_buttons_layput.addWidget(self.new_employee_btn)
        self.second_buttons_layput.addWidget(self.delete_empl)

        self.revoke_selected_btn = QtWidgets.QPushButton()
        font = QtGui.QFont()
        font.setPointSize(14)
        self.revoke_selected_btn.setFont(font)
        self.revoke_selected_btn.setObjectName("revoke_selected_btn")
        self.revoke_selected_btn.setText("Revoke selected")
        self.gridLayout.addWidget(self.revoke_selected_btn, 11, 0, 1, 3)

        self.assign_label = QtWidgets.QLabel(self.centralwidget)
        self.assign_label.setText("Assign employee:")
        self.assign_label.setMaximumHeight(25)
        self.gridLayout.addWidget(self.assign_label, 11, 3, 1, 3)

        self.available_empl_cb = QtWidgets.QComboBox(self.centralwidget)
        self.available_empl_cb.setFont(font)
        self.available_empl_cb.setMaximumHeight(25)

        self.gridLayout.addWidget(self.available_empl_cb, 11, 6, 1, 3)

        self.confirm_assignment = QtWidgets.QPushButton()
        self.confirm_assignment.setFont(font)
        self.confirm_assignment.setObjectName("confirm_assignment")
        self.confirm_assignment.setText("Confirm assignment")
        self.gridLayout.addWidget(self.confirm_assignment, 11, 9, 1, 5)

        self.event_train_label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.event_train_label.setFont(font)
        self.event_train_label.setObjectName("label_24")
        self.event_train_label.setText("TRAIN EMPLOYEE")
        self.event_train_label.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.event_train_label, 4, 15, 1, 1)

        self.event_editor_label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.event_editor_label.setFont(font)
        self.event_editor_label.setObjectName("label_24")
        self.event_editor_label.setText("EMPLOYEE EDITOR")
        self.event_editor_label.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.event_editor_label, 0, 15, 1, 1)

        font = QtGui.QFont()
        font.setPointSize(14)
        self.name_label = QtWidgets.QLabel(self.centralwidget)
        self.name_label.setFont(font)
        self.name_label.setObjectName("label_24")
        self.name_label.setText("ID:(), LAST NAME,FIRST NAME:")
        self.name_label.setMaximumHeight(45)
        self.gridLayout.addWidget(self.name_label, 1, 14, 1, 1)

        self.name_tb = QtWidgets.QLineEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.name_tb.setFont(font)
        self.name_tb.setMaximumHeight(35)
        self.gridLayout.addWidget(self.name_tb, 2, 14, 1, 6)




        self.employee_lbl = QtWidgets.QLabel(self.centralwidget)
        self.employee_lbl.setFont(font)
        self.employee_lbl.setObjectName("label_24")
        self.employee_lbl.setText("Employee:")
        self.employee_lbl.setMaximumHeight(25)
        self.gridLayout.addWidget(self.employee_lbl, 5, 14, 1, 1)

        self.employee_cb = QtWidgets.QComboBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.employee_cb.setFont(font)
        self.employee_cb.setMinimumHeight(35)
        self.gridLayout.addWidget(self.employee_cb, 6, 14, 1, 6)

        self.time_from_label = QtWidgets.QLabel(self.centralwidget)
        self.time_from_label.setFont(font)
        self.time_from_label.setObjectName("label_24")
        self.time_from_label.setText("Last worked:")
        self.time_from_label.setMaximumHeight(25)
        self.gridLayout.addWidget(self.time_from_label, 9, 14, 1, 1)

        self.last_worked_tm = QtWidgets.QDateEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.last_worked_tm.setFont(font)
        # self.last_worked_tm.setDisplayFormat("dd-mm-YYYY")
        self.last_worked_tm.setMinimumHeight(35)
        d = QtCore.QDate.fromString(datetime.datetime.now().strftime('%d-%m-%Y'), 'dd-MM-yyyy')

        self.last_worked_tm.setDate(d)
        self.gridLayout.addWidget(self.last_worked_tm, 10, 14, 1, 6)

        self.station_lbl = QtWidgets.QLabel(self.centralwidget)
        self.station_lbl.setFont(font)
        self.station_lbl.setObjectName("label_24")
        self.station_lbl.setText("Station:")
        self.station_lbl.setMaximumHeight(25)
        self.gridLayout.addWidget(self.station_lbl, 7, 14, 1, 1)

        self.station_cb = QtWidgets.QComboBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.station_cb.setFont(font)
        self.station_cb.setMinimumHeight(35)
        self.gridLayout.addWidget(self.station_cb, 8, 14, 1, 6)

        self.save_changes_btn = QtWidgets.QPushButton()
        font = QtGui.QFont()
        font.setPointSize(17)
        self.save_changes_btn.setFont(font)
        self.save_changes_btn.setObjectName("start_btn6")
        self.gridLayout.addWidget(self.save_changes_btn, 11, 14, 1, 6)

        self.save_changes_btn1 = QtWidgets.QPushButton()
        font = QtGui.QFont()
        font.setPointSize(17)
        self.save_changes_btn1.setFont(font)
        self.save_changes_btn1.setObjectName("start_btn7")
        self.gridLayout.addWidget(self.save_changes_btn1, 3, 14, 1, 6)

        self.tableView_labor = QtWidgets.QTableView(self.centralwidget)
        self.tableView_labor.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)  # <---
        self.tableView_labor.setAlternatingRowColors(True)
        self.tableView_labor.setMinimumWidth(950)

        self.tableView_labor.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView_labor.setObjectName("tableView")
        font = QtGui.QFont()
        font.setPointSize(12)
        self.tableView_labor.setFont(font)

        self.gridLayout.addWidget(self.tableView_labor, 0, 0, 11, 14)

        font = QtGui.QFont()
        font.setPointSize(14)
        self.stations_list = QtWidgets.QListWidget(self.centralwidget)
        self.stations_list.setMinimumSize(250, 400)
        self.stations_list.setMaximumWidth(400)
        self.stations_list.setObjectName("main_tf")
        self.stations_list.setFont(font)

        self.reset_labor_btn = QtWidgets.QPushButton(self.centralwidget)
        self.reset_labor_btn.setFont(font)
        self.reset_labor_btn.setMaximumHeight(110)
        self.reset_labor_btn.setMaximumWidth(420)
        self.reset_labor_btn.setText("RESET LABOR")

        self.reset_labor_btn.setObjectName("name_tb1")
        self.v_layout.addWidget(self.reset_labor_btn)
        self.v_layout.addWidget(self.stations_list)

        self.hb_layout.addLayout(self.v_layout)
        self.v2_layout.addLayout(self.top_buttons_layout)
        self.v2_layout.addLayout(self.second_buttons_layput)
        self.v2_layout.addLayout(self.gridLayout)
        self.hb_layout.addLayout(self.v2_layout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        MainWindow.setWindowTitle(_translate("MainWindow", "Labor Plan v5"))
        self.export_to_excel.setText(_translate("MainWindow", "Export to Excel"))
        self.import_from_excel.setText(_translate("MainWindow", "Import from Excel"))
        self.new_employee_btn.setText(_translate("MainWindow", "New Employee"))
        self.delete_empl.setText(_translate("MainWindow", "Delete Employee"))

        self.save_changes_btn.setText(_translate("MainWindow", "Set Last Worked"))
        self.save_changes_btn1.setText(_translate("MainWindow", "Save"))
