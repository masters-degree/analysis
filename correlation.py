# https://statrpy2020.blogspot.com/2022/05/python.html

from db.repositories import performance
import scipy.cluster.hierarchy as spc
from db import getConnection
from data import subjectsName
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
import seaborn as sns
from scipy import stats
from scipy.stats import t
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
    """
    сделать градацию всета Красный - Белый - Синий
    """
    correlationMatrix = df.corr()

    sns.heatmap(correlationMatrix, linewidth=0.5, vmin=-1, vmax=1, cmap="Spectral", xticklabels=subjectsName, yticklabels=subjectsName)

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

    plt.figure()

    sns.heatmap(new, linewidth=0.5, vmin=0, vmax=0.05, cmap="Spectral", xticklabels=subjectsName, yticklabels=subjectsName)

    df_cor = df_cor.query('p<=0.05')

    dbscan = DBSCAN()

    pdist = spc.distance.pdist(correlationMatrix)
    linkage = spc.linkage(pdist, method='complete')
    idx = spc.fcluster(linkage, 0.5 * pdist.max(), 'distance')

    return linkage[:, 2]


if __name__ == '__main__':
    with getConnection() as connection:
        cursor = connection.cursor()
        data = performance.getStudentMarksByGroup(cursor, 1)
        df = matrixToEqualColsLen(transformToMatrix(data, 0, 2, 3))

        firstSub = np.array(list(map(lambda item: list(item.values())[0], list(df[[0]].transpose().to_dict().values()))))
        secondSub = np.array(list(map(lambda item: list(item.values())[0], list(df[[1]].transpose().to_dict().values()))))
        thirdSub = np.array(list(map(lambda item: list(item.values())[0], list(df[[3]].transpose().to_dict().values()))))

        def prepareToPrint(arr):
            return ', '.join(list(map(str, arr)))

        print(df)
        print(prepareToPrint(firstSub))
        print(prepareToPrint(secondSub))
        print(prepareToPrint(thirdSub))

        x, y = firstSub, thirdSub

        xy = x * y

        xMean = np.mean(x)
        yMean = np.mean(y)
        xyMean = np.mean(xy)
        xMeanYMean = xMean * yMean

        print(prepareToPrint(xy))
        print(f'x mean = {xMean}')
        print(f'y mean = {yMean}')
        print(f'XmeanYmean = {xMeanYMean}')
        print(f'xyMean = {xyMean}')

        xQ = np.std(x)
        yQ = np.std(y)
        r = (xyMean - xMeanYMean) / (xQ * yQ)

        print(f'xq = {xQ}')
        print(f'xq = {yQ}')

        print(f'rXY = {r}')

        alpha = 0.05

        print(np.power(r, 2))

        tCrit = t.ppf(1 - (alpha / 2), len(x) - 2)

        t = r * np.sqrt((len(x) - 2) / (1 - np.power(r, 2)))

        getCorrelation(df)

        print(tCrit, t)

        plt.show()

