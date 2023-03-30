import sqlite3
from faker import Faker
from os import path
from data import studentPerformanceV2
import math


def getConnection():
    return sqlite3.connect(path.join(path.dirname(__file__), 'db.sqlite3'))


DB_SUBJECT_TABLE_NAME = 'subject'
DB_STUDENT_TABLE_NAME = 'student'
DB_STUDENT_PERFORMANCE_TABLE_NAME = 'student_performance'
INSERT_CHUNK_LEN = 2000


def createDb(cursor):
    cursor.execute("CREATE TABLE IF NOT EXISTS %s("
                   "id VARCHAR,"
                   "name VARCHAR,"
                   "PRIMARY KEY (id)"
                   ")" % DB_SUBJECT_TABLE_NAME)

    cursor.execute("CREATE TABLE IF NOT EXISTS %s("
                   "id VARCHAR,"
                   "name VARCHAR,"
                   "PRIMARY KEY (id)"
                   ")" % DB_STUDENT_TABLE_NAME)

    cursor.execute("CREATE TABLE IF NOT EXISTS %s("
                   "student_id VARCHAR,"
                   "subject_id VARCHAR,"
                   "mark INT,"
                   "FOREIGN KEY (subject_id) REFERENCES %s (id)"
                   ")" % (DB_STUDENT_PERFORMANCE_TABLE_NAME, DB_SUBJECT_TABLE_NAME))


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
            "INSERT INTO %s VALUES(?, ?)" % DB_STUDENT_TABLE_NAME,
            map(lambda item: (item[''], fake.name()),
                uniqueByField(studentPerformanceV2, ''))
        )

    if not len(cursor.execute("SELECT * FROM %s" % DB_SUBJECT_TABLE_NAME).fetchall()) > 0:
        cursor.executemany(
            "INSERT INTO %s VALUES(?, ?)" % DB_SUBJECT_TABLE_NAME,
            map(lambda item: (f"{item} score", item), ['math', 'reading', 'writing'])
        )

    for subjectId in cursor.execute("SELECT name FROM %s" % DB_SUBJECT_TABLE_NAME).fetchall():
        for chunkIndex in range(math.ceil(len(studentPerformanceV2) / INSERT_CHUNK_LEN)):
            chunkStartIndex = chunkIndex * INSERT_CHUNK_LEN
            chunkEndIndex = chunkStartIndex + INSERT_CHUNK_LEN

            cursor.executemany(
                "INSERT INTO %s VALUES(?, ?, ?)" % DB_STUDENT_PERFORMANCE_TABLE_NAME,
                map(lambda item: (
                    item[''], subjectId[0], item[f"{subjectId[0]} score"]),
                    studentPerformanceV2[chunkStartIndex: chunkEndIndex])
            )


if __name__ == '__main__':
    with getConnection() as connection:
        cursor = connection.cursor()

        createDb(cursor)
        feelDb(cursor)

        connection.commit()
