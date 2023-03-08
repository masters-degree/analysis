from db import getConnection, DB_DEPARTMENT_TABLE_NAME, DB_STUDENT_TABLE_NAME


def getDepartmentIds(cursor):
    return tuple(item[0] for item in cursor.execute(f'SELECT DISTINCT id FROM {DB_DEPARTMENT_TABLE_NAME}').fetchall())


if __name__ == '__main__':
    with getConnection() as connection:
        cursor = connection.cursor()
        print(len(getDepartmentIds(cursor)))