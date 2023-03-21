# https://statrpy2020.blogspot.com/2022/05/python.html

from db.repositories import performance
import scipy.cluster.hierarchy as spc
from db import getConnection
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.decomposition import PCA
import seaborn as sns
from scipy import stats
import pandas as pd


if __name__ == '__main__':
    with getConnection() as connection:
        cursor = connection.cursor()
        data = performance.getStudentsByDepartment(cursor, 'IDEPT8313')
        fig, (ax1, ax2, ax3) = plt.subplots(3)

        """
        посмотреть кластаризацию на основе матрицы корреляции
        """

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

        marksBySubject = list(map(toEqualLen, marksBySubject.values()))

        df = pd.DataFrame(marksBySubject)
        df = df[df > 0].dropna(axis=1) # удаление студентов, у которых нет оценок хотя бы по одному предмету
        print(df)
        df = df.transpose()
        correlationMatrix = df.corr()

        sns.heatmap(correlationMatrix, linewidth=0.5, vmin=-1, vmax=1, ax=ax1)

        for x in range(correlationMatrix.shape[0]):
            correlationMatrix.iloc[x, x] = 0.0

        pc = correlationMatrix.abs().idxmax()
        cormax = correlationMatrix.loc[pc.index, pc.values]
        df_cor = pd.DataFrame({'colname ': pc, 'cor': np.diagonal(cormax)})
        df_cor.sort_values(by=['cor'])
        df_cor = df.corr()
        df_cor = pd.DataFrame(np.tril(df_cor, k=-1), columns=df_cor.columns,
                              index=df_cor.columns)
        df_cor = df_cor.stack()
        df_cor = df_cor[df_cor.abs() > 0]
        df_cor = df_cor.rename("pearson")
        df_cor = df_cor.reset_index()
        df_cor['p'] = df_cor.apply(lambda r:
                                   round(stats.pearsonr(df[r.level_0], df[r.level_1])[1], 4), axis=1)


        new = correlationMatrix.copy(True)

        for i in range(0, df_cor.shape[0]):
            new.loc[int(df_cor.loc[i][0])][int(df_cor.loc[i][1])] = df_cor.loc[i][3]
            new.loc[int(df_cor.loc[i][1])][int(df_cor.loc[i][0])] = df_cor.loc[i][3]

        sns.heatmap(new, linewidth=0.5, vmin=0, vmax=0.05, ax=ax2)

        df_cor = df_cor.query('p<=0.05')

        print(correlationMatrix)
        dbscan = DBSCAN()

        pdist = spc.distance.pdist(correlationMatrix)
        linkage = spc.linkage(pdist, method='complete')
        idx = spc.fcluster(linkage, 0.5 * pdist.max(), 'distance')

        print(linkage)
        spc.dendrogram(linkage,
                       labels=list(range(1, 57)),
                       leaf_rotation=90,
                       leaf_font_size=6,
                       ax=ax3
                       )


        plt.show()

