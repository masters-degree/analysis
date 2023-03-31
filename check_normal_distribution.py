# http://www.mathprofi.ru/kriteriy_soglasiya.html
import functools
import math
import numpy as np
import copy
from scipy.stats import chi2
from scipy.special import erf

Phi = lambda x: erf(x / 2 ** 0.5) / 2

# xi: ni
def checkNormalDistribution(valuesAndCount, alpha=0.05):
    valuesAndCount = copy.deepcopy(valuesAndCount)
    x = list(valuesAndCount.keys())
    delta = max(x) - min(x)
    baseN = functools.reduce(lambda acc, item: acc + item, list(valuesAndCount.values()), 0)
    h = delta / (1 + (3.322 * math.log10(baseN)))
    m = math.floor((delta + h) / h) # оптимальный количество интервалов
    h = delta / (m - 1)
    leftIntervalsPart = []
    rightIntervalsPart = []
    intervalsPart = {}

    for i in range(0, m):
        left = (rightIntervalsPart[i - 1] if i > 0 else min(x) - (h / 2))
        right = (left + h if i > 0 else min(x) + (h / 2))
        leftIntervalsPart.append(left)
        rightIntervalsPart.append(right)
        intervalsPart.setdefault(f'{left}-{right}', 0)

    for x, n in valuesAndCount.items():
        for left, right in zip(leftIntervalsPart, rightIntervalsPart):
            if left <= x < right:
                intervalsPart[f'{left}-{right}'] = intervalsPart[f'{left}-{right}'] + n

    valuesAndCount = {}

    for left, right in zip(leftIntervalsPart, rightIntervalsPart):
        valuesAndCount.setdefault(left + (h / 2), intervalsPart[f'{left}-{right}'])

    x = list(valuesAndCount.keys())
    baseN = functools.reduce(lambda acc, item: acc + item, list(valuesAndCount.values()), 0)

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

    leftZIntervalsPart = [*leftIntervalsPart]
    rightZIntervalsPart = [*rightIntervalsPart]
    leftZIntervalsPart[0] = -math.inf
    rightZIntervalsPart[len(rightZIntervalsPart) - 1] = math.inf

    leftFZIntervalsPart = list(map(lambda z: Phi((z - xe) / oe), leftZIntervalsPart))
    rightFZIntervalsPart = list(map(lambda z: Phi((z - xe) / oe), rightZIntervalsPart))

    # xP
    xP = [*leftFZIntervalsPart]
    for indx, (left, right) in enumerate(zip(leftFZIntervalsPart, rightFZIntervalsPart)):
        xP[indx] = right - left

    # xi: n'
    nQuotes = {}
    for index, (x, n) in enumerate(valuesAndCount.items()):
        nQuotes.setdefault(x, xP[index] * baseN)

    print(valuesAndCount.values())
    print(nQuotes.values())
    print(sum(nQuotes.values()), baseN)


    def grouping(items):
        xForGrouping = None
        xForDeleting = []
        newGroups = {}
        newGroupsForCounts = {}
        # объединение интервалов
        for x, nQuote in items:
            if nQuote < 5:
                if not xForGrouping:
                    xForGrouping = [x]
                else:
                    xForGrouping.append(x)
            else:
                if xForGrouping:
                    newGroups.setdefault(x, sum([nQuotes[_x] for _x in xForGrouping]) + nQuotes[x])
                    newGroupsForCounts.setdefault(x, sum([valuesAndCount[_x] for _x in xForGrouping]) + valuesAndCount[x])
                    xForDeleting = xForDeleting + xForGrouping
                    xForGrouping = None

        return xForDeleting, newGroups, newGroupsForCounts

    xForDeleting, newGroups, newGroupsForCounts = grouping(nQuotes.items())
    for _x in xForDeleting:
        del nQuotes[_x]
        del valuesAndCount[_x]

    nQuotes = {**nQuotes, **newGroups}
    valuesAndCount = {**valuesAndCount, **newGroupsForCounts}

    items = list(nQuotes.items())
    items.reverse()

    xForDeleting, newGroups, newGroupsForCounts = grouping(items)

    for _x in xForDeleting:
        del nQuotes[_x]
        del valuesAndCount[_x]

    nQuotes = {**nQuotes, **newGroups}
    valuesAndCount = {**valuesAndCount, **newGroupsForCounts}

    # xi: n''
    n2Quotes = {}
    for x, nQuote in nQuotes.items():
        n2Quotes.setdefault(x, (math.pow(valuesAndCount[x] - nQuote, 2)) / nQuote)

    n2QuotesSum = sum(n2Quotes.values())

    print(m)
    x2 = chi2.ppf(1 - alpha, m - 3)

    #print(xAndNSum, x2AndNSum, baseN, xe, de, oe, x2)
    #print(xz.values())
    #print(xfz.values())
    #print(nQuotes.values())
    #print(n2Quotes.values())
    #print(n2QuotesSum)

    print(n2QuotesSum, x2)

    return n2QuotesSum < x2


if __name__ == '__main__':
    print(checkNormalDistribution({
        1: 1,
        1.03: 3,
        1.05: 6,
        1.06: 4,
        1.08: 2,
        1.10: 4,
        1.12: 3,
        1.15: 6,
        1.16: 5,
        1.19: 2,
        1.20: 4,
        1.23: 4,
        1.25: 8,
        1.26: 4,
        1.29: 4,
        1.30: 6,
        1.32: 4,
        1.33: 5,
        1.37: 6,
        1.38: 2,
        1.39: 1,
        1.40: 2,
        1.44: 3,
        1.45: 3,
        1.46: 2,
        1.49: 4,
        1.50: 2,
    }))
