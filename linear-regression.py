# https://tonais.ru/library/lineynaya-regressiya-s-pomoschyu-scikit-learn-v-python
# https://habr.com/ru/post/558084/
# https://e.vyatsu.ru/pluginfile.php/462626/mod_resource/content/2/%D0%A2%D0%B5%D0%BE%D1%80%D0%B5%D1%82%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B9%20%D0%BC%D0%B0%D1%82%D0%B5%D1%80%D0%B8%D0%B0%D0%BB_%D1%80%D0%B5%D0%B3%D1%80%D0%B5%D1%81%D1%81%D0%B8%D0%BE%D0%BD%D0%BD%D1%8B%D0%B9%20%D0%BF%D0%B0%D1%80%D0%BD.%D0%B0%D0%BD%D0%B0%D0%BB%D0%B8%D0%B7.pdf
# rss - https://translated.turbopages.org/proxy_u/en-ru.ru.351946bd-6431df47-8f436ac9-74722d776562/https/www.easycalculation.com/statistics/learn-residual-sum-squares.php
import functools
import re

from scipy.stats import f
from scipy.stats import t
import numpy as np
from db import getConnection
from db.repositories import performance
import matplotlib.pyplot as plt

def getRegression(_x, _y, predictedX, alpha=0.05):
    x = np.array(_x)
    y = np.array(_y)

    xMean = np.mean(x)
    yMean = np.mean(y)
    x2 = np.power(x, 2)
    x2Mean = np.mean(x2)
    y2 = np.power(y, 2)
    xyMean = np.mean(x * y)

    b = (xyMean - (xMean * yMean)) / (x2Mean - np.power(xMean, 2))  # точка пересечения с осью Y
    a = yMean - (b * xMean)  # угловой коэффициент
    qX = np.std(x)
    qY = np.std(y)

    r = b * (qX / qY)  # линейный коэффициент корреляции
    r2 = np.power(r, 2)
    FObs = (r2 / (1 - r2)) * (len(x) - 2)

    FCrit = f.ppf(1 - alpha, dfn=1, dfd=len(x) - 2)  # вычисление F-крит

    lx1 = x.min()
    ly1 = a + (b * lx1)
    lx2 = max(x)
    ly2 = a + (b * lx2)

    rss = (np.power(y - ((x * b) + a), 2).sum()) / (
            len(x) - 2)

    sB = np.sqrt(rss) / (qX * np.sqrt(len(x)))
    sA = (np.sqrt(rss) * np.sqrt(x2.sum())) / (qX * len(x))
    sR = np.sqrt((1 - r2) / (len(x) - 2))

    tB = b / sB
    tA = a / sA
    tr = r / sR

    TCrit = t.ppf(1 - (alpha / 2), len(x) - 2)  # t-крит

    xP = predictedX  # Предсказываемый x
    yP = a + (b * xP)  # Результат предсказания x

    m = np.sqrt(rss * (1 + (1 / len(x)) + (np.power((xP - xMean), 2) / (len(x) * np.power(qX, 2)))))
    delta = m * TCrit

    plt.scatter(x, y)  # Оценки
    plt.plot([lx1, lx2], [ly1, ly2], color='r')  # прямая регрессии
    plt.scatter([xP], [yP], color='y')  # предсказываемый x

    plt.xlabel('Очередность оценки')
    plt.ylabel('Оценка')
    plt.legend(["Оценка", "Прямая регрессии", "Предсказываемый x"])

    return {
        'a': a,
        'b': b,
        "f": (
            FObs > FCrit,  # Можно ли принять H0
            FObs,  # Наблюдаемое значение критерия Фишера
            FCrit  # Критичекское значение критерия Фишера
        ),
        "tB": (
            tB > TCrit,
            tB,  # Наблюдаемое значение критерия Стьюдента
            TCrit  # Критичекское значение критерия Стьюдента
        ),
        "tA": (
            tA > TCrit,  # Можно ли принять H0
            tA,  # Наблюдаемое значение критерия Стьюдента
            TCrit  # Критичекское значение критерия Стьюдента
        ),
        "tr": (
            tr > TCrit,  # Можно ли принять H0
            tr,  # Наблюдаемое значение критерия Стьюдента
            TCrit  # Критичекское значение критерия Стьюдента
        ),
        'predict': {
            'y': yP,
            'isSafety': (yP - delta) <= yP <= (yP + delta)
        }
    }


if __name__ == '__main__':
    with getConnection() as connection:
        cursor = connection.cursor()

        # для testDatas
        # data = np.matrix(functools.reduce(lambda acc, item: acc + [rmSpaces(map(float, map(float, rmSpaces(re.split(r"( )+", item.strip())))))], testDatas.strip().split('\n'), []))
        # x = np.asarray(data[:, 5])
        # y = np.asarray(data[:, 13])

        # для теста
        #x = np.array([1.2, 3.1, 5.3, 7.4, 9.6, 11.8, 14.5, 18.7])
        #y = np.array([0.9, 1.2, 1.8, 2.2, 2.6, 2.9, 3.3, 3.8])

        marks = performance.getStudentMarksByGroup(cursor, 1)
        y = list(
            map(
                lambda item: np.mean(item),
                functools.reduce(
                    lambda acc, item: {**acc, item[1]: [*acc[item[1]], item[3]]} if acc.get(item[1]) else {**acc,
                        item[1]: [item[3]]},
                    marks,
                    {}
                ).values()
            )
        )
        x = list(set(map(lambda item: item[1], marks)))

        print(x)
        print(y)

        print(getRegression(x, y, 9))

        plt.show()
