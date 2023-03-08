import csv
from os import path

departmentInformation = []
studentCouncelingInformation = []
employeeInformation = []
studentPerformance = []


with open(path.join(path.dirname(__file__), 'Department_Information.csv'), 'r') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        departmentInformation.append(row)


with open(path.join(path.dirname(__file__), 'Student_Counceling_Information.csv'), 'r') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        studentCouncelingInformation.append(row)


with open(path.join(path.dirname(__file__), 'Employee_Information.csv'), 'r') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        employeeInformation.append(row)


with open(path.join(path.dirname(__file__), 'Student_Performance_Data.csv'), 'r') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        studentPerformance.append(row)

if __name__ == '__main__':
    print(departmentInformation)
    print(studentCouncelingInformation)
    print(employeeInformation)
    print(studentPerformance)