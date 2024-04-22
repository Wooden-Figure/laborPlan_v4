import random

from data_layer import *

stations = {
  "harvest": 1,
  "AP testing": 2,
  "AP repair": 3,
  "switch testing": 4,
  "switch sanitization": 4,
  "optics testing": 3,
  "optics receiving": 2,
  "AP sort": 3,
  "AP prepceive": 4,
  "DIMM sort": 2,
  "shipping": 4,
  "GPU": 2,
  "switch receiving": 3
}

# a short demo how actually the database works

# initialize the database
init_database()

print("Adding new employees (if not exists)")
# add some new employees (if not exists)

for x in range(100):
    insert_employee("Exployee_{}".format(x))

insert_employee("Alex")
insert_employee("Mary")
insert_employee("Rob")

input()
print("Remove Rob1 if exits")
# remove the employee (if exists)
remove_employee_by_id(select_employee_id_by_name("Rob1"))

print("Insert Training values")

for x in range(100):
    insert_training(select_employee_id_by_name("Exployee_{}".format(random.randint(1, 99))),
                    random.choice(list(stations.keys())), "15-03-2024")


print("Assign employees to stations")
# assign an employee to station (works if the employee is trained only)
assign_employee_by_id(select_employee_id_by_name("Rob"), 'harvest', True)
assign_employee_by_id(select_employee_id_by_name("Mary"), 'GPU', True)
assign_employee_by_id(select_employee_id_by_name("Alex"), 'GPU', True)
input()

print("De-assign Rob from GPU..")

# de-assign Rob
assign_employee_by_id(select_employee_id_by_name("Rob"), 'GPU', False)
input()

print("Just a list of employees")

employees = select_all_employee()
print(employees)

print("Change Rob name to Rob1")
# update employee name
update_employee_name(select_employee_id_by_name("Rob"), "Rob1")
input()

print("Train Rob(1) using his new name")

# insert training and assign using new name
insert_training(select_employee_id_by_name("Rob1"), "shipping", "15-03-2024")
assign_employee_by_id(select_employee_id_by_name("Rob1"), 'shipping', True)

insert_training(select_employee_id_by_name("Mary"), "GPU", '20-03-2020')

# get list of all the employee's assigned to the station
print("get list of all the assigned employees to GPU")
assigned = select_all_assigned_by_station('GPU')
print(assigned)

print("Assign Rob(1) back to GPU...")

# assign back Rob to GPU
assign_employee_by_id(select_employee_id_by_name("Rob1"), 'GPU', True)

print("get list of all the assigned employees to GPU again...")

assigned = select_all_assigned_by_station('GPU')
print(assigned)

# export/import to excel
print("Export/import from/to Excel")

save_to_excel('results.xlsx')
import_from_excel('results.xlsx')

print("Get list of the available employees for GPU")

# get all the employees available for some station (trained but not assigned yet)
available_ids = select_trained_available_employee('GPU')
print(available_ids)


print("De-assign Alex and get list of the available employees for GPU again...")
assign_employee_by_id(select_employee_id_by_name("Alex"), 'GPU', False)

# get all the employees available for some station (trained but not assigned yet)
available_ids = select_trained_available_employee('GPU')
print(available_ids)

print("Reset the labor plan...")
# reset_labor()

print("Get all the available IDs for GPU again...")
available_ids = select_trained_available_employee('GPU')
print(available_ids)
