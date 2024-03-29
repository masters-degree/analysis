from db import getConnection
from repositories import performance

if __name__ == '__main__':
    with getConnection() as connection:
        cursor = connection.cursor()

        print('Всего оценок - %s' % len(performance.getAll(cursor)))
        print('Всего семестров - %s' % len(performance.getSemesterIds(cursor)))
        print('Всего предметов - %s' % len(performance.getPaperIds(cursor)))
        print('Всего студентов - %s' % len(performance.getStudentIds(cursor)))
        print('Предметов в семестре - %s' % len(performance.getSubjectsBySemester(cursor, 1)))
