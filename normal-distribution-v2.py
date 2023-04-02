# проверка нормальности распределения https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.normaltest.html
# https://statanaliz.info/statistica/proverka-gipotez/kriterij-soglasiya-pirsona-khi-kvadrat/
# https://python-school.ru/blog/python-for-statissticians/
# http://www.mathprofi.ru/asimmetriya_i_excess.html - про эксцесс и ассиметрию
# https://studbooks.net/2256067/matematika_himiya_fizika/vyyavlenie_grubyh_oshibok_vyborke_isklyuchenie_anomalnyh_znacheniy
# https://translated.turbopages.org/proxy_u/en-ru.ru.53124c72-642939c1-0a4ccc9a-74722d776562/https/www.thoughtco.com/the-difference-between-alpha-and-p-values-3126420

import copy
import functools
import math

import numpy as np
import matplotlib.pyplot as plt
from db.repositories import performance
from db import getConnection
from check_normal_distribution import checkNormalDistribution
from scipy.stats import norm, normaltest

normData = [56.0, 57.0, 57.0, 58.0, 58.0, 58.0, 59.0, 59.0, 59.0, 59.0, 59.0, 60.0, 60.0, 60.0, 60.0, 60.0, 60.0, 60.0, 60.0, 60.0, 61.0, 61.0, 61.0, 61.0, 61.0, 61.0, 61.0, 61.0, 61.0, 61.0, 61.0, 61.0, 61.0, 62.0, 62.0, 62.0, 62.0, 62.0, 62.0, 62.0, 62.0, 62.0, 62.0, 62.0, 62.0, 62.0, 62.0, 62.0, 62.0, 62.0, 62.0, 62.0, 63.0, 63.0, 63.0, 63.0, 63.0, 63.0, 63.0, 63.0, 63.0, 63.0, 63.0, 63.0, 63.0, 63.0, 63.0, 63.0, 63.0, 63.0, 63.0, 63.0, 63.0, 63.0, 63.0, 63.0, 63.0, 63.0, 64.0, 64.0, 64.0, 64.0, 64.0, 64.0, 64.0, 64.0, 64.0, 64.0, 64.0, 64.0, 64.0, 64.0, 64.0, 64.0, 64.0, 64.0, 64.0, 64.0, 64.0, 64.0, 64.0, 64.0, 64.0, 64.0, 64.0, 64.0, 64.0, 64.0, 64.0, 64.0, 64.0, 64.0, 64.0, 65.0, 65.0, 65.0, 65.0, 65.0, 65.0, 65.0, 65.0, 65.0, 65.0, 65.0, 65.0, 65.0, 65.0, 65.0, 65.0, 65.0, 65.0, 65.0, 65.0, 65.0, 65.0, 65.0, 65.0, 65.0, 65.0, 65.0, 65.0, 65.0, 65.0, 65.0, 65.0, 65.0, 65.0, 65.0, 65.0, 65.0, 65.0, 65.0, 65.0, 65.0, 65.0, 65.0, 65.0, 66.0, 66.0, 66.0, 66.0, 66.0, 66.0, 66.0, 66.0, 66.0, 66.0, 66.0, 66.0, 66.0, 66.0, 66.0, 66.0, 66.0, 66.0, 66.0, 66.0, 66.0, 66.0, 66.0, 66.0, 66.0, 66.0, 66.0, 66.0, 66.0, 66.0, 66.0, 66.0, 66.0, 66.0, 66.0, 66.0, 66.0, 66.0, 66.0, 66.0, 66.0, 66.0, 66.0, 66.0, 66.0, 66.0, 66.0, 66.0, 66.0, 66.0, 66.0, 66.0, 66.0, 66.0, 67.0, 67.0, 67.0, 67.0, 67.0, 67.0, 67.0, 67.0, 67.0, 67.0, 67.0, 67.0, 67.0, 67.0, 67.0, 67.0, 67.0, 67.0, 67.0, 67.0, 67.0, 67.0, 67.0, 67.0, 67.0, 67.0, 67.0, 67.0, 67.0, 67.0, 67.0, 67.0, 67.0, 67.0, 67.0, 67.0, 67.0, 67.0, 67.0, 67.0, 67.0, 67.0, 67.0, 67.0, 67.0, 67.0, 67.0, 67.0, 67.0, 67.0, 67.0, 67.0, 67.0, 67.0, 67.0, 67.0, 67.0, 67.0, 67.0, 67.0, 67.0, 67.0, 67.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 68.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 69.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 71.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 72.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 73.0, 74.0, 74.0, 74.0, 74.0, 74.0, 74.0, 74.0, 74.0, 74.0, 74.0, 74.0, 74.0, 74.0, 74.0, 74.0, 74.0, 74.0, 74.0, 74.0, 74.0, 74.0, 74.0, 74.0, 74.0, 74.0, 74.0, 74.0, 74.0, 74.0, 74.0, 74.0, 74.0, 74.0, 74.0, 74.0, 74.0, 74.0, 74.0, 74.0, 74.0, 74.0, 74.0, 74.0, 74.0, 74.0, 74.0, 74.0, 74.0, 74.0, 74.0, 74.0, 74.0, 74.0, 74.0, 74.0, 74.0, 74.0, 74.0, 74.0, 74.0, 74.0, 75.0, 75.0, 75.0, 75.0, 75.0, 75.0, 75.0, 75.0, 75.0, 75.0, 75.0, 75.0, 75.0, 75.0, 75.0, 75.0, 75.0, 75.0, 75.0, 75.0, 75.0, 75.0, 75.0, 75.0, 75.0, 75.0, 75.0, 75.0, 75.0, 75.0, 75.0, 75.0, 75.0, 75.0, 75.0, 75.0, 75.0, 75.0, 75.0, 75.0, 75.0, 75.0, 75.0, 75.0, 75.0, 75.0, 75.0, 75.0, 75.0, 75.0, 75.0, 75.0, 76.0, 76.0, 76.0, 76.0, 76.0, 76.0, 76.0, 76.0, 76.0, 76.0, 76.0, 76.0, 76.0, 76.0, 76.0, 76.0, 76.0, 76.0, 76.0, 76.0, 76.0, 76.0, 76.0, 76.0, 76.0, 76.0, 76.0, 76.0, 76.0, 76.0, 76.0, 76.0, 76.0, 76.0, 76.0, 76.0, 76.0, 76.0, 76.0, 76.0, 76.0, 76.0, 77.0, 77.0, 77.0, 77.0, 77.0, 77.0, 77.0, 77.0, 77.0, 77.0, 77.0, 77.0, 77.0, 77.0, 77.0, 77.0, 77.0, 77.0, 77.0, 77.0, 77.0, 77.0, 77.0, 77.0, 77.0, 77.0, 77.0, 77.0, 77.0, 77.0, 77.0, 77.0, 77.0, 78.0, 78.0, 78.0, 78.0, 78.0, 78.0, 78.0, 78.0, 78.0, 78.0, 78.0, 78.0, 78.0, 78.0, 78.0, 78.0, 78.0, 78.0, 78.0, 78.0, 78.0, 78.0, 78.0, 78.0, 79.0, 79.0, 79.0, 79.0, 79.0, 79.0, 79.0, 79.0, 79.0, 79.0, 79.0, 79.0, 79.0, 79.0, 79.0, 79.0, 79.0, 79.0, 80.0, 80.0, 80.0, 80.0, 80.0, 80.0, 80.0, 80.0, 80.0, 80.0, 80.0, 80.0, 81.0, 81.0, 81.0, 81.0, 81.0, 81.0, 81.0, 81.0, 82.0, 82.0, 82.0, 82.0, 82.0, 83.0, 83.0, 83.0, 84.0, 85.0]

def getNormalDistribution(marks):
    dataBase = marks

    dataLen = len(dataBase)

    dataBase.sort()
    dataBase.reverse()

    marksCount = functools.reduce(
        lambda acc, mark: {**acc, mark: acc[mark] + 1} if acc.get(mark) else {**acc, mark: 1}, dataBase, {})

    # Оценки от 0 до 100 с их вероятностью, если оценки небыло в изначальном массиве ее вероятность = 0
    baseDistribution = {}
    for mark in range(1, 101):
        markCount = marksCount.get(mark)

        baseDistribution.setdefault(mark, markCount if markCount else 0)

    baseDistribution = list(baseDistribution.values())

    m = np.mean(dataBase)
    d = np.var(dataBase)
    q = np.std(dataBase)
    print('Матожидание - ', m)
    print('Средниквадратическое отклонение - ', q)
    print('Дисперсия - ', d)

    plt.ylabel('Количество')
    plt.xlabel('Оценка')

    x = np.linspace(1, 100, 100)

    theoreticalDistribution = norm.pdf(x, loc=m, scale=q)
    theoreticalDistribution = list(map(lambda item: item * len(dataBase), theoreticalDistribution))

    deleted = [*baseDistribution]

    for index, theoreticalCount in enumerate(theoreticalDistribution):
        if baseDistribution[index] > (math.ceil(theoreticalCount * 1.25)):
            baseDistribution[index] = 0
        else:
            deleted[index] = 0

    plt.hist(range(1, 101), weights=baseDistribution,
             bins=len(baseDistribution))

    plt.hist(x, weights=theoreticalDistribution,
             bins=len(theoreticalDistribution), alpha=0.6)

    plt.hist(range(1, 101), weights=deleted,
             bins=len(theoreticalDistribution), color='red', alpha=0.4)

    for index, _deleted in enumerate(deleted):
        if _deleted > 0:
            print(f'Удалена оценка {index + 1} с количеством {_deleted}')
            dataBase = list(filter(lambda item: not (item == index + 1), dataBase))

    marksCount = functools.reduce(
        lambda acc, mark: {**acc, mark: acc[mark] + 1} if acc.get(mark) else {**acc, mark: 1}, dataBase, {})

    _, p = normaltest(dataBase)

    resultCheck, theoreticalDistributionFromCheck, x2, x2Crit = checkNormalDistribution(marksCount, dataLen, m=m, q=q,
                                                                                        alpha=0.05, useGrouping=False)

    deletedMarks = map(str, functools.reduce(
        lambda acc, item: acc + [deleted.index(item) + 1] if deleted[deleted.index(item)] > 0 else acc, deleted, []))

    plt.hist(theoreticalDistributionFromCheck.keys(), weights=theoreticalDistributionFromCheck.values(),
             bins=len(theoreticalDistribution), color='green', alpha=0.4)
    plt.legend(
        ["Изначальное распределение", "Теоритическое распределение", f"Удаленные выбросы ({', '.join(deletedMarks)})",
         "Теоритическое распределение (проверка критерия пирсона)"])

    print(f'P-value {p}')
    print(f"result from custom check {resultCheck}")

    plt.suptitle(
             f'Количество оценок - {dataLen} \nМатожидание - {round(m, 2)} \nДисперсия - {round(d, 2)} \nСреднеквардратическое отклонение - {round(q, 2)}\n$x^2 = {x2}$ \n$x^2 крит = {x2Crit}$\nПринимаем H0 - {"да" if resultCheck else "Нет"}',
        horizontalalignment='left', x=0.13, y=0.75
    )


if __name__ == '__main__':
    with getConnection() as connection:
        cursor = connection.cursor()

        """
        описание бд (структура, поля)
        составить список методов анализа
        """

        plt.title('Оценки группы за семестр')
        getNormalDistribution(list(item[3] for item in performance.getStudentsByDepartamentAndSemester(cursor, 'IDEPT5528', 8)))

        plt.figure()
        plt.title('Оценки все студентов института за весь период обучения')
        getNormalDistribution(list(item[1] for item in performance.getStudentsByDepartment(cursor, 'IDEPT5528')))

        plt.figure()
        plt.title('Оценка одного студента')
        getNormalDistribution(list(item[0] for item in performance.getStudentMarks(cursor, 'SID20131177')))

        plt.figure()
        plt.title('Оценка студентов института за предмет')
        getNormalDistribution(list(item[1] for item in performance.getStudentsBySubject(cursor, 'SEMI0012995', 'IDEPT5528')))

        plt.show()
