# https://proglib.io/p/unsupervised-ml-with-python - Иерархическая кластеризация
# https://digitrain.ru/articles/13812/
# https://proglib.io/p/unsupervised-ml-with-python - DBSCAN кластаризация

import numpy as np
from sklearn.datasets import load_iris
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.decomposition import PCA
from db.repositories import performance
from db import getConnection


# плотностной алгоритм пространственной кластеризации с присутствием шума
if __name__ == '__main__':

    """
    кластиризация - самих студентов по оценкам (предметам)
    кластиризация - разделение предвам погруппам (связь предметов по оценкам студентов)
    кластиризация - институтов по оценкам студентов
    
    из методов на основе кластаризации
    
    дискременантый анализ (кластаризация)
    
    
    двухмерная кластаризация
    кластаризация по первым 2м оценкам
    """

    with getConnection() as connection:
        cursor = connection.cursor()
        tempStudentId = {}
        tempSubjectId = {}
        subjectIdCounter = 1
        studentIdCounter = 1
        X = []

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

            X.append([studentId, subjectId])

        iris = load_iris()

        X = np.array(X)
        # Определяем модель
        dbscan = DBSCAN()

        # Обучаем
        dbscan.fit(X)

        # Уменьшаем размерность при помощи метода главных компонент
        pca = PCA(n_components=2).fit(X)
        pca_2d = pca.transform(X)

        print(set(dbscan.labels_), len(dbscan.labels_), pca_2d.shape[0])

        print(range(0, pca_2d.shape[0]))

        clusters = {}

        for i in range(0, pca_2d.shape[0]):
            clusterLabel = dbscan.labels_[i]
            clusterCoordinates = clusters.get(clusterLabel)

            if clusterCoordinates:
                clusterCoordinates[0] = clusterCoordinates[0] + [pca_2d[i, 0]]
                clusterCoordinates[1] = clusterCoordinates[1] + [pca_2d[i, 1]]
            else:
                clusterCoordinates = [[pca_2d[i, 0]], [pca_2d[i, 1]]]

            clusters.setdefault(clusterLabel, clusterCoordinates)

        for clusterLabel, clusterCoordinates in clusters.items():
            if clusterLabel == -1:
                plt.scatter(clusterCoordinates[0], clusterCoordinates[1], c='b', marker='*')
            else:
                plt.scatter(clusterCoordinates[0], clusterCoordinates[1])

        plt.show()
