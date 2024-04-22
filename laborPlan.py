import copy
from data_model import *
import multiprocessing
from gui import Ui_MainWindow
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView
import data_layer
import sys
import random
import json


def read_json(config_file):
    """
    reads json files
    :param config_file:
    :return:
    """
    try:
        print(config_file)
        with open(config_file, 'r') as f:
            config = json.load(f)
        return config
    except Exception as e:
        print("Exception in read_json: {}".format(str(e)))
        print(traceback.format_exc())


header = ["id", "Name", "Last Worked", "Status"]


class Application(QMainWindow, Ui_MainWindow):
    """
    The main application class
    """

    def __init__(self, parent=None):
        """
        initialize the Application
        :param parent:
        """
        try:
            super(Application, self).__init__(parent)
            # load the GUI
            self.setupUi(self)
            self.set_state('start')

            self.update_stations_list()
            self.stations = list(read_json("stations.json").keys())

            self.import_from_excel.clicked.connect(self.import_excel)
            self.export_to_excel.clicked.connect(self.export_excel)
            self.tableView_labor.doubleClicked.connect(self.edit_labor)
            self.save_changes_btn.clicked.connect(self.save_changes_training)
            self.save_changes_btn1.clicked.connect(self.save_changes_name)

            self.new_employee_btn.clicked.connect(self.create_new_employee)
            self.stations_list.itemClicked.connect(self.select_station)
            self.confirm_assignment.clicked.connect(self.assign_employee)
            self.revoke_selected_btn.clicked.connect(self.revoke_employee)
            self.delete_empl.clicked.connect(self.delete_employee)
            self.reset_labor_btn.clicked.connect(self.reset_labor)
            self.random_labor_btn.clicked.connect(self.random_labor)
            self.update_combo_boxes()

            self.new_employee_mode = False

        except Exception as e:
            print("Exception in init: {}".format(str(e)))
            print(traceback.format_exc())

    def import_excel(self):
        """
        import the trainings from Excel
        :return:
        """
        filePath, filters = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Please select an Excel file', '', 'Excel (*.xlsx)')
        if filePath:
            data_layer.import_from_excel(filePath)
            self.alert("Imported")

    def export_excel(self):
        """
        export data to Excel
        :return:
        """
        filename, filter = QtWidgets.QFileDialog.getSaveFileName(
            self, 'Save file', '', 'Excel files(*.xlsx)')
        if not filename:
            return
        else:
            data_layer.save_to_excel(filename)
            self.alert("Saved to: {}".format(filename))

    def random_labor(self):
        """
        build a random labor plan based on the stations limits
        :return:
        """
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure you want to reset all the assignments and create a random labor?",
                                     QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            data_layer.reset_labor()
            stations = read_json('stations.json')
            for station, limit in stations.items():
                available = list(data_layer.select_trained_available_employee(station).tolist())
                n = limit
                # declaring list
                if n < len(available):
                    selection = random.sample(available, n)
                else:
                    selection = available
                for employee in selection:
                    data_layer.assign_employee_by_id(data_layer.select_employee_id_by_name(employee), station, True)
            self.update_labor_db(self.station_tb.toPlainText())

    def reset_labor(self):
        """
        reset all the assignments
        :return:
        """
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure you want to reset all the assignments?",
                                     QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            data_layer.reset_labor()
            self.update_labor_db(self.station_tb.toPlainText())

    def delete_employee(self):
        """
        completely delete an employee
        :return:
        """
        current_id = self.get_current_employee_id()
        if current_id:
            reply = QMessageBox.question(self, 'Message',
                                         "Are you sure to delete this employee from all the stations and labor plan?",
                                         QMessageBox.Yes |
                                         QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                data_layer.remove_employee_by_id(int(current_id))
                self.update_labor_db(self.station_tb.toPlainText())

    def update_combo_boxes(self):
        """
        Update combo boxes
        :return:
        """
        self.employee_cb.clear()
        employees = list(data_layer.select_all_employee())
        employees.insert(0, 'select employee...')
        self.employee_cb.addItems(employees)
        self.station_cb.clear()
        self.stations = list(read_json("stations.json").keys())

        stations = copy.deepcopy(self.stations)
        stations.insert(0, 'select station...')
        self.station_cb.addItems(stations)

        if self.station_tb.toPlainText():
            self.available_empl_cb.clear()
            available = list(data_layer.select_trained_available_employee(self.station_tb.toPlainText()).tolist())
            available.insert(0, 'select valid employee...')
            self.available_empl_cb.addItems(available)

    def save_changes_name(self):
        """
        save the new or updated employee
        :return:
        """
        if not self.new_employee_mode:
            empl_id = int(self.get_current_employee_id())
            data_layer.update_employee_name(empl_id, self.name_tb.text())
            self.update_labor_db(self.station_tb.toPlainText())
        else:
            res = data_layer.insert_employee(self.name_tb.text())
            self.alert(res)
            self.name_tb.clear()
            self.new_mode = False
        self.update_combo_boxes()

    def assign_employee(self):
        """
        assign employee to the station
        :return:
        """
        if "select" not in self.available_empl_cb.currentText():
            data_layer.assign_employee_by_id(data_layer.
                                             select_employee_id_by_name(self.available_empl_cb.currentText()),
                                             self.station_tb.toPlainText(), True)
            self.update_labor_db(self.station_tb.toPlainText())
        else:
            self.alert("Please select an employee first")

    def revoke_employee(self):
        """
        revoke employee from the station
        :return:
        """
        current_selected = self.get_current_employee_id()
        data_layer.assign_employee_by_id(int(current_selected),
                                         self.station_tb.toPlainText(), False)
        self.update_labor_db(self.station_tb.toPlainText())

    def alert(self, text):
        QMessageBox.about(self, "Info", text)

    def create_new_employee(self):
        """
        enable a New Employee mode
        :return:
        """
        self.new_employee_mode = True
        self.name_tb.clear()
        self.set_state("edit")
        self.name_label.setText("The new employee name:")

    def save_changes_training(self):
        """
        save the new training values
        :return:
        """
        try:
            employee = self.employee_cb.currentText()
            station = self.station_cb.currentText()
            date = self.last_worked_tm.date()
            if 'select' in employee or "select" in station:
                self.alert("Please select an employee and station first")
            else:
                res = data_layer.insert_training(data_layer.select_employee_id_by_name(employee), station,
                                                 date.toString('dd-MM-yyyy'))
                self.alert(res)
                self.update_combo_boxes()

        except Exception as e:
            print(traceback.format_exc())

    def select_station(self, schedule):
        """
        select new station at the left list
        :param schedule:
        :return:
        """
        self.new_mode = False
        self.new_employee_mode = False
        self.name_tb.clear()
        self.name_label.setText("ID:(), NAME:")

        self.update_labor_db(schedule.text())
        self.station_tb.setText(schedule.text().split(' |')[0])
        self.max_empl_tb.setText(schedule.text().split(' |')[1])
        self.set_state('selected')

    def update_labor_db(self, station):
        """
        update posts database and displays changes
        :param station:
        :return:
        """
        try:

            station = station.split(' | ')[0]
            self.new_mode = False
            assigned_empls = data_layer.select_all_assigned_by_station(station)
            self.globals_labor_df = assigned_empls
            self.globals_labor_df.columns = header
            self.model = pandasModel(self.globals_labor_df)
            self.tableView_labor.setModel(self.model)
            self.tableView_labor.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
            self.tableView_labor.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.set_site_policy()
            self.update_combo_boxes()

        except Exception as e:
            self.log("Exception in update_posts_db: {}".format(str(e)))

    def update_stations_list(self):
        """
        update the list of stations based on the .json file
        :return:
        """
        schedules = read_json("stations.json")
        schedules_data = []
        self.stations = []
        for k, v in schedules.items():
            schedules_data.append(k + ' | {} empl.'.format(v))
            self.stations.append(k)
        index = 0
        self.stations_list.clear()
        for schedule in schedules_data:
            self.stations_list.insertItem(index, schedule)
            index += 1

    def get_current_employee_id(self):
        """
        returns an ID of the current employee selected
        :return:
        """
        try:
            df_rows = sorted(set(index.row() for index in
                                 self.tableView_labor.selectedIndexes()))
            if df_rows == []:
                return False
            employee_id = [self.globals_labor_df.iloc[i]['id'] for i in df_rows][0]
            return employee_id
        except Exception as e:
            self.log("Exception in get_current_employee_id: {}".format(str(e)))

    def get_current_employee_name(self):
        """
        returns Name of the current employee selected
        :return:
        """
        try:
            df_rows = sorted(set(index.row() for index in
                                 self.tableView_labor.selectedIndexes()))

            if df_rows == []:
                return False
            employee_id = [self.globals_labor_df.iloc[i]['Name'] for i in df_rows][0]
            return employee_id
        except Exception as e:
            self.log("Exception in get_current_employee_name: {}".format(str(e)))

    def edit_labor(self):
        """
        enable the Edit mode
        :return:
        """
        self.set_state('edit')
        employee_name = self.get_current_employee_name()
        employee_id = self.get_current_employee_id()
        self.new_employee_mode = False
        self.name_tb.clear()
        self.name_label.setText("ID:({}), NAME:".format(employee_id))
        self.name_tb.setText(employee_name)

    def set_site_policy(self, initial=False):
        """
        set size policy of the Table view
        :return:
        """
        self.tableView_labor.setAlternatingRowColors(True)
        self.tableView_labor.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        if not initial:
            self.tableView_labor.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)

        self.tableView_labor.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableView_labor.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

    def set_editor_block_state(self, state, clear=True):
        self.save_changes_btn1.setEnabled(state)
        self.name_tb.setEnabled(state)

    def set_state(self, state):
        """
        chang state of the controls
        - locks and activates buttons depending on
        the current state of the system, just to be user-friendly
        :param state:
        :return:
        """
        try:
            if state == 'start':
                self.max_empl_tb.setEnabled(False)
                self.station_tb.setEnabled(False)
                self.tableView_labor.setEnabled(False)
                self.reset_labor_btn.setEnabled(True)
                self.export_to_excel.setEnabled(True)
                self.import_from_excel.setEnabled(True)
                self.new_employee_btn.setEnabled(True)
                self.delete_empl.setEnabled(False)

                self.set_editor_block_state(False)
                self.random_labor_btn.setEnabled(True)
                self.reset_labor_btn.setEnabled(True)

            if state == 'selected':
                self.available_empl_cb.setEnabled(True)
                self.confirm_assignment.setEnabled(True)
                self.max_empl_tb.setEnabled(False)
                self.station_tb.setEnabled(False)
                self.tableView_labor.setEnabled(True)
                self.reset_labor_btn.setEnabled(True)
                self.random_labor_btn.setEnabled(True)
                self.export_to_excel.setEnabled(True)
                self.import_from_excel.setEnabled(True)
                self.new_employee_btn.setEnabled(True)
                self.delete_empl.setEnabled(True)
                self.set_editor_block_state(False)

            if state == 'edit':
                self.set_editor_block_state(True)
                self.new_employee_btn.setEnabled(True)
                self.export_to_excel.setEnabled(True)

            if state == 'saved_changes':
                self.set_editor_block_state(False, clear=False)
                self.new_employee_btn.setEnabled(True)
                self.export_to_excel.setEnabled(True)
                self.export_csv_btn.setEnabled(True)
            self.update_combo_boxes()

        except Exception as e:
            print("Exception in set_state: {}".format(str(e)))
            print(traceback.format_exc())

    def log(self, message):
        """
        prints the output to the LOG panel and to the LOG.txt file
        :param message:
        :return:
        """
        try:
            appl.processEvents()
            with open("LOG.txt", "a+") as f:
                f.write(message + '\n')
        except Exception:
            print("Exception in log: {}".format(str(e)))
            print(traceback.format_exc())


if __name__ == '__main__':
    multiprocessing.freeze_support()
    # sys.stdout = open("global_log.txt", "w")
    appl = QtWidgets.QApplication(sys.argv)
    appl.setStyleSheet("QMainWindow {background: '#c5d2e3';}");
    appl.processEvents()
    form = Application()
    form.show()
    sys.exit(appl.exec_())
