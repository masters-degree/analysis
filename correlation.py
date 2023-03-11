import functools

from db.repositories import performance
from db import getConnection
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


if __name__ == '__main__':
    with getConnection() as connection:
        cursor = connection.cursor()
        data = performance.getStudentsByDepartment(cursor, 'IDEPT8313')

        # оценки предмета по семестрам

        marksByStudents = {}

        for (student_id, mark, semester_id, subject_id) in data:
            marksBySubject = marksByStudents.get(student_id)

            if marksBySubject:
                marks = marksBySubject.get(subject_id)
                if marks:
                    marksBySubject[subject_id] = marks + [mark]
                else:
                    marksBySubject.setdefault(subject_id, [mark])
            else:
                marksByStudents = {**marksByStudents, student_id: {subject_id: [mark]}}

        for studentId, marksBySubject in marksByStudents.items():
            for subjectId, marks in marksBySubject.items():
                if len(marks) > 1:
                    print(f'Студент {studentId} имеет дубль оценки для предмета {subjectId}')
                    marksBySubject[subjectId] = np.mean(marks)
                else:
                    marksBySubject[subjectId] = marks[0]

            marksByStudents[studentId] = marksBySubject

        marksBySubject = {}

        for studentId, _marksBySubject in marksByStudents.items():
            for subjectId, mark in _marksBySubject.items():
                marks = marksBySubject.get(subjectId)

                if marks:
                    marks.append(mark)
                else:
                    marksBySubject.setdefault(subjectId, [mark])


        maxMarksCountInSubjects = max(list(map(len, marksBySubject.values())))

        def toEqualLen(marks):
            res = marks

            if len(marks) != maxMarksCountInSubjects:
                res = marks + [0 for _ in range(0, maxMarksCountInSubjects - len(marks))]

            return res

        print(marksBySubject)
        marksBySubject = list(map(toEqualLen, marksBySubject.values()))

        matrixToCorrelation = np.array(marksBySubject)
        correlationMatrix = np.corrcoef(matrixToCorrelation)
        print(matrixToCorrelation)
        print(correlationMatrix)

        sns.heatmap(correlationMatrix, linewidth=0.5, cmap='Dark2', vmin=-1, vmax=1)

        plt.show()
