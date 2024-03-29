# http://www.mathprofi.ru/proverka_statisticheskih_gipotez.html
import math


from scipy import stats

from db.repositories import performance
from db import getConnection
import numpy as np


if __name__ == '__main__':
    with getConnection() as connection:

        cursor = connection.cursor()
        data1 = performance.getStudentsByDepartment(cursor, 'IDEPT8313')
        data2 = performance.getStudentsByDepartment(cursor, 'IDEPT3778')
        a = 0.01
        f = (1 - (2 * a)) / 2

        def getMarks(data):
            new = []
            for item in data:
                new.append(item[1])
            return new

        def getInfo(data):
            n = len(data)
            # матожидание
            m = np.mean(data)
            d = np.var(data)

            return n, m, d


        info1 = getInfo(getMarks(data1))
        info2 = getInfo(getMarks(data2))

        _, p = stats.ttest_ind(a=getMarks(data1), b=getMarks(data2), equal_var=True)

        print(p > a)

