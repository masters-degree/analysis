# Хайкин С. Нейронные сети: полный курс. М.: ООО «И. Д. Вильямс», 2006. 1104 с.
# https://www.youtube.com/watch?v=0tG9isAuJE8
# https://colab.research.google.com/drive/1NwyjYcmhivAYi2tGyUBLVHLD3cwEy5rl?usp=sharing#scrollTo=-sd7lP9t2UB_
# https://habr.com/ru/post/495884/
# https://habr.com/ru/post/426797/
import functools

import numpy as np
import matplotlib.pyplot as plt
from db.repositories import performance
from db import getConnection


data = '''Zimbabwe	ZWE	1960	3776681
Zimbabwe	ZWE	1961	3905034
Zimbabwe	ZWE	1962	4039201
Zimbabwe	ZWE	1963	4178726
Zimbabwe	ZWE	1964	4322861
Zimbabwe	ZWE	1965	4471177
Zimbabwe	ZWE	1966	4623351
Zimbabwe	ZWE	1967	4779827
Zimbabwe	ZWE	1968	4941906
Zimbabwe	ZWE	1969	5111337
Zimbabwe	ZWE	1970	5289303
Zimbabwe	ZWE	1971	5476982
Zimbabwe	ZWE	1972	5673911
Zimbabwe	ZWE	1973	5877726
Zimbabwe	ZWE	1974	6085074
Zimbabwe	ZWE	1975	6293875
Zimbabwe	ZWE	1976	6502569
Zimbabwe	ZWE	1977	6712827
Zimbabwe	ZWE	1978	6929664
Zimbabwe	ZWE	1979	7160023
Zimbabwe	ZWE	1980	7408624
Zimbabwe	ZWE	1981	7675591
Zimbabwe	ZWE	1982	7958241
Zimbabwe	ZWE	1983	8254747
Zimbabwe	ZWE	1984	8562249
Zimbabwe	ZWE	1985	8877489
Zimbabwe	ZWE	1986	9200149
Zimbabwe	ZWE	1987	9527203
Zimbabwe	ZWE	1988	9849125
Zimbabwe	ZWE	1989	10153852
Zimbabwe	ZWE	1990	10432421
Zimbabwe	ZWE	1991	10680995
Zimbabwe	ZWE	1992	10900502
Zimbabwe	ZWE	1993	11092766
Zimbabwe	ZWE	1994	11261744
Zimbabwe	ZWE	1995	11410714
Zimbabwe	ZWE	1996	11541217
Zimbabwe	ZWE	1997	11653242
Zimbabwe	ZWE	1998	11747072
Zimbabwe	ZWE	1999	11822719
Zimbabwe	ZWE	2000	11881477
Zimbabwe	ZWE	2001	11923914
Zimbabwe	ZWE	2002	11954290
Zimbabwe	ZWE	2003	11982224
Zimbabwe	ZWE	2004	12019912
Zimbabwe	ZWE	2005	12076699
Zimbabwe	ZWE	2006	12155491
Zimbabwe	ZWE	2007	12255922
Zimbabwe	ZWE	2008	12379549
Zimbabwe	ZWE	2009	12526968
Zimbabwe	ZWE	2010	12697723
Zimbabwe	ZWE	2011	12894316
Zimbabwe	ZWE	2012	13115131
Zimbabwe	ZWE	2013	13350356
Zimbabwe	ZWE	2014	13586681
Zimbabwe	ZWE	2015	13814629
Zimbabwe	ZWE	2016	14030390
Zimbabwe	ZWE	2017	14236745
Zimbabwe	ZWE	2018	14439018'''

with getConnection() as connection:
    cursor = connection.cursor()
    data1 = performance.getStudentsByDepartment(cursor, 'IDEPT1825')
    studentMeanMark = {}

    for id, mark, semesterId in data1:
        marks = studentMeanMark.get(semesterId)
        if marks:
            studentMeanMark[semesterId] = marks + [mark]
        else:
            studentMeanMark.setdefault(semesterId, [mark])

    for id, marks in studentMeanMark.items():
        studentMeanMark[id] = np.mean(marks)

    data1 = np.array(list(studentMeanMark.items())).transpose().tolist()


    input_len = 5
    output_len = 2
    piece_num = (len(data1[1]) - input_len - output_len)
    print(piece_num)
    data_x_list = []
    data_y_list = []
    for i in range(piece_num):
        vekt_x = np.reshape(data1[1][i:i + input_len], (input_len, 1))
        data_x_list.append(vekt_x)
        data_y_list.append(data1[1][i + input_len:i + input_len + output_len])

    print(data_x_list)
    data_array = np.stack(data_x_list)
    data_y_array = np.stack(data_y_list)

    print(data_array)

    from keras.layers import Dense, BatchNormalization, LeakyReLU
    from keras.layers import Activation, Input, MaxPooling1D, Dropout
    from keras.layers import AveragePooling1D, Conv1D, Flatten
    from keras.models import Sequential, Model
    from keras.optimizers import Adam, RMSprop, SGD

    model = Sequential()
    model.add(Conv1D(filters=32, kernel_size=5, padding="same", strides=1, input_shape=(input_len, 1)))

    model.add(Conv1D(8, output_len))
    model.add(Dropout(0.3))
    model.add(Conv1D(16, output_len))
    model.add(Dropout(0.3))
    model.add(Flatten())
    model.add(Dense(16, activation='relu'))
    model.add(Dense(output_len, activation=None))

    optimizer = Adam(learning_rate=0.0001, beta_1=0.9, beta_2=0.999, amsgrad=False)

    model.compile(optimizer=optimizer, loss='mae')

    EPOCHS = 1000

    model.fit(data_array, data_y_array, epochs=EPOCHS, batch_size=output_len)

    print("Model trained")

    val_data = np.array(data1[1][len(data1[1]) - input_len - output_len:len(data1[1]) - output_len])
    val_data = np.reshape(val_data, (1, input_len, 1))
    val_arg = data1[0][len(data1[0]) - output_len:]
    pred = model.predict([val_data])

    plt.plot(data1[0], data1[1], 'g', val_arg, pred[0], 'bo')

if __name__ == '__main__':
    plt.show()
