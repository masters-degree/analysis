# https://proglib.io/p/unsupervised-ml-with-python - Иерархическая кластеризация
# https://digitrain.ru/articles/13812/

# Иерархическая кластеризация

import pandas as pd
from sklearn.mixture import GaussianMixture
import matplotlib.pyplot as plt
from db.repositories import performance
from db import getConnection


with getConnection() as connection:
    cursor = connection.cursor()
    tempStudentId = {}
    tempSubjectId = {}
    subjectIdCounter = 1
    studentIdCounter = 1
    X = []

    for student in performance.getStudentsByDepartamentAndSemester(cursor, 'IDEPT1825', 1):
        studentId = student[0]
        subjectId = student[2]

        if not tempStudentId.get(studentId):
            studentIdCounter = studentIdCounter + 1
            tempStudentId.setdefault(studentId, studentIdCounter)

        studentId = tempStudentId[studentId]

        if not tempSubjectId.get(subjectId):
            subjectIdCounter = subjectIdCounter + 1
            tempSubjectId.setdefault(subjectId, subjectIdCounter)

        subjectId = tempSubjectId[subjectId]

        X.append([studentId, student[3], subjectId])

    n_clusters = 3
    gmm_model = GaussianMixture(n_components=n_clusters)
    gmm_model.fit(X)

    cluster_labels = gmm_model.predict(X)
    X = pd.DataFrame(X)
    X["cluster"] = cluster_labels

    for k in range(0, n_clusters):
        data = X[X["cluster"] == k]
        print(data)
        plt.scatter(data[1], data[0])

if __name__ == '__main__':
    plt.show()
