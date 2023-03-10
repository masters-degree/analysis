# проверка нормальности распределения https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.normaltest.html
# https://statanaliz.info/statistica/proverka-gipotez/kriterij-soglasiya-pirsona-khi-kvadrat/
# https://python-school.ru/blog/python-for-statissticians/
# http://www.mathprofi.ru/asimmetriya_i_excess.html - про эксцесс и ассиметрию
import functools

import numpy as np
import matplotlib.pyplot as plt
from db.repositories import performance
from db import getConnection
from check_normal_distribution import checkNormalDistribution

normData = [65.3479471204239,
            80.72858060346245,
            40.807971864501035,
            98.637140652347,
            83.41639083278278,
            56.441190337124354,
            85.95696552190762,
            97.04104050468422,
            97.99637020203468,
            84.5528841165255,
            80.67146830034501,
            70.51282867665608,
            90.36198249480914,
            85.993991402105,
            95.75958856239644,
            100.76546514515307,
            69.62066165067156,
            19.069584951751608,
            71.9746459083607,
            74.03015504168889,
            58.120433736173425,
            84.64678904289693,
            94.05108061948482,
            53.60441159290389,
            67.06128222811553,
            73.88760753938804,
            48.269383587310315,
            74.2632441259401,
            82.22963169148773,
            57.59735441944187,
            107.90729113377189,
            88.0556922822173,
            64.34007897998218,
            88.31123621050232,
            63.7202278415096,
            101.10436924551682,
            70.22522235404098,
            105.73494733621784,
            63.4171349940563,
            112.85769192726761,
            80.83982433277141,
            68.77774898787766,
            121.12697736382152,
            63.1305864588483,
            89.57621261916182,
            69.86907068115333,
            77.5061705365097,
            84.81108136686294,
            69.03319270541579,
            77.64060319602054,
            105.71029296978426,
            84.67885951583882,
            30.854463919933785,
            89.4805094851848,
            43.66228494514082,
            60.71349167583491,
            85.09310617480406,
            81.56068708444162,
            118.82180657102276,
            54.02342744604413,
            117.06483191009343,
            122.28178807750645,
            78.3157198221219,
            69.4400775495202,
            71.02185854472003,
            51.8104385113344,
            84.5851518352215,
            100.82033559369843,
            75.4984735931124,
            52.18738819368521,
            74.48357491519666,
            93.6043913433385,
            93.32238630910062,
            72.85466963537917,
            64.02445620122855,
            89.93423926554077,
            72.70026127556625,
            72.60595964423506,
            80.17985131788093,
            90.809438644151,
            61.51488936537895,
            59.601755599953975,
            51.737269990666086,
            91.4571235326929,
            111.48641551403769,
            111.77396481424208,
            14.841452357355422,
            123.16906285743211,
            58.193046415018586,
            57.90330960424363,
            91.28652806398681,
            58.50595801494084,
            103.52241827583236,
            51.50751061506024,
            60.16275235751309,
            116.38099468429633,
            82.67815688280493,
            69.02056098469741,
            77.68945564198675,
            93.25314023518104]

if __name__ == '__main__':
    with getConnection() as connection:
        cursor = connection.cursor()
        dataBase = list(item[3] for item in performance.getStudentsByDepartamentAndSemester(cursor, 'IDEPT1825', 8))
        dataLen = len(dataBase) # количество оценок

        dataBase.sort()
        dataBase.reverse()

        marksCount = functools.reduce(
            lambda acc, mark: {**acc, mark: acc[mark] + 1} if acc.get(mark) else {**acc, mark: 1}, dataBase, {})
        data = list(map(lambda item: item[1] / dataLen, marksCount.items()))

        print(data)

        print('Матожидание - ', functools.reduce(lambda acc, item: (item[0] * item[1]) + acc, marksCount.items(), 0) / sum(marksCount.values()))
        print('Средниквадратическое отклонение - ', np.nanstd(dataBase))
        print('Дисперсия - ', np.nanvar(dataBase))

        plt.hist(marksCount.keys(), weights=data, label='sdfsdf', bins=50)

        plt.ylabel('P')
        plt.xlabel('Оценка')

        print(checkNormalDistribution(marksCount, 1, dataLen))

        plt.show()
