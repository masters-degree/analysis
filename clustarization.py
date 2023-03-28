# https://proglib.io/p/unsupervised-ml-with-python - Иерархическая кластеризация
# https://digitrain.ru/articles/13812/
# https://proglib.io/p/unsupervised-ml-with-python - DBSCAN кластаризация
import copy

import numpy as np
import scipy.cluster.hierarchy as spc
from sklearn.datasets import load_iris, load_wine
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

from db.repositories import performance
from db import getConnection
import pandas as pd


# плотностной алгоритм пространственной кластеризации с присутствием шума
if __name__ == '__main__':

    """
    кластиризация - самих студентов по оценкам (предметам)
    кластиризация - разделение предвам погруппам (связь предметов по оценкам студентов)
    кластиризация - институтов по оценкам студентов
    
    из методов на основе кластаризации
    
    двухмерная кластаризация
    кластаризация по первым 2м оценкам
    """

    with getConnection() as connection:
        cursor = connection.cursor()
        tempStudentId = {}
        tempSubjectId = {}
        subjectIdCounter = 1
        studentIdCounter = 1
        studentMarksBySubject = {}

        for student in performance.getStudentsWithDepartments(cursor):
            studentId = student[0]
            subjectId = student[1]

            if not tempStudentId.get(studentId):
                studentIdCounter = studentIdCounter + 1
                tempStudentId.setdefault(studentId, studentIdCounter)

            studentId = tempStudentId[studentId]

            if not tempSubjectId.get(subjectId):
                subjectIdCounter = subjectIdCounter + 1
                tempSubjectId.setdefault(subjectId, subjectIdCounter)

            subjectId = tempSubjectId[subjectId]

            if studentMarksBySubject.get(subjectId):
                studentMarksBySubject[subjectId] = studentMarksBySubject[subjectId] + [float(student[2])]
            else:
                studentMarksBySubject.setdefault(subjectId, [float(student[2])])

        dump = copy.deepcopy(studentMarksBySubject)

        iris = load_iris()

        maxMarksCountInSubjects = max(list(map(len, studentMarksBySubject.values())))


        def toEqualLen(marks):
            res = marks

            if len(marks) != maxMarksCountInSubjects:
                res = marks + [0 for _ in range(0, maxMarksCountInSubjects - len(marks))]

            return res

        studentMarksBySubject = list(map(toEqualLen, studentMarksBySubject.values()))

        df = pd.DataFrame(studentMarksBySubject)
        df = df[df > 0].dropna(axis=1).transpose() # удаление студентов, у которых нет оценок хотя бы по одному предмету

        model = TSNE(learning_rate=100)

        # Обучаем модель
        transformed = model.fit_transform(df)

        # Представляем результат в двумерных координатах
        x_axis = transformed[:, 0]
        y_axis = transformed[:, 1]

        plt.scatter(x_axis, y_axis)
        plt.show()

