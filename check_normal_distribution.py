# http://www.mathprofi.ru/kriteriy_soglasiya.html

import math
import numpy as np
import copy
from scipy.stats import chi2


def pr(data):
    for i, (x, y) in enumerate(data.items()):
        if i % 19 == 0:
            print()
        print(f'{x}\t{round(y, 3)}')
# xi: ni

def checkNormalDistribution(valuesAndCount, baseN, m=None, q=None, h=1, alpha=0.05):
    valuesAndCount = copy.deepcopy(valuesAndCount)
    # xi: xi * ni
    xAndN = {}
    for x, n in valuesAndCount.items():
        xAndN.setdefault(x, x * n)
    # xi: xi^2 * ni
    x2AndN = {}
    for x, n in valuesAndCount.items():
        x2AndN.setdefault(x, np.power(x, 2) * n)

    xAndNSum = sum(xAndN.values())
    x2AndNSum = sum(x2AndN.values())

    # выборочная средняя (матожидание)
    xe = xAndNSum / baseN if not m else m
    # выборочная дисперсия
    de = (x2AndNSum / baseN) - math.pow(xe, 2)
    # выборочное стандартное отклонение
    oe = math.sqrt(de) if not q else q

    # xi: zi
    xz = {}
    for x, n in valuesAndCount.items():
        xz.setdefault(x, (x - xe) / oe)

    # xi: f(zi)
    xfz = {}
    for x, z in xz.items():
        xfz.setdefault(x, (1 / (math.sqrt(2 * math.pi))) * (math.pow(math.e, -(math.pow(z, 2) / 2))))

    # xi: n' (теоритические частоты)
    nQuotes = {}
    for x, fz in xfz.items():
        nQuotes.setdefault(x, ((h * baseN) / oe * fz))

    # xi: n''
    n2Quotes = {}
    for x, nQuote in nQuotes.items():
        n2Quotes.setdefault(x, (math.pow(valuesAndCount[x] - nQuote, 2)) / nQuote)

    # вычисление x2 наблюдаемого
    x2Obs = sum(n2Quotes.values())

    # вычисление x2 критического
    x2Crit = chi2.ppf(1 - alpha, len(n2Quotes.values()) - 3)

    print(x2Obs, x2Crit)

    return x2Obs < x2Crit, nQuotes, x2Obs, x2Crit


if __name__ == '__main__':
    print(checkNormalDistribution({
        9: 2,
        12: 6,
        15: 10,
        18: 17,
        21: 33,
        24: 11,
        27: 9,
        30: 7,
        33: 5
    }, 100, h=3))
