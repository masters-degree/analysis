import functools
import random
import csv
from faker import Faker
from os import path


fake = Faker('ru')

subjectType = {
    'Verbal': 'Verbal',
    'Math': 'Math',
    'Inf': 'Inf',
}

genders = {
    'Male': 'Male',
    'Female': 'Female'
}

studentType = {
    'Lag': 'Lag',
    'Norm': 'Norm',
    'Excellent': 'Excellent',
}

studentTypeMarkBounds = {
    studentType['Lag']: list(range(60, 80)),
    studentType['Norm']: list(range(65, 86)),
    studentType['Excellent']: list(range(75, 96)),
    'VeryExcellent': list(range(85, 101)),
    'VeryLag': list(range(50, 60)),
}

subjectsName = [
    'История', "Высшая математика", "Информатика",
    'Русский язык', "Дискретная метематика", "Язык Python",
    'Философия', "Теория вероятности", "ООП",
    'Экономика', "Численные методы", "Теория баз данных",

    'БЖД', "Основы теории алгоритмов", "Операционные системы",
    'Правоведение', "Data mining", "Управление данными",
    'Предотвращение коррупции', "Моделирование систем", "WEB",
    'Английский язык', "Интеллектуальный анализ данных", "Java",
]


class Student:
    def __init__(self, id, group, type, favoriteSubjectType, gender, name):
        self.id = id
        self.group = group
        self.type = type
        self.gender = gender
        self.favoriteSubjectType = favoriteSubjectType
        self.name = name
        group.addStudent(self)

    def getMark(self, subject):
        mark = 0

        if self.type == studentType['Lag']:
            indicator = random.choice(list(range(1, 101)))

            if indicator <= 10:
                mark = random.choice(studentTypeMarkBounds['VeryLag'])
            else:
                mark = random.choice(studentTypeMarkBounds[studentType['Lag']])
        elif self.type == studentType['Norm']:
            if subject.type == self.favoriteSubjectType:
                mark = random.choice(studentTypeMarkBounds['Excellent'])
            else:
                mark = random.choice(studentTypeMarkBounds[studentType['Norm']])
        elif self.type == studentType['Excellent']:
            if subject.type == self.favoriteSubjectType:
                mark = random.choice(studentTypeMarkBounds['VeryExcellent'])
            else:
                mark = random.choice(studentTypeMarkBounds[studentType['Excellent']])

        return mark


class Semester:
    def __init__(self, id, students, subjects):
        self.id = id
        self.students = students
        self.subjects = subjects


    def getMarks(self):
        marks = []

        for student in self.students:
            for subject in self.subjects:
                mark = student.getMark(subject)

                marks.append((student.id, mark, self.id, subject.id))

        return marks

    def getMarksByStudent(self):
        marks = functools.reduce(lambda acc, item: {**acc, item.id: []}, self.students, {})

        for student in self.students:
            for subject in self.subjects:
                mark = student.getMark(subject)

                marks[student.id] = marks[student.id] + [mark]

        return marks


class Subject:
    def __init__(self, id, type, name):
        self.id = id
        self.type = type
        self.name = name

    def __str__(self):
        return f'{self.type}'


class Group:
    def __init__(self, id):
        self.id = id
        self.students = []

    def addStudent(self, student):
        self.students.append(student)


def getStudent(id, group):
    indicator = random.choice(list(range(1, 101)))
    isLag = indicator <= 30
    isNorm = 30 <= indicator <= 70
    isExcellent = 70 <= indicator <= 100

    if isLag:
        currentStudentType = studentType['Lag']
    elif isNorm:
        currentStudentType = studentType['Norm']
    else:
        currentStudentType = studentType['Excellent']

    gender = random.choice(list(genders.values()))

    return Student(
        id,
        group,
        currentStudentType,
        random.choice([subjectType['Inf'], subjectType['Math'], subjectType['Verbal']]),
        gender,
        fake.unique.name_female() if gender == genders['Female'] else fake.unique.name_male()
    )


def getSubject(id, type, name):
    return Subject(id, type, name)


def getGroup(id):
    return Group(id)


def getSemester(id, students, subjects):
    return Semester(id, students, subjects)


def getStudents(groups):
    students = []

    currentGroup = 0
    for index in range(1, 154):
        group = groups[currentGroup]

        students.append(getStudent(index, group))

        if len(groups[currentGroup].students) >= 51:
            currentGroup += 1

    return students


def getSemesters(subjects, students):
    semesters = []

    for index in range(0, 8):
        semesters.append(getSemester(index + 1, students, subjects[index * 3: (index * 3) + 3]))

    return semesters


def getSubjects():
    subjects = []
    subjectTypeCounter = 1

    for index in range(1, 25):
        if subjectTypeCounter == 4:
            subjectTypeCounter = 1

        if subjectTypeCounter == 1:
            currentSubjectType = subjectType['Verbal']
        elif subjectTypeCounter == 2:
            currentSubjectType = subjectType['Math']
        else:
            currentSubjectType = subjectType['Inf']

        subjectTypeCounter += 1

        subjects.append(getSubject(index, currentSubjectType, subjectsName[index - 1]))

    return list(subjects)


def getMarkInfo(markInfo):
    studentId, mark, semesterId, subjectId = markInfo
    return studentId, mark, semesterId, subjectId


def marksFactory():
    subjects = getSubjects()
    groups = list(map(getGroup, range(1, 4)))
    students = getStudents(groups)
    semesters = getSemesters(subjects, students)
    studentsData = functools.reduce(lambda acc, item: {**acc, item.id: []}, students, {})
    semestersData = list(map(lambda semester: semester.getMarksByStudent(), semesters))
    resStudentsData = []

    for student in students:
        for index, semester in enumerate(semesters):
            print(semestersData[index][student.id])
            studentsData[student.id] = studentsData[student.id] + semestersData[index][student.id]

    for index, studentData in enumerate(studentsData.values()):
        resStudentsData.append([students[index].id, students[index].name, students[index].gender, students[index].group.id] + studentData)

    return resStudentsData


if __name__ == '__main__':
    newDatav2 = marksFactory()
    labels = ['id', 'name', 'gender', 'group'] + subjectsName

    with open(path.join(path.dirname(__file__), 'new-performance.csv'), 'w', newline='') as newCsvfile:
        writer = csv.DictWriter(newCsvfile, fieldnames=labels)
        writer.writeheader()

        for student in newDatav2:

            print(dict.fromkeys(labels, student))
            data = dict.fromkeys(labels, [])

            for index, key in enumerate(data.keys()):
                data[key] = student[index]

            writer.writerow(data)