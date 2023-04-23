# https://statrpy2020.blogspot.com/2022/05/python.html

from db.repositories import performance
import scipy.cluster.hierarchy as spc
from db import getConnection
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
import seaborn as sns
from scipy import stats
import pandas as pd


def transformToMatrix(data, rowLabelIndex, colLabelIndex, markLabelIndex):
    matrix = {}

    # распределение студентов с их оценками по редметам
    for dataItem in data:
        col = dataItem[colLabelIndex]
        mark = dataItem[markLabelIndex]
        row = dataItem[rowLabelIndex]
        rowData = matrix.get(row)

        if rowData:
            marks = rowData.get(col)
            if marks:
                rowData[col] = marks + [mark]
            else:
                rowData.setdefault(col, [mark])
        else:
            matrix = {**matrix, row: {col: [mark]}}

    # избавление от дублей оценок
    for colLabel, colData in matrix.items():
        for rowLabel, marks in colData.items():
            if len(marks) > 1:
                print(f'Студент {colLabel} имеет дубль оценки для предмета {rowLabel}')
                colData[rowLabel] = np.mean(marks)
            else:
                colData[rowLabel] = marks[0]

        matrix[colLabel] = colData

    resMatrix = {}

    # избавление от идишников студентов
    for colLabel, colData in matrix.items():
        for rowLabel, mark in colData.items():
            marks = resMatrix.get(rowLabel)

            if marks:
                marks.append(mark)
            else:
                resMatrix.setdefault(rowLabel, [mark])

    return resMatrix


def matrixToEqualColsLen(matrix):
    maxMarksCountInSubjects = max(list(map(len, matrix.values())))

    def toEqualLen(marks):
        res = marks

        if len(marks) != maxMarksCountInSubjects:
            res = marks + [0 for _ in range(0, maxMarksCountInSubjects - len(marks))]

        return res

    marksBySubject = list(map(toEqualLen, matrix.values()))

    df = pd.DataFrame(marksBySubject)
    df = df[df > 0].dropna(axis=1)  # удаление студентов, у которых нет оценок хотя бы по одному предмету

    return df.transpose()


def getCorrelation(df):
    fig, (ax1, ax2, ax3) = plt.subplots(3)

    #print(df)

    """
    сделать градацию всета Красный - Белый - Синий
    """
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

    dbscan = DBSCAN()

    pdist = spc.distance.pdist(correlationMatrix)
    linkage = spc.linkage(pdist, method='complete')
    idx = spc.fcluster(linkage, 0.5 * pdist.max(), 'distance')

    spc.dendrogram(linkage,
                   labels=list(range(1, df.shape[1] + 1)),
                   leaf_rotation=90,
                   leaf_font_size=6,
                   ax=ax3
                   )

    return linkage[:, 2]


if __name__ == '__main__':
    with getConnection() as connection:
        cursor = connection.cursor()
        data = performance.getStudentsMarks(cursor)

        getCorrelation(matrixToEqualColsLen(transformToMatrix(data, 0, 3, 1)))

        plt.show()
