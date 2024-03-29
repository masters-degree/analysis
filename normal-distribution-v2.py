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

def pr(data):
    for i, (x, y) in enumerate(data.items()):
        if i % 39 == 0:
            print()
        print(f'{x}\t{y}')
def getNormalDistribution(marks):
    dataBase = marks
    dataLen = len(dataBase)
    dataBase.sort()
    dataBase.reverse()

    new = []
    # избавление от нулей
    for index, item in enumerate(dataBase):
        if item > 0:
            new.append(item)

    dataBase = new

    # подсчет количества вхождений в интервал (количества x в выборке)
    marksCount = functools.reduce(
        lambda acc, mark: {**acc, mark: acc[mark] + 1} if acc.get(mark) else {**acc, mark: 1}, dataBase, {})

    # для коректного вида гистрограмм для отсутствующих оценко проставляем количество 0
    baseDistribution = {}
    for mark in range(1, 101):
        markCount = marksCount.get(mark)

        baseDistribution.setdefault(mark, markCount if markCount else 0)

    # частоты базового расмпределения
    baseDistribution = list(baseDistribution.values())

    m = np.mean(dataBase)
    d = np.var(dataBase)
    q = np.std(dataBase)
    print('Матожидание - ', m)
    print('Средниквадратическое отклонение - ', q)
    print('Дисперсия - ', d)

    plt.ylabel('Количество')
    plt.xlabel('Оценка')

    # равномерное расрпеделение от 1 до 100
    x = np.linspace(1, 100, 100)

    # теоритическое нормальное распределение с заданным матожиданием (m) и среднеквадратическим отклонением (q)
    theoreticalDistribution = norm.pdf(x, loc=m, scale=q)
    # преобразование частот к подобию изначального распределения
    theoreticalDistribution = list(map(lambda item: item * len(dataBase), theoreticalDistribution))

    # удаленные частосты-выбросы
    deleted = [*baseDistribution]

    for index, theoreticalCount in enumerate(theoreticalDistribution):
        if baseDistribution[index] > (math.ceil(theoreticalCount * 1.25)):
            baseDistribution[index] = 0
        else:
            deleted[index] = 0

    # гистограмма базового распредления
    plt.hist(range(1, 101), weights=baseDistribution, range=(1, 100), bins=100)

    # гистограмма теоритического распределения
    plt.hist(x, weights=theoreticalDistribution, alpha=0.6, range=(1, 100), bins=100)

    # гистограмма удаленных частот
    plt.hist(range(1, 101), weights=deleted, color='red', alpha=0.4, range=(1, 100), bins=100)

    for index, _deleted in enumerate(deleted):
        if _deleted > 0:
            print(f'Удалена оценка {index + 1} с количеством {_deleted}')
            dataBase = list(filter(lambda item: not (item == index + 1), dataBase))

    marksCount = functools.reduce(
        lambda acc, mark: {**acc, mark: acc[mark] + 1} if acc.get(mark) else {**acc, mark: 1}, dataBase, {})

    _, p = normaltest(dataBase)

    resultCheck, theoreticalDistributionFromCheck, x2, x2Crit = checkNormalDistribution(marksCount, dataLen, m=m, q=q,
                                                                                        alpha=0.01)

    deletedMarks = map(str, functools.reduce(
        lambda acc, item: acc + [deleted.index(item) + 1] if deleted[deleted.index(item)] > 0 else acc, deleted, []))

    # гистограмма теоритических частот, при расчете критерия Пирсона
    plt.hist(theoreticalDistributionFromCheck.keys(), weights=theoreticalDistributionFromCheck.values(), color='green', alpha=0.4, range=(1, 100), bins=100)
    plt.legend(
        ["Изначальное распределение", "Теоретические распределение", f"Удаленные выбросы ({', '.join(deletedMarks)})",
         "Теоретические частоты (проверка критерия Пирсона)"])

    print(f'P-value {p}')
    print(f"result from custom check {resultCheck}")


if __name__ == '__main__':
    with getConnection() as connection:
        cursor = connection.cursor()

        plt.title('Оценки группы за семестр')
        getNormalDistribution(list(item[3] for item in performance.getStudentMarksByGroupAndSemester(cursor, 1, 1)))

        plt.figure()
        plt.title('Оценки всех студентов')
        getNormalDistribution(list(item[1] for item in performance.getStudentsMarks(cursor)))

        plt.figure()
        plt.title('Оценка одного студента')
        getNormalDistribution(list(item[0] for item in performance.getStudentMarks(cursor, 1)))

        plt.figure()
        plt.title('Оценка студентов института за предмет')
        getNormalDistribution(
            list(item[1] for item in performance.getStudentsBySubject(cursor, 'SEMI0012995', 'IDEPT5528')))

        plt.show()
