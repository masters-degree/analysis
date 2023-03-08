from data import studentMarksMatrix
import matplotlib.pyplot as plt
import numpy as np



def prepareData(matrix):
    preparedMatrix = matrix.copy()

    preparedMatrix[preparedMatrix < 75] = 0
    preparedMatrix[(preparedMatrix >= 75) & (preparedMatrix != 0)] = 1

    return preparedMatrix


def calcultaStistic(matrix):
    preparedMatrix = matrix.copy()

    preparedMatrix[preparedMatrix < 75] = 0
    preparedMatrix[(preparedMatrix >= 75) & (preparedMatrix != 0)] = 1

    return preparedMatrix


if __name__ == '__main__':
    matrix = prepareData(studentMarksMatrix)
    zeroMarkInSemesterTotalCount = 0 # Количество студентов с 0 в всех семестрах
    zeroMarkInSemesterCount = [] # Количество студентов с 0 в по каждому семестру
    d = []
    plusMarkInSemesterTotalCount = 0 # Количество студентов с 1 в всех семестрах
    plusMarkInSemesterCount = [] # Количество студентов с 1 в по каждому семестру
    c = []
    D = []
    standardDeviation = []

    for row in matrix.transpose():
        zeroMarkInSemesterTotalCount = zeroMarkInSemesterTotalCount + 1 if row[row == 0].shape[1] == row.shape[1] else zeroMarkInSemesterTotalCount

    for studentIndex in range(0, matrix.shape[0]):
        count = 0

        for row in matrix.transpose():
            count = count + 1 if row[0, studentIndex] == 0 else count

        zeroMarkInSemesterCount.append(count)

    for count in zeroMarkInSemesterCount:
        d.append(zeroMarkInSemesterTotalCount / count)


    for row in matrix.transpose():
        plusMarkInSemesterTotalCount = plusMarkInSemesterTotalCount + 1 if row[row == 1].shape[1] == row.shape[1] else plusMarkInSemesterTotalCount

    for studentIndex in range(0, matrix.shape[0]):
        count = 0

        for row in matrix.transpose():
            count = count + 1 if row[0, studentIndex] == 1 else count

        plusMarkInSemesterCount.append(count)

    for count in plusMarkInSemesterCount:
        c.append(plusMarkInSemesterTotalCount / count)

    for negativeMark, positiveMark in zip(d, c):
        D.append(negativeMark * positiveMark)
        standardDeviation.append(np.sqrt(negativeMark * positiveMark))


    print(standardDeviation)