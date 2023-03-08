# проверка нормальности распределения https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.normaltest.html
# https://statanaliz.info/statistica/proverka-gipotez/kriterij-soglasiya-pirsona-khi-kvadrat/
# https://python-school.ru/blog/python-for-statissticians/
# http://www.mathprofi.ru/asimmetriya_i_excess.html - про эксцесс и ассиметрию

import numpy as np
from scipy.stats import norm, normaltest
import matplotlib.pyplot as plt
from db.repositories import performance
from db import getConnection


if __name__ == '__main__':
    with getConnection() as connection:
        cursor = connection.cursor()
        data = list(item[3] for item in performance.getStudentsByDepartamentAndSemester(cursor, 'IDEPT1825', 8))

        mean, var, skew, kurt = norm.stats(moments='mvsk')

        x = np.linspace(norm.ppf(0.01, loc=np.mean(data), scale=np.std(data)),
                        norm.ppf(0.99, loc=np.mean(data), scale=np.std(data)), len(data))

        plt.plot(x, norm.pdf(x, loc=np.mean(data), scale=np.std(data)),
                 'r-', lw=5, alpha=0.6, label='norm pdf')

        plt.hist(data, density=True, bins='auto', histtype='stepfilled', alpha=0.2)

        xi2, p = normaltest(data) # p - Двусторонняя вероятность хи-квадрат для проверки гипотезы (вероятность того, что распределение нормальное)

        alpha = 0.05

        print(data)

        print(xi2, p, alpha)

        if p > alpha:
            print("The null hypothesis cannot be rejected")
        else:
            print("The null hypothesis can be rejected")

        plt.show()
