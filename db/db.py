import sqlite3
from faker import Faker
from os import path
from data import studentPerformance, studentCouncelingInformation, employeeInformation, departmentInformation
import math


def getConnection():
    return sqlite3.connect(path.join(path.dirname(__file__), 'db.sqlite3'))


DB_DEPARTMENT_TABLE_NAME = 'department'
DB_EMPLOYEE_TABLE_NAME = 'employee'
DB_STUDENT_TABLE_NAME = 'student'
DB_STUDENT_PERFORMANCE_TABLE_NAME = 'student_performance'
INSERT_CHUNK_LEN = 2000


def createDb(cursor):
    cursor.execute("CREATE TABLE IF NOT EXISTS %s("
                   "id VARCHAR PRIMARY KEY,"
                   "name VARCHAR,"
                   "date DATETIME"
                   ")" % DB_DEPARTMENT_TABLE_NAME)

    cursor.execute("CREATE TABLE IF NOT EXISTS %s("
                   "id VARCHAR PRIMARY KEY,"
                   "department_id VARCHAR,"
                   "name VARCHAR,"
                   "FOREIGN KEY (department_id) REFERENCES %s (id)"
                   ")" % (DB_EMPLOYEE_TABLE_NAME, DB_DEPARTMENT_TABLE_NAME))

    cursor.execute("CREATE TABLE IF NOT EXISTS %s("
                   "id VARCHAR,"
                   "department_id VARCHAR,"
                   "name VARCHAR,"
                   "FOREIGN KEY (department_id) REFERENCES %s (id),"
                   "PRIMARY KEY (id, department_id)"
                   ")" % (DB_STUDENT_TABLE_NAME, DB_DEPARTMENT_TABLE_NAME))

    cursor.execute("CREATE TABLE IF NOT EXISTS %s("
                   "student_id VARCHAR,"
                   "semester_id INT,"
                   "subject_id VARCHAR,"
                   "marks INT,"
                   "FOREIGN KEY (student_id) REFERENCES %s (id)"
                   ")" % (DB_STUDENT_PERFORMANCE_TABLE_NAME, DB_STUDENT_TABLE_NAME))


def uniqueByField(collection, field):
    temp = []
    filteredData = []

    for item in collection:
        fieldValue = item[field]

        if fieldValue not in temp:
            filteredData.append(item)
            temp.append(fieldValue)

    return filteredData


def feelDb(cursor):
    fake = Faker()

    if not (len(cursor.execute("SELECT * FROM %s" % DB_DEPARTMENT_TABLE_NAME).fetchall()) > 0):
        cursor.executemany(
            "INSERT INTO %s VALUES(?, ?, ?)" % DB_DEPARTMENT_TABLE_NAME,
            map(lambda item: (item['Department_ID'], item['Department_Name'], item['DOE']),
                uniqueByField(departmentInformation, 'Department_ID'))
        )

    if not len(cursor.execute("SELECT * FROM %s" % DB_EMPLOYEE_TABLE_NAME).fetchall()) > 0:
        cursor.executemany(
            "INSERT INTO %s VALUES(?, ?, ?)" % DB_EMPLOYEE_TABLE_NAME,
            map(lambda item: (item['Employee ID'], item['Department_ID'], fake.name()),
                uniqueByField(employeeInformation, 'Employee ID'))
        )

    if not len(cursor.execute("SELECT * FROM %s" % DB_STUDENT_TABLE_NAME).fetchall()) > 0:
        cursor.executemany(
            "INSERT INTO %s VALUES(?, ?, ?)" % DB_STUDENT_TABLE_NAME,
            map(lambda item: (item['Student_ID'], item['Department_Choices'], fake.name()),
                uniqueByField(studentCouncelingInformation, 'Student_ID'))
        )

    if not len(cursor.execute("SELECT * FROM %s" % DB_STUDENT_PERFORMANCE_TABLE_NAME).fetchall()) > 0:
        for chunkIndex in range(math.ceil(len(studentPerformance) / INSERT_CHUNK_LEN)):
            chunkStartIndex = chunkIndex * INSERT_CHUNK_LEN
            chunkEndIndex = chunkStartIndex + INSERT_CHUNK_LEN

            cursor.executemany(
                "INSERT INTO %s VALUES(?, ?, ?, ?)" % DB_STUDENT_PERFORMANCE_TABLE_NAME,
                map(lambda item: (
                    item['Student_ID'], item['Semster_Name'].replace('Sem_', ''), item['Paper_ID'], item['Marks']),
                    studentPerformance[chunkStartIndex: chunkEndIndex])
            )


if __name__ == '__main__':
    with getConnection() as connection:
        cursor = connection.cursor()

        createDb(cursor)
        feelDb(cursor)

        connection.commit()
