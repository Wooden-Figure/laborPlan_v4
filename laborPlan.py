import copy
import traceback

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


header = ["id", "Last Name", "First Name", "Last Worked", "Status"]


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

            # updates the stations
            self.update_stations_list()
            self.stations = list(read_json("stations.json").keys())

            # connects the UI features to each part it is assigned to
            self.import_from_excel.clicked.connect(self.import_excel)
            self.export_to_excel.clicked.connect(self.export_excel)
            self.tableView_labor.doubleClicked.connect(self.edit_labor)
            self.save_changes_btn.clicked.connect(self.save_changes_training)
            self.save_changes_btn1.clicked.connect(self.save_changes_name)

            # same as above
            self.new_employee_btn.clicked.connect(self.create_new_employee)
            self.stations_list.itemClicked.connect(self.select_station)
            self.confirm_assignment.clicked.connect(self.assign_employee)
            self.revoke_selected_btn.clicked.connect(self.revoke_employee)
            self.delete_empl.clicked.connect(self.delete_employee)
            self.reset_labor_btn.clicked.connect(self.reset_labor)
            self.random_labor_btn.clicked.connect(self.random_labor)
            self.update_combo_boxes()

            self.new_employee_mode = False
            self.new_mode = False

        except Exception as e:
            print("Exception in init: {}".format(str(e)))
            print(traceback.format_exc())

    def import_excel(self):
        """
        import the trainings from Excel
        :return:
        """
        filepath, filters = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Please select an Excel file', '', 'Excel (*.xlsx)')
        if filepath:
            data_layer.import_from_excel(filepath)
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
        build a random labor based on the stations limits from the JSON file
        :return:
        """
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure you want to reset all the assignments and create random labor?",
                                     QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            assigned = []
            data_layer.reset_labor()
            stations = read_json('stations.json')
            # ensures builders are not double slotted (unless intentional w/ revoke function)
            for station, limit in stations.items():
                available = [x for x in list(data_layer.select_trained_available_employee(station).tolist())
                             if x not in assigned]
                n = limit
                # declaring list
                if n < len(available):
                    selection = random.sample(available, n)
                else:
                    selection = available
                for x in selection:
                    assigned.append(x)

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
        # sorts the builders by alphabetical order
        employees.sort()
        employees.insert(0, 'Select Builder...')

        self.employee_cb.addItems(employees)
        self.station_cb.clear()
        self.stations = list(read_json("stations.json").keys())

        stations = copy.deepcopy(self.stations)
        stations.insert(0, 'Select station...')
        self.station_cb.addItems(stations)

        if self.station_tb.toPlainText():
            self.available_empl_cb.clear()
            available = list(data_layer.select_trained_available_employee(self.station_tb.toPlainText()).tolist())
            available.sort()
            available.insert(0, 'Select valid Builder...')
            self.available_empl_cb.addItems(available)

    def save_changes_name(self):
        """
        save the new or updated employee
        :return:
        """
        if ',' not in self.name_tb.text() or self.name_tb.text().count(',') > 1:
            self.alert("Please enter Last Name and First Name single comma separated.")
            return
        # updates the employee when not in new employee mode
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
            self.alert("Please select a Builder first")

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
        self.name_label.setText("The new Builder\n(Last Name,First Name):")

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
                self.alert("Please select a Builder and station first")
            else:
                res = data_layer.insert_training(data_layer.select_employee_id_by_name(employee), station,
                                                 date.toString('dd-MM-yyyy'))
                self.alert(res)
                self.update_combo_boxes()
        except Exception as e:
            print("Exception occurred: {}".format(e))
            print(traceback.format_exc())

    def select_station(self, schedule):
        """
        select new station on the left
        :param schedule:
        :return:
        """
        self.new_mode = False
        self.new_employee_mode = False
        self.name_tb.clear()
        self.name_label.setText("ID:(), LAST NAME,FIRST NAME")

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
            print('update_labor_db')
            station = station.split(' | ')[0]
            self.new_mode = False
            assigned_empls = data_layer.select_all_assigned_by_station(station)
            self.globals_labor_df = assigned_empls
            print('1')

            self.globals_labor_df['last name'] = ''
            if len(self.globals_labor_df) > 0:
                self.globals_labor_df['name'] = (
                    self.globals_labor_df['name'].apply(lambda x: x + ',' if ',' not in x else x))
                self.globals_labor_df[['last name', 'name']] = self.globals_labor_df['name'].str.split(',', expand=True)

            self.globals_labor_df = self.globals_labor_df[['employee_id', 'last name', 'name', 'last_worked', 'status']]
            print('3')
            # sorts everything by last name
            self.globals_labor_df = self.globals_labor_df.sort_values("last name")

            print('4')
            print(self.globals_labor_df)
            print(header)
            self.globals_labor_df.columns = header
            print('2')
            print(self.globals_labor_df)
            self.model = pandasModel(self.globals_labor_df)
            self.tableView_labor.setModel(self.model)
            self.tableView_labor.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
            self.tableView_labor.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.set_site_policy()
            self.update_combo_boxes()

        except Exception as e:
            print(traceback.format_exc())
            self.log("Exception in update_posts_db: {}".format(str(e)))

    def update_stations_list(self):
        """
        update the list of stations based on the .json file
        :return:
        """
        schedules = read_json("stations.json")
        schedules = {key: value for key, value in sorted(schedules.items())}

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
        returns an ID of the current empl selected
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
        returns a Name of the current empl selected
        :return:
        """
        try:
            df_rows = sorted(set(index.row() for index in
                                 self.tableView_labor.selectedIndexes()))

            if df_rows == []:
                return False
            employee_id = [self.globals_labor_df.iloc[i]
                           ['Last Name'] + ',' + self.globals_labor_df.iloc[i]['First Name'] for i in df_rows][0]
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
        self.name_label.setText("ID:({}), LAST NAME,FIRST NAME:".format(employee_id))
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
        except IOError as io_error:
            print("IOError in log: {}".format(io_error))
            print(traceback.format_exc())
        except Exception as general_error:
            print("Exception in log: {}".format(general_error))
            print(traceback.format_exc())
        """except Exception:
            print("Exception in log: {}".format(str(e)))
            print(traceback.format_exc())
            """


if __name__ == '__main__':
    multiprocessing.freeze_support()
    # sys.stdout = open("global_log.txt", "w")
    appl = QtWidgets.QApplication(sys.argv)
    appl.setStyleSheet("QMainWindow {background: '#c5d2e3';}")
    appl.processEvents()
    form = Application()
    form.show()
    sys.exit(appl.exec_())
