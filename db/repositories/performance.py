from db import getConnection, DB_STUDENT_PERFORMANCE_TABLE_NAME, DB_STUDENT_TABLE_NAME


def getSemesterIds(cursor):
    return tuple(item[0] for item in cursor.execute(f'SELECT DISTINCT semester_id FROM {DB_STUDENT_PERFORMANCE_TABLE_NAME}').fetchall())


def getPaperIds(cursor):
    return tuple(item[0] for item in cursor.execute(f'SELECT DISTINCT subject_id FROM {DB_STUDENT_PERFORMANCE_TABLE_NAME}').fetchall())


def getStudentIds(cursor):
    return tuple(item[0] for item in cursor.execute(f'SELECT DISTINCT student_id FROM {DB_STUDENT_PERFORMANCE_TABLE_NAME}').fetchall())


def getAll(cursor):
    return tuple(item[0] for item in cursor.execute(f'SELECT * FROM {DB_STUDENT_PERFORMANCE_TABLE_NAME}').fetchall())


def getStudentsBySubject(cursor, subjectId, departmentId):
    return cursor.execute(f"""SELECT student_id, marks
FROM {DB_STUDENT_PERFORMANCE_TABLE_NAME}
LEFT JOIN {DB_STUDENT_TABLE_NAME} ON {DB_STUDENT_TABLE_NAME}.id = {DB_STUDENT_PERFORMANCE_TABLE_NAME}.student_id
WHERE {DB_STUDENT_TABLE_NAME}.department_id = "{departmentId}" AND {DB_STUDENT_PERFORMANCE_TABLE_NAME}.subject_id = "{subjectId}"
""").fetchall()


def getSubjectsBySemester(cursor, semesterId):
    return tuple(item[0] for item in cursor.execute(f"""SELECT DISTINCT subject_id
FROM {DB_STUDENT_PERFORMANCE_TABLE_NAME}
WHERE semester_id = "{semesterId}"
""").fetchall())


def getSubjectsByDepartament(cursor, departmentId):
    return tuple(item[0] for item in cursor.execute(f"""SELECT DISTINCT subject_id
FROM {DB_STUDENT_PERFORMANCE_TABLE_NAME}
LEFT JOIN {DB_STUDENT_TABLE_NAME} ON {DB_STUDENT_TABLE_NAME}.id = {DB_STUDENT_PERFORMANCE_TABLE_NAME}.student_id
WHERE {DB_STUDENT_TABLE_NAME}.department_id = "{departmentId}"
""").fetchall())


def getSubjectsBySemesterAndDepartament(cursor, semesterId, departmentId):
    return tuple(item[0] for item in cursor.execute(f"""SELECT DISTINCT subject_id
FROM {DB_STUDENT_PERFORMANCE_TABLE_NAME}
LEFT JOIN {DB_STUDENT_TABLE_NAME} ON {DB_STUDENT_TABLE_NAME}.id = {DB_STUDENT_PERFORMANCE_TABLE_NAME}.student_id
WHERE {DB_STUDENT_TABLE_NAME}.department_id = "{departmentId}" AND {DB_STUDENT_PERFORMANCE_TABLE_NAME}.semester_id = "{semesterId}"
""").fetchall())


def getStudentsByDepartament(cursor, departmentId):
    return cursor.execute(f"""SELECT student_id, semester_id, subject_id, marks
FROM {DB_STUDENT_PERFORMANCE_TABLE_NAME}
LEFT JOIN {DB_STUDENT_TABLE_NAME} ON {DB_STUDENT_TABLE_NAME}.id = {DB_STUDENT_PERFORMANCE_TABLE_NAME}.student_id
WHERE {DB_STUDENT_TABLE_NAME}.department_id = "{departmentId}"
""").fetchall()


def getStudentsByDepartamentAndSemester(cursor, departmentId, semesterId):
    return cursor.execute(f"""SELECT student_id, semester_id, subject_id, marks
FROM {DB_STUDENT_PERFORMANCE_TABLE_NAME}
LEFT JOIN {DB_STUDENT_TABLE_NAME} ON {DB_STUDENT_TABLE_NAME}.id = {DB_STUDENT_PERFORMANCE_TABLE_NAME}.student_id
WHERE {DB_STUDENT_TABLE_NAME}.department_id = "{departmentId}" AND {DB_STUDENT_PERFORMANCE_TABLE_NAME}.semester_id = "{semesterId}"
""").fetchall()


def getStudentsByDepartment(cursor, departmentId):
    return cursor.execute(f"""SELECT DISTINCT student_id, marks, semester_id, subject_id
FROM {DB_STUDENT_PERFORMANCE_TABLE_NAME}
LEFT JOIN {DB_STUDENT_TABLE_NAME} ON {DB_STUDENT_TABLE_NAME}.id = {DB_STUDENT_PERFORMANCE_TABLE_NAME}.student_id
WHERE {DB_STUDENT_TABLE_NAME}.department_id = "{departmentId}"
""").fetchall()


def getStudentMarks(cursor, studentId):
    return cursor.execute(f"""SELECT DISTINCT marks, semester_id, subject_id
FROM {DB_STUDENT_PERFORMANCE_TABLE_NAME}
WHERE {DB_STUDENT_PERFORMANCE_TABLE_NAME}.student_id = "{studentId}"
""").fetchall()


def getStudentMarkBySubjectAndSemester(cursor, studentId, subjectId):
    return tuple(item[0] for item in cursor.execute(f"""SELECT marks
FROM {DB_STUDENT_PERFORMANCE_TABLE_NAME}
    WHERE {DB_STUDENT_PERFORMANCE_TABLE_NAME}.student_id = "{studentId}"
    AND {DB_STUDENT_PERFORMANCE_TABLE_NAME}.subject_id = "{subjectId}"
""").fetchall())

def getStudentMarksBySemester(cursor, semesterId):
    return tuple(item[0] for item in cursor.execute(f"""SELECT marks
FROM {DB_STUDENT_PERFORMANCE_TABLE_NAME}
WHERE {DB_STUDENT_PERFORMANCE_TABLE_NAME}.semester_id = "{semesterId}"
""").fetchall())

def getSubjectsInSemesterByDepartment(cursor, semesterId, departmentId):
    return cursor.execute(f"""SELECT DISTINCT subject_Id
FROM {DB_STUDENT_PERFORMANCE_TABLE_NAME}
LEFT JOIN {DB_STUDENT_TABLE_NAME} ON {DB_STUDENT_TABLE_NAME}.id = {DB_STUDENT_PERFORMANCE_TABLE_NAME}.student_id
WHERE {DB_STUDENT_TABLE_NAME}.department_id = "{departmentId}" AND {DB_STUDENT_PERFORMANCE_TABLE_NAME}.semester_id = "{semesterId}"
""").fetchall()


def getStudentsWithDepartments(cursor):
    return cursor.execute(f"""SELECT student_id, department_id, marks
FROM {DB_STUDENT_PERFORMANCE_TABLE_NAME}
LEFT JOIN {DB_STUDENT_TABLE_NAME} ON {DB_STUDENT_TABLE_NAME}.id = {DB_STUDENT_PERFORMANCE_TABLE_NAME}.student_id
""").fetchall()


if __name__ == '__main__':
    with getConnection() as connection:
        cursor = connection.cursor()
        print(getStudentsWithDepartments(cursor))

