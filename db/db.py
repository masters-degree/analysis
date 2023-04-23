import sqlite3
from faker import Faker
from os import path
from data import newPerformance
from data import subjectsName


def getConnection():
    return sqlite3.connect(path.join(path.dirname(__file__), 'db.sqlite3'))


DB_SUBJECT_TABLE_NAME = 'subject'
DB_STUDENT_TABLE_NAME = 'student'
DB_STUDENT_PERFORMANCE_TABLE_NAME = 'student_performance'
INSERT_CHUNK_LEN = 2000


def createDb(cursor):

    cursor.execute("CREATE TABLE IF NOT EXISTS %s("
                   "id VARCHAR PRIMARY KEY,"
                   "name VARCHAR"
                   ")" % DB_SUBJECT_TABLE_NAME)

    cursor.execute("CREATE TABLE IF NOT EXISTS %s("
                   "id VARCHAR,"
                   "name VARCHAR,"
                   "'group' INT,"
                   "gender VARCHAR,"
                   "PRIMARY KEY (id)"
                   ")" % DB_STUDENT_TABLE_NAME)

    cursor.execute("CREATE TABLE IF NOT EXISTS %s("
                   "student_id VARCHAR,"
                   "semester_id INT,"
                   "subject_id VARCHAR,"
                   "mark INT,"
                   "FOREIGN KEY (student_id) REFERENCES %s (id)"
                   "FOREIGN KEY (subject_id) REFERENCES %s (id)"
                   ")" % (DB_STUDENT_PERFORMANCE_TABLE_NAME, DB_STUDENT_TABLE_NAME, DB_SUBJECT_TABLE_NAME))


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

    if not len(cursor.execute("SELECT * FROM %s" % DB_STUDENT_TABLE_NAME).fetchall()) > 0:
        cursor.executemany(
            "INSERT INTO %s VALUES(?, ?, ?, ?)" % DB_STUDENT_TABLE_NAME,
            map(lambda item: (item['id'], item['name'], item['group'], item['gender']),
                uniqueByField(newPerformance, 'id')))

    if not len(cursor.execute("SELECT * FROM %s" % DB_SUBJECT_TABLE_NAME).fetchall()) > 0:
        cursor.executemany(
            "INSERT INTO %s VALUES(?, ?)" % DB_SUBJECT_TABLE_NAME,
            map(lambda item: [item[0] + 1, item[1]], enumerate(subjectsName)))

    if not len(cursor.execute("SELECT * FROM %s" % DB_STUDENT_PERFORMANCE_TABLE_NAME).fetchall()) > 0:
        for student in newPerformance:
            semCounter = 1

            for index, subjectName in enumerate(subjectsName):
                if index % 3 == 0 and index != 0:
                    semCounter += 1

                cursor.execute(
                    "INSERT INTO %s VALUES(?, ?, ?, ?)" % DB_STUDENT_PERFORMANCE_TABLE_NAME,
                    [student['id'], semCounter, index + 1, student[subjectName]]
                )


if __name__ == '__main__':
    with getConnection() as connection:
        cursor = connection.cursor()

        createDb(cursor)
        feelDb(cursor)

        connection.commit()
