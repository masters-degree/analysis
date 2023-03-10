# http://www.mathprofi.ru/kriteriy_soglasiya.html

import math

import numpy as np
from scipy.stats import chi2


# xi: ni
def checkNormalDistribution(valuesAndCount, h, baseN, alpha=0.05):
    xCount = len(valuesAndCount.values())
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

    # выюорочная средняя
    xe = xAndNSum / baseN
    # выюорочная дисперсия
    de = (x2AndNSum / baseN) - math.pow(xe, 2)
    # выборочное стандартное отклонение
    oe = math.sqrt(de)

    # xi: zi
    xz = {}
    for x, n in valuesAndCount.items():
        xz.setdefault(x, (x - xe) / oe)

    # xi: f(zi)
    xfz = {}
    for x, z in xz.items():
        xfz.setdefault(x, (1 / (math.sqrt(2 * math.pi))) * (math.pow(math.e, -(math.pow(z, 2) / 2))))

    # xi: n'
    nQuotes = {}
    for x, fz in xfz.items():
        nQuotes.setdefault(x, ((h * baseN) / oe * fz))

    # xi: n''
    n2Quotes = {}
    for x, nQuote in nQuotes.items():
        n2Quotes.setdefault(x, (math.pow(valuesAndCount[x] - nQuote, 2)) / nQuote)

    n2QuotesSum = sum(n2Quotes.values())

    x2 = chi2.ppf(1 - alpha, xCount - 2)

    #print(xAndNSum, x2AndNSum, baseN, xe, de, oe, x2)
    #print(xz.values())
    #print(xfz.values())
    #print(nQuotes.values())
    #print(n2Quotes.values())
    #print(n2QuotesSum)

    return n2QuotesSum < x2


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
    }, 3, 100))