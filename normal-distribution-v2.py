# проверка нормальности распределения https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.normaltest.html
# https://statanaliz.info/statistica/proverka-gipotez/kriterij-soglasiya-pirsona-khi-kvadrat/
# https://python-school.ru/blog/python-for-statissticians/
# http://www.mathprofi.ru/asimmetriya_i_excess.html - про эксцесс и ассиметрию
# https://studbooks.net/2256067/matematika_himiya_fizika/vyyavlenie_grubyh_oshibok_vyborke_isklyuchenie_anomalnyh_znacheniy

import copy
import functools

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from db.repositories import performance
from db import getConnection
from check_normal_distribution import checkNormalDistribution
from scipy.stats import norm, normaltest

normData = [74,63,74,68,64,75,62,67,61,74,79,70,71,75,66,74,65,65,65,67,72,79,70,76,75,59,79,67,70,69,65,78,78,66,69,77,73,71,63,75,66,73,67,70,62,74,66,77,63,73,72,72,65,77,74,68,70,75,73,70,64,68,69,77,69,64,75,73,66,65,66,71,72,76,65,68,64,69,70,72,74,69,68,72,73,80,73,68,73,64,68,74,64,67,72,74,73,73,73,69,71,79,61,61,58,79,67,73,72,72,66,75,73,73,74,73,72,75,75,72,70,67,73,69,69,68,77,71,70,81,72,65,68,63,70,65,74,61,68,71,63,70,75,69,68,75,64,67,71,78,67,66,75,75,63,63,69,64,66,70,74,70,68,72,76,73,63,68,74,69,74,67,70,68,68,73,69,62,69,69,71,73,69,66,68,71,71,67,67,68,68,72,69,66,64,77,75,70,65,67,72,68,68,65,74,72,75,64,70,63,61,66,68,78,68,80,72,72,68,68,65,79,65,70,73,66,76,63,63,75,62,67,68,66,69,65,70,68,68,78,71,68,76,71,70,62,65,70,68,59,67,71,75,62,75,74,68,63,71,71,64,65,78,66,79,65,71,69,69,74,72,69,72,68,71,77,71,75,66,75,66,60,69,75,73,63,79,77,72,73,66,78,70,71,80,78,69,74,64,79,67,65,71,72,65,76,68,70,78,71,67,68,70,70,74,69,68,62,64,72,63,75,76,70,68,58,74,65,70,80,64,61,71,76,76,66,69,71,67,74,75,73,70,70,66,72,68,71,76,74,69,76,64,65,64,67,68,72,77,69,74,64,80,72,74,78,68,79,68,73,74,67,73,74,63,69,73,78,67,82,71,73,78,73,73,66,73,71,75,72,71,74,72,76,68,80,68,73,65,78,74,59,77,70,70,59,67,71,71,76,78,77,71,64,72,71,78,63,71,68,62,68,67,68,69,69,71,62,74,71,65,68,75,75,72,66,70,65,71,65,72,77,71,69,69,69,69,73,72,79,72,64,66,72,69,62,65,77,67,78,77,64,76,60,73,72,60,76,71,71,79,76,78,64,66,76,64,61,72,74,69,69,64,83,65,69,66,72,63,75,64,60,65,71,70,76,70,77,74,79,62,74,69,72,69,77,68,67,66,75,64,71,67,79,69,63,65,69,71,80,78,70,69,68,57,75,74,60,75,69,67,72,71,77,70,73,80,82,71,78,73,75,72,69,80,75,66,71,64,68,75,76,76,62,71,70,69,68,67,70,74,75,63,67,69,80,66,73,68,74,75,65,75,68,70,69,71,66,70,64,68,74,81,59,66,66,76,76,71,63,74,72,78,84,67,71,69,61,72,71,83,64,65,71,76,76,70,73,74,63,68,70,63,76,77,72,69,60,69,63,80,66,62,74,64,70,75,66,75,64,76,70,61,68,74,60,72,73,71,67,72,70,60,71,70,68,73,70,66,69,75,66,72,76,66,62,68,77,68,72,82,74,71,65,73,70,72,63,73,74,79,59,67,74,68,75,70,78,71,73,67,64,65,66,76,69,69,58,67,79,73,75,73,71,77,75,74,69,70,77,76,68,79,64,75,75,70,68,59,66,69,72,76,70,75,63,72,74,68,75,67,69,64,70,78,64,66,65,71,65,73,79,77,70,67,73,65,75,69,78,71,85,71,70,67,69,74,74,73,70,71,78,65,66,60,68,61,62,73,72,66,75,79,78,70,75,70,81,68,73,77,69,67,71,69,66,72,73,59,72,76,71,71,73,68,73,69,77,65,74,73,77,75,77,65,68,74,65,75,76,78,67,65,69,68,78,69,75,71,66,65,61,71,77,65,69,75,66,73,61,66,76,69,72,68,71,61,71,74,73,70,80,67,67,77,75,79,64,72,82,76,75,73,78,66,69,69,63,75,77,74,70,74,65,68,69,70,75,66,81,71,80,67,68,70,65,76,65,62,75,75,76,72,71,71,66,68,67,69,69,69,68,63,66,70,77,67,71,72,82,74,68,69,68,72,67,72,61,65,69,68,64,73,70,72,74,78,70,72,64,68,68,72,61,72,72,70,73,72,70,66,78,62,76,65,71,75,67,67,71,68,76,69,67,66,71,64,71,64,68,67,73,70,80,64,67,72,69,76,75,71,70,78,82,83,72,79,67,72,65,68,69,64,66,70,74,76,69,83,62,66,67,69,71,70,81,76,68,64,65,76,68,70,75,74,72,68,69,65,74,64,71,85,75,74,70,61,74,77,68]


def grubbs_stat(y):
    std_dev = np.std(y)
    avg_y = np.mean(y)
    abs_val_minus_avg = abs(y - avg_y)
    max_of_deviations = max(abs_val_minus_avg)
    max_ind = np.argmax(abs_val_minus_avg)
    Gcal = max_of_deviations / std_dev
    return Gcal, max_ind

def calculate_critical_value(size, alpha):
    t_dist = stats.t.ppf(1 - alpha / (2 * size), size - 2)
    numerator = (size - 1) * np.sqrt(np.square(t_dist))
    denominator = np.sqrt(size) * np.sqrt(size - 2 + np.square(t_dist))
    critical_value = numerator / denominator
    return critical_value


def check_G_values(Gs, Gc, inp, max_index):
    return Gs > Gc

if __name__ == '__main__':
    with getConnection() as connection:
        cursor = connection.cursor()

        """
        добавить инфу про отсичение больших значений на границах, типа  не я сделал
        описание бд (структура, поля)
        составить список методов анализа
    
        добавить в график что ща выборка и матожидание, среднее и тд
        выводить количество оценок
        
        построить нескольго графиков
        """

        def clear(data):
            dataLen = len(data)
            res = [*data]

            for _ in range(0, int(dataLen / 2)):
                Gcritical = calculate_critical_value(dataLen, 0.05)
                Gstat, max_index = grubbs_stat(res)

                if check_G_values(Gstat, Gcritical, res, max_index):
                    print(f'popped - {res[max_index]}')
                    res.pop(max_index)

            return res

        leftBorder = 60 # леваая граница отсичения оценко
        rightBorder = 90 # правая граница отсичения оценк
        dataBase = list(item[0] for item in performance.getStudentMarks(cursor, 'SID20131143'))
        dataBase = clear(functools.reduce(lambda acc, item: acc + [item] if item not in [] else acc, dataBase, []))
        dataLen = len(dataBase)  # вариантов оценок можеть быть от 0 до 100

        dataBase.sort()
        dataBase.reverse()

        marksCount = functools.reduce(
            lambda acc, mark: {**acc, mark: acc[mark] + 1} if acc.get(mark) else {**acc, mark: 1}, dataBase, {})

        baseMarksCount = copy.deepcopy(marksCount)

        countM = np.mean(list(marksCount.values()))

        # Оценки от 0 до 100 с их вероятностью, если оценки небыло в изначальном массиве ее вероятность = 0
        foolMarksWithProbability = {}
        for mark in range(1, 101):
            markCount = marksCount.get(mark)

            foolMarksWithProbability.setdefault(mark, markCount / dataLen if markCount else 0)

        plt.hist(foolMarksWithProbability.keys(), weights=foolMarksWithProbability.values(),
                 bins=len(foolMarksWithProbability.keys()))

        m = np.mean(dataBase)
        d = np.var(dataBase)
        q = np.std(dataBase)
        print('Матожидание - ', m)
        print('Средниквадратическое отклонение - ', q)
        print('Дисперсия - ', d)

        plt.ylabel('P')
        plt.xlabel('Оценка')

        x = np.linspace(1, 100, 100)

        theoreticalDistribution = norm.pdf(x, loc=m, scale=q)

        plt.plot(x, theoreticalDistribution)

        print(checkNormalDistribution(baseMarksCount, 1, dataLen, alpha=0.05))

        _, p = normaltest(dataBase)
        print(f'P-value {p}')
        plt.show()
