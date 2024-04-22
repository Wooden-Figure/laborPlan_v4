import datetime
import os.path
import sqlite3
import traceback
import pandas as pd


def get_connection():
    """
    connect to the database
    :return:
    """
    try:
        connection = sqlite3.connect('database.db')
        connection.execute('PRAGMA foreign_keys = ON')
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        return connection, cursor
    except Exception as e:
        print("Exception in get_connection: {}".format(str(e)))
        print(traceback.format_exc())


def init_database():
    """
    initialize the DB
    :return:
    """
    try:
        if not os.path.exists('database.db'):
            connection = sqlite3.connect('database.db')
            with open('schema.sql') as f:
                res = connection.executescript(f.read())
    except Exception as e:
        print("Exception in init_database: {}".format(str(e)))
        print(traceback.format_exc())


def remove_employee_by_id(employee_id):
    """
    Remove Employee by ID
    :param employee_id:
    :return:
    """
    try:
        if not employee_id or employee_id is None:
            print("No employee detected to remove")
            return
        conn, cursor = get_connection()
        sql = 'DELETE FROM employee WHERE id={}'.format(employee_id)
        res = cursor.execute(sql)
        conn.commit()
        conn.close()
    except Exception as e:
        print("Exception in remove_employee_by_id: {}".format(str(e)))
        print(traceback.format_exc())


def assign_employee_by_id(employee_id, station, assign):
    """
    assign (or de-assign) the employee to the station
    :param employee_id:
    :param station:
    :param assign:
    :return:
    """
    try:
        print('assign_employee_by_id')
        print(employee_id, station, assign)
        conn, cursor = get_connection()
        result = pd.read_sql_query(
            'SELECT * FROM plan WHERE employee_id="{}" and station="{}"'.format(employee_id, station), conn)
        if len(result) == 0:
            print('Employee is not trained for this station')
            conn.commit()
            conn.close()
            return None
        else:
            sql = ''' UPDATE plan SET assigned = ?, last_worked = ? WHERE employee_id = ? and station = ?'''
            cursor.execute(sql, (assign, datetime.datetime.now().strftime("%d-%m-%Y"), employee_id, station))
        conn.commit()
        conn.close()
    except Exception as e:
        print("Exception in remove_employee_by_id: {}".format(str(e)))
        print(traceback.format_exc())


def get_bulk_df_names(row):
    """
    a small method-helper to get the names by id for the df
    :param row:
    :return:
    """
    return select_employee_name_by_id(row['employee_id'])


def check_status(row):
    """
    checks the status of the employee based on the latest time worked
    :param row:
    :return:
    """
    if (datetime.datetime.now() - datetime.datetime.strptime(row['last_worked'], "%d-%m-%Y")).days > 240:
        return "Not Trained"
    else:
        return "Trained"


def select_all_assigned_by_station(station):
    """
    select the list of the employee assigned to the station, add the name and status
    :param station:
    :return:
    """
    try:
        conn, cursor = get_connection()
        result = pd.read_sql_query('SELECT * FROM plan WHERE station= "{}" and assigned = true'.format(station), conn)

        conn.commit()
        conn.close()
        if len(result) > 0:
            result['name'] = result.apply(get_bulk_df_names, axis=1)
        else:
            result['name'] = ' '

        if len(result) > 0:
            result['status'] = result.apply(check_status, axis=1)
        else:
            result['status'] = ' '

        result = result[["employee_id", "name", "last_worked", "status"]]
        return result
    except Exception as e:
        print("Exception in select_all_assigned_by_station: {}".format(str(e)))
        print(traceback.format_exc())


def select_employee_name_by_id(employee_id):
    """
    get employee name by ID
    :param employee_id:
    :return:
    """
    try:
        conn, cursor = get_connection()
        result = pd.read_sql_query('SELECT * FROM employee WHERE id={}'.format(employee_id), conn)
        conn.commit()
        conn.close()
        return result['name'].values[0]
    except Exception as e:
        print("Exception in select_employee_name_by_id: {}".format(str(e)))
        print(traceback.format_exc())


def select_all_employee():
    """
    select all the employee
    :return:
    """
    try:
        conn, cursor = get_connection()
        sql = """select * from employee"""
        result = pd.read_sql_query(sql, conn)
        conn.commit()
        conn.close()
        return result['name'].values
    except Exception as e:
        print("Exception in select_all_employee: {}".format(str(e)))
        print(traceback.format_exc())


def select_trained_available_employee(station):
    """
    get list of the valid and available employees for some station
    :return:
    """
    try:
        conn, cursor = get_connection()
        sql = """select * from employee"""
        result = pd.read_sql_query('SELECT * FROM plan WHERE station="{}" and assigned=false'.format(station), conn)

        if len(result) > 0:
            result['status'] = result.apply(check_status, axis=1)
        else:
            result['status'] = ' '
        if len(result) > 0:
            result['name'] = result.apply(get_bulk_df_names, axis=1)
        else:
            result['name'] = ' '
        result = result[result['status'] == "Trained"]
        conn.commit()
        conn.close()
        print(result)
        return result['name'].values
    except Exception as e:
        print("Exception in select_all_employee: {}".format(str(e)))
        print(traceback.format_exc())


def select_employee_id_by_name(name):
    """
    select employee ID by Name
    :param name:
    :return:
    """
    try:
        conn, cursor = get_connection()
        result = conn.execute('SELECT * FROM employee where name = "{}"'.format(name.strip())).fetchone()
        conn.commit()
        conn.close()
        return result[0]
    except Exception:
        print("No employee detected with this name: {}".format(name))
        return


def insert_training(employee_id, station, trained_time):
    """
    insert or update last worked time for the employee
    :param employee_id:
    :param station:
    :param trained_time:
    :return:
    """
    try:
        conn, cursor = get_connection()
        result = pd.read_sql_query(
            'SELECT * FROM plan WHERE employee_id="{}" and station="{}"'.format(employee_id, station), conn)
        if len(result) == 0:
            try:
                cursor.execute("INSERT INTO plan (employee_id, station, last_worked, assigned) VALUES (?,?,?,?)",
                               (employee_id, station, trained_time, False))
            except Exception:
                return "Employee with ID {} not found".format(employee_id)
        else:
            sql = ''' UPDATE plan SET last_worked = ? WHERE employee_id = ? and station = ?'''
            cursor.execute(sql, (trained_time, employee_id, station))
        conn.commit()
        conn.close()
        return "Last worked date updated: employee: {}, station: {}, time: {}".format(employee_id, station, trained_time)
    except Exception as e:
        print("Exception in insert_training: {}".format(str(e)))
        print(traceback.format_exc())


def insert_employee(name):
    """
    insert new employee by name (if not exists)
    :param name:
    :return:
    """
    try:
        conn, cursor = get_connection()

        employee_exists = conn.execute('SELECT * FROM employee where name = "{}"'.format(name.strip())).fetchall()
        if employee_exists:
            print("employee with the name {} exists already!".format(name))
            conn.commit()
            conn.close()
            return "employee with the name {} exists already!".format(name)
        cursor.execute("INSERT INTO employee (name) VALUES (?)", (name,))
        conn.commit()
        conn.close()
        return "New employee added!"
    except Exception as e:
        print("Exception in insert_employee: {}".format(str(e)))
        print(traceback.format_exc())


def update_employee_name(employee_id, new_name):
    """
    update the employee name (if not taken already)
    :param employee_id:
    :param new_name:
    :return:
    """
    try:
        conn, cursor = get_connection()
        emp_old = conn.execute('SELECT * FROM employee where name = "{}"'.format(new_name.strip())).fetchall()
        if emp_old:
            print("Employee {} exists already".format(new_name))
            conn.commit()
            conn.close()
            return
        sql = ''' UPDATE employee SET name = ? WHERE id = ?'''
        cursor.execute(sql, (new_name, employee_id))
        conn.commit()
        conn.close()


    except Exception as e:
        print("Exception in update_employee_name: {}".format(str(e)))
        print(traceback.format_exc())


def reset_labor():
    """
    reset a labor (set all the employees to not assigned)
    :return:
    """
    try:
        conn, cursor = get_connection()
        sql = ''' UPDATE plan SET assigned = false'''
        res = cursor.execute(sql, ())
        conn.commit()
        conn.close()
    except Exception as e:
        print("Exception in reset_labor: {}".format(str(e)))
        print(traceback.format_exc())


def save_to_excel(file_name):
    """
    import to Excel
    :param file_name:
    :return:
    """
    try:
        conn, cursor = get_connection()
        header = ["Employee ID", "Name", "Station", "Last Worked", "Status"]
        result = pd.read_sql_query(
            'SELECT * FROM plan', conn)
        if len(result) > 0:
            result['name'] = result.apply(get_bulk_df_names, axis=1)
        else:
            result['name'] = ' '
        if len(result) > 0:
            result['status'] = result.apply(check_status, axis=1)
        else:
            result['status'] = ' '
        result = result[['employee_id', 'name', 'station', 'last_worked', 'status']]
        result.columns = header
        result.to_excel(file_name, index=False)
        conn.commit()
        conn.close()
    except Exception as e:
        print("Exception in save_to_excel: {}".format(str(e)))
        print(traceback.format_exc())


def import_from_excel(file_name):
    """
    import training data from excel
    :param file_name:
    :return:
    """
    try:
        if not os.path.exists(file_name):
            print("file does not exists")
            return
        df = pd.read_excel(file_name)
        if any(x not in df.columns for x in ["Employee ID", "Station", "Last Worked"]):
            print("Excel column names seems to be wrong")
            return
        else:
            for index, row in df.iterrows():
                if str(row['Employee ID']) != '':
                    insert_training(row['Employee ID'], row['Station'], row['Last Worked'])
    except Exception as e:
        print("Exception in import_from_excel: {}".format(str(e)))
        print(traceback.format_exc())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    init_database()
