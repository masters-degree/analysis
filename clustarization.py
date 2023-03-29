# https://proglib.io/p/unsupervised-ml-with-python - Иерархическая кластеризация
# https://digitrain.ru/articles/13812/
# https://proglib.io/p/unsupervised-ml-with-python - DBSCAN кластаризация
# https://edu.vsu.ru/pluginfile.php/1246728/mod_resource/content/1/191.pdf#:~:text=%D0%9F%D1%80%D0%BE%D1%81%D1%82%D1%80%D0%B0%D0%BD%D1%81%D1%82%D0%B2%D0%BE%20%D0%BF%D1%80%D0%B8%D0%B7%D0%BD%D0%B0%D0%BA%D0%BE%D0%B2%20%E2%80%93%20%D1%8D%D1%82%D0%BE%20N%2D%D0%BC%D0%B5%D1%80%D0%BD%D0%BE%D0%B5,%D0%BF%D1%80%D0%B5%D0%B4%D1%81%D1%82%D0%B0%D0%B2%D0%BB%D1%8F%D0%B5%D1%82%20%D1%81%D0%BE%D0%B1%D0%BE%D0%B9%20%D0%B7%D0%BD%D0%B0%D1%87%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%BE%D0%BF%D1%80%D0%B5%D0%B4%D0%B5%D0%BB%D0%B5%D0%BD%D0%BD%D0%BE%D0%B9%20%D1%85%D0%B0%D1%80%D0%B0%D0%BA%D1%82%D0%B5%D1%80%D0%B8%D1%81%D1%82%D0%B8%D0%BA%D0%B8
# https://habr.com/ru/company/otus/blog/680724/

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors
from db.repositories import performance
from db import getConnection

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
        X = []

        marksByStudents = {}

        for (student_id, subject_id, mark) in performance.getStudents(cursor):
            marksBySubject = marksByStudents.get(student_id)

            if marksBySubject:
                marks = marksBySubject.get(subject_id)
                if marks:
                    marksBySubject[subject_id] = marks + [mark]
                else:
                    marksBySubject.setdefault(subject_id, [mark])
            else:
                marksByStudents = {**marksByStudents, student_id: {subject_id: [mark]}}

        marksBySubject = {}
        marks = []

        for studentId, _marksBySubject in marksByStudents.items():
            for subjectId, mark in _marksBySubject.items():
                marks = marksBySubject.get(subjectId)

                if marks:
                    marks.append(mark)
                else:
                    marksBySubject.setdefault(subjectId, [mark])


        for studentId, _marksBySubject in marksByStudents.items():
            for subjectId, mark in _marksBySubject.items():
                marks.append(mark)

        maxMarksCountInSubjects = max(list(map(len, marksBySubject.values())))

        def toEqualLen(marks):
            res = marks

            if len(marks) != maxMarksCountInSubjects:
                res = marks + [0 for _ in range(0, maxMarksCountInSubjects - len(marks))]

            return list(map(lambda item: item[0] if type(item) is list else item, res))

        marksBySubject = list(map(toEqualLen, marksBySubject.values()))
        df = pd.DataFrame(marksBySubject)
        df = df[df > 0].dropna(axis=1).transpose() # удаление студентов, у которых нет оценок хотя бы по одному предмету

        # Определяем модель
        dbscan = DBSCAN(eps=4, min_samples=4)

        # Обучаем
        dbscan.fit(df)


        neigh = NearestNeighbors(n_neighbors=3)
        nbrs = neigh.fit(df)
        distances, indices = nbrs.kneighbors(df)

        # Уменьшаем размерность при помощи метода главных компонент
        pca = PCA(n_components=2).fit(df)
        pca_2d = pca.transform(df)

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

        marksByClusterInSubject = {}

        for index, row in enumerate(df.iterrows()):
            clusterLabel = dbscan.labels_[index]
            rowData = row[1]

            for itemIndex in range(0, rowData.shape[0]):
                clusters = marksByClusterInSubject.get(itemIndex)

                if clusters:
                    if clusters.get(clusterLabel):
                        clusters[clusterLabel] = clusters[clusterLabel] + [rowData[itemIndex]]
                    else:
                        clusters.setdefault(clusterLabel, [rowData[itemIndex]])
                else:
                    marksByClusterInSubject.setdefault(itemIndex, {clusterLabel: [rowData[itemIndex]]})

        # Отобразим график расстояний между точками
        #distances = np.sort(distances, axis=0)
        #distances = distances[:, 1]
        #plt.figure(figsize=(20, 10))
        #plt.plot(distances)
        #plt.title('K-distance Graph', fontsize=20)
        #plt.xlabel('Data Points sorted by distance', fontsize=14)
        #plt.ylabel('Epsilon', fontsize=14)

        fig, axes = plt.subplots(len(marksByClusterInSubject.keys()))

        for index, (subjectId, clusters) in enumerate(marksByClusterInSubject.items()):
            for clusterLabel, marks in clusters.items():
                axes[index].scatter([clusterLabel for _ in range(0, len(marks))], marks)

        plt.show()

