import numpy as np
import math
from statsmodels.stats.stattools import medcouple
import matplotlib.pyplot as plt
import pandas as pd
from time import time

t0 = time()

def prepare(data, type = 'time'):
    #convert Series to list
    data = data.tolist()
    #Remove possible zeros
    data = list(filter(lambda a: a != float(0), data))

    qq1 = np.percentile(data, 25)
    qq3 = np.percentile(data, 75)
    IQR = qq3 - qq1

    medad = float(medcouple(data))
    if type =='time':
        if medad > 0:
            loa = qq1 - (1.5 * ((math.e ** (-4 * medad)) * IQR))
            if loa < 0:
                loa = 0
            uoa = qq3 + (1.5 * ((math.e ** (3 * medad)) * IQR))
        if medad <= 0:
            loa = qq1 - (1.5 * ((math.e ** (-3 * medad)) * IQR))
            if loa < 0:
                loa = 0
            uoa = qq3 + (1.5 * ((math.e ** (4 * medad)) * IQR))
        if medad == 0:
            loa = qq1 - (1.5 * IQR)
            if loa < 0:
                loa = 0
            uoa = qq3 + (1.5 * IQR)
    else:
        if medad > 0:
            loa = qq1 - (1.5 * ((math.e ** (-4 * medad)) * IQR))
            uoa = qq3 + (1.5 * ((math.e ** (3 * medad)) * IQR))
        if medad <= 0:
            loa = qq1 - (1.5 * ((math.e ** (-3 * medad)) * IQR))
            uoa = qq3 + (1.5 * ((math.e ** (4 * medad)) * IQR))
        if medad == 0:
            loa = qq1 - (1.5 * IQR)
            uoa = qq3 + (1.5 * IQR)

    raw = data

    data_clean = [x for x in raw if x < uoa and x > loa]
    outlier = [x for x in raw if x > uoa or x < loa]
    return data_clean, loa, uoa, outlier


def stats(data):

    avg = np.mean(data)
    qq1 = np.percentile(data, 25)
    med = np.median(data)
    qq3 = np.percentile(data, 75)
    std = np.std(data)

    return avg, qq1, med, qq3, std


def area(data, type ='other'):
    #calculates areas

    if type == 'time':
        u_1 = stats(data)[0] + stats(data)[4]
        u_2 = stats(data)[0] + (2 * stats(data)[4])
        u_3 = stats(data)[0] + (3 * stats(data)[4])

        d_1 = stats(data)[0] - stats(data)[4]
        if d_1 < 0 :
            d_1 = 0
        d_2 = stats(data)[0] - (2 * stats(data)[4])
        if d_2 < 0 :
            d_2 = 0
        d_3 = stats(data)[0] - (3 * stats(data)[4])
        if d_3 < 0 :
            d_3 = 0

    else:
        u_1 = stats(data)[0] + stats(data)[4]
        u_2 = stats(data)[0] + (2 * stats(data)[4])
        u_3 = stats(data)[0] + (3 * stats(data)[4])
        d_1 = stats(data)[0] - stats(data)[4]
        d_2 = stats(data)[0] - (2 * stats(data)[4])
        d_3 = stats(data)[0] - (3 * stats(data)[4])

    return  u_1, u_2, u_3 , d_1, d_2, d_3


def find_area(data, point, ddtype ='other'):
    #defines area of each point

    u_1, u_2, u_3, d_1, d_2, d_3 = area(data, type = ddtype)
    areak = 'NON'

    if point < u_3 and point > u_2:
        areak = 'u3'
    if point < u_2 and point > u_1:
        areak = 'u2'
    if point < u_1 and point > stats(data)[0]:
        areak = 'u1'
    if point < stats(data)[0] and point > u_1:
        areak = 'd1'
    if point < u_1 and point > u_2:
        areak = 'd2'
    if point < u_2 and point > u_3:
        areak = 'd3'

    return areak


def weco_1(data):
    #The most recent point plots outside one of the 3-sigma control limits.
    # If a point lies outside either of these limits, there is only a 0.3%
    # chance that this was caused by the normal process.

    u_1, u_2, u_3, d_1, d_2, d_3 = area(data, type='time')
    no_weco_1 = []
    indexak = 0
    for i in data:
        if i < d_3 or i > u_3:
            no_weco_1.append(indexak)
        indexak+=1
    return no_weco_1


def weco_2(data):
    #Two of the three most recent points plot outside and on the same side
    # as one of the 2-sigma control limits.

    u_1, u_2, u_3, d_1, d_2, d_3 = area(data, type='time')
    no_weco_2 = []
    poss_range = np.arange(2,len(data),1)
    #weco_2 should look at a range of 3 >> poss_range
    for i in poss_range:
        rangek = np.arange(i-2, i + 1, 1)
        tempak = []
        for j in rangek:
            if data[j] > u_2:
                tempak.append('u')
            if data[j] < d_2:
                tempak.append('d')
        if tempak.count('u') >= 2 or tempak.count('d') >= 2:
            no_weco_2.append(i)

    return no_weco_2


def weco_3(data):
    #Four of the five most recent points plot outside and on the same side
    # as one of the 1-sigma control limits
    u_1, u_2, u_3, d_1, d_2, d_3 = area(data, type='time')
    no_weco_3 = []
    poss_range = np.arange(4, len(data), 1)
    # weco_3 should look at a range of 5 >> poss_range
    for i in poss_range:
        rangek = np.arange(i - 4, i + 1, 1)
        tempak = []
        for j in rangek:
            if data[j] > u_1:
                tempak.append('u')
            if data[j] < d_1:
                tempak.append('d')

        if tempak.count('u') >= 4 or tempak.count('d') >= 4:
            no_weco_3.append(i)

    return no_weco_3


def weco_4(data):
    #Eight out of the last eight points plot on the same side of the center
    #line, or target value.
    no_weco_4 = []
    poss_range = np.arange(7, len(data), 1)
    # weco_4 should look at a range of 8 >> poss_range
    avg = stats(data)[0]
    for i in poss_range:
        rangek = np.arange(i - 7, i + 1, 1)
        tempak = []
        for j in rangek:
            if data[j] > avg:
                tempak.append('u')
            if data[j] < avg:
                tempak.append('d')
        if tempak.count('u') == 8 or tempak.count('d') == 8:
            no_weco_4.append(i)

    return no_weco_4


def weco_5(data):
    #Six points in a row increasing or decreasing.
    no_weco_5 = []
    poss_range = np.arange(5, len(data), 1)
    # weco_5 should look at a range of 6 >> poss_range forces the code
    #to ignore the first 5 points ad start from 6th point
    for i in poss_range:
        rangek = np.arange(i - 5, i + 1, 1)
        tempak = []
        a = 0
        for j in rangek:
            if a != 0:
                if data[j] < data[j-1]:
                    tempak.append('l')
                else:
                    tempak.append('h')
            a+=1
        if tempak.count('l') == 6 or tempak.count('h') == 6:
            no_weco_5.append(i)

    return no_weco_5


def weco_6(data):
    #Fifteen points in a row within one sigma
    u_1, u_2, u_3, d_1, d_2, d_3 = area(data, type='time')
    no_weco_6 = []
    poss_range = np.arange(14, len(data), 1)

    for i in poss_range:
        rangek = np.arange(i - 14, i + 1, 1)
        tempak = []
        for j in rangek:
            if data[j] > d_1 and data[j] < u_1:
                tempak.append('T')
        if tempak.count('T') == 15 :
            no_weco_6.append(i)

    return no_weco_6


def weco_7(data):
    #Fourteen points in a row alternating direction
    no_weco_7 = []
    poss_range = np.arange(13, len(data), 1)

    for i in poss_range:
        rangek = np.arange(i - 14, i + 1, 1)
        tempak = []
        a = 0
        for j in rangek:
            if a != 0:
                if data[j] < data[j-1]:
                    tempak.append('l')
                else:
                    tempak.append('h')
            a+=1
        alt_1 = ['l','h','l','h','l','h','l','h','l','h','l','h','l']
        alt_2 = ['h','l', 'h','l','h','l','h','l','h','l','h','l','h']
        if tempak == alt_1 or tempak == alt_2:
            no_weco_7.append(i)

    return no_weco_7


def weco_8(data):
    #Eight points in a row outside one sigma.
    u_1, u_2, u_3, d_1, d_2, d_3 = area(data, type='time')
    no_weco_8 = []
    poss_range = np.arange(7, len(data), 1)
    # weco_3 should look at a range of 5 >> poss_range
    for i in poss_range:
        rangek = np.arange(i - 7, i + 1, 1)
        tempak = []
        for j in rangek:
            if data[j] > u_1 or data[j] < d_1:
                tempak.append('T')

        if tempak.count('T') == 8 :
            no_weco_8.append(i)

    return no_weco_8


def weco_rules(data):
    w1 = weco_1(data)
    w2 = weco_2(data)
    w3 = weco_3(data)
    w4 = weco_4(data)
    w5 = weco_5(data)
    w6 = weco_6(data)
    w7 = weco_7(data)
    w8 = weco_8(data)

    w_list =[w1, w2, w3, w4, w5, w6, w7, w8]
    total_weco = []
    for i in w_list:
        for j in i:
            if j not in total_weco:
                total_weco.append(j)
    return sorted(total_weco)


def nelson_1(data):
    # The most recent point plots outside one of the 3-sigma control limits.
    # If a point lies outside either of these limits, there is only a 0.3%
    # chance that this was caused by the normal process.

    u_1, u_2, u_3, d_1, d_2, d_3 = area(data, type='time')
    no_nelson_1 = []
    indexak = 0
    for i in data:
        if i < d_3 or i > u_3:
            no_nelson_1.append(indexak)
        indexak += 1
    return no_nelson_1


def nelson_2(data):
    # Two of the three most recent points plot outside and on the same side
    # as one of the 2-sigma control limits.

    u_1, u_2, u_3, d_1, d_2, d_3 = area(data, type='time')
    no_nelson_2 = []
    poss_range = np.arange(2, len(data), 1)
    # nelson_2 should look at a range of 3 >> poss_range
    for i in poss_range:
        rangek = np.arange(i - 2, i + 1, 1)
        tempak = []
        for j in rangek:
            if data[j] > u_2:
                tempak.append('u')
            if data[j] < d_2:
                tempak.append('d')
        if tempak.count('u') >= 2 or tempak.count('d') >= 2:
            no_nelson_2.append(i)

    return no_nelson_2


def nelson_3(data):
    # Four of the five most recent points plot outside and on the same side
    # as one of the 1-sigma control limits
    u_1, u_2, u_3, d_1, d_2, d_3 = area(data, type='time')
    no_nelson_3 = []
    poss_range = np.arange(4, len(data), 1)
    # weco_3 should look at a range of 5 >> poss_range
    for i in poss_range:
        rangek = np.arange(i - 4, i + 1, 1)
        tempak = []
        for j in rangek:
            if data[j] > u_1:
                tempak.append('u')
            if data[j] < d_1:
                tempak.append('d')

        if tempak.count('u') >= 4 or tempak.count('d') >= 4:
            no_nelson_3.append(i)

    return no_nelson_3


def nelson_4(data):
    # Nine out of the last nine points plot on the same side of the center
    # line, or target value.
    no_nelson_4 = []
    poss_range = np.arange(8, len(data), 1)
    # weco_4 should look at a range of 8 >> poss_range
    avg = stats(data)[0]
    for i in poss_range:
        rangek = np.arange(i - 8, i + 1, 1)
        tempak = []
        for j in rangek:
            if data[j] > avg:
                tempak.append('u')
            if data[j] < avg:
                tempak.append('d')
        if tempak.count('u') == 9 or tempak.count('d') == 9:
            no_nelson_4.append(i)

    return no_nelson_4


def nelson_5(data):
    #Six points in a row increasing or decreasing.
    no_nelson_5 = []
    poss_range = np.arange(5, len(data), 1)
    # nelson_5 should look at a range of 6 >> poss_range forces the code
    #to ignore the first 5 points ad start from 6th point
    for i in poss_range:
        rangek = np.arange(i - 5, i + 1, 1)
        tempak = []
        a = 0
        for j in rangek:
            if a != 0:
                if data[j] < data[j-1]:
                    tempak.append('l')
                else:
                    tempak.append('h')
            a+=1
        if tempak.count('l') == 5 or tempak.count('h') ==5:
            no_nelson_5.append(i)

    return no_nelson_5


def nelson_6(data):
    #Fifteen points in a row within one sigma
    u_1, u_2, u_3, d_1, d_2, d_3 = area(data, type='time')
    no_nelson_6 = []
    poss_range = np.arange(14, len(data), 1)

    for i in poss_range:
        rangek = np.arange(i - 14, i + 1, 1)
        tempak = []
        for j in rangek:
            if data[j] > d_1 and data[j] < u_1:
                tempak.append('T')
        if tempak.count('T') == 15 :
            no_nelson_6.append(i)

    return no_nelson_6


def nelson_7(data):
    #Fourteen points in a row alternating direction
    no_nelson_7 = []
    poss_range = np.arange(13, len(data), 1)

    for i in poss_range:
        rangek = np.arange(i - 14, i + 1, 1)
        tempak = []
        a = 0
        for j in rangek:
            if a != 0:
                if data[j] < data[j-1]:
                    tempak.append('l')
                else:
                    tempak.append('h')
            a+=1
        alt_1 = ['l','h','l','h','l','h','l','h','l','h','l','h','l']
        alt_2 = ['h','l', 'h','l','h','l','h','l','h','l','h','l','h']
        if tempak == alt_1 or tempak == alt_2:
            no_nelson_7.append(i)

    return no_nelson_7


def nelson_8(data):
    #Eight points in a row outside one sigma.
    u_1, u_2, u_3, d_1, d_2, d_3 = area(data, type='time')
    no_nelson_8 = []
    poss_range = np.arange(7, len(data), 1)
    # nelson_8 should look at a range of 5 >> poss_range
    for i in poss_range:
        rangek = np.arange(i - 7, i + 1, 1)
        tempak = []
        for j in rangek:
            if data[j] > u_1 or data[j] < d_1:
                tempak.append('T')

        if tempak.count('T') == 8 :
            no_nelson_8.append(i)

    return no_nelson_8


def nelson_rules(data):
    n1 = nelson_1(data)
    n2 = nelson_2(data)
    n3 = nelson_3(data)
    n4 = nelson_4(data)
    n5 = nelson_5(data)
    n6 = nelson_6(data)
    n7 = nelson_7(data)
    n8 = nelson_8(data)

    n_list =[n1, n2, n3, n4, n5, n6, n7, n8]
    total_nelson = []
    for i in n_list:
        for j in i:
            if j not in total_nelson:
                total_nelson.append(j)
    return sorted(total_nelson)


def aiag_1(data):
    # One of one point is outside of +-3-sigma control limits

    u_1, u_2, u_3, d_1, d_2, d_3 = area(data, type='time')
    no_aiag_1 = []
    indexak = 0
    for i in data:
        if i < d_3 or i > u_3:
            no_aiag_1.append(indexak)
        indexak += 1
    return no_aiag_1


def aiag_2(data):
    #Seven out of seven are above or below center line
    no_aiag_2 = []
    poss_range = np.arange(6, len(data), 1)
    # aiag_2 should look at a range of 8 >> poss_range
    avg = stats(data)[0]
    for i in poss_range:
        rangek = np.arange(i - 6, i + 1, 1)
        tempak = []
        for j in rangek:
            if data[j] > avg:
                tempak.append('u')
            if data[j] < avg:
                tempak.append('d')
        if tempak.count('u') == 7 or tempak.count('d') == 7:
            no_aiag_2.append(i)

    return no_aiag_2


def aiag_3(data):
    #Seven points in a row increasing
    no_aiag_3 = []
    poss_range = np.arange(6, len(data), 1)
    # aiag_3 should look at a range of 6 >> poss_range forces the code
    # to ignore the first 5 points ad start from 6th point
    for i in poss_range:
        rangek = np.arange(i - 6, i + 1, 1)
        tempak = []
        a = 0
        for j in rangek:
            if a != 0:
                if data[j] > data[j - 1]:
                    tempak.append('h')

            a += 1
        if tempak.count('h') == 7:
            no_aiag_3.append(i)

    return no_aiag_3


def aiag_4(data):
    # Seven points in a row decreasing
    no_aiag_4 = []
    poss_range = np.arange(6, len(data), 1)
    # aiag_4 should look at a range of 6 >> poss_range forces the code
    # to ignore the first 5 points ad start from 6th point
    for i in poss_range:
        rangek = np.arange(i - 6, i + 1, 1)
        tempak = []
        a = 0
        for j in rangek:
            if a != 0:
                if data[j] < data[j - 1]:
                    tempak.append('l')

            a += 1
        if tempak.count('l') == 7:
            no_aiag_4.append(i)

    return no_aiag_4


def aiag_rules(data):
    a1 = aiag_1(data)
    a2 = aiag_2(data)
    a3 = aiag_3(data)
    a4 = aiag_4(data)


    a_list =[a1, a2, a3, a4]
    total_aiag = []
    for i in a_list:
        for j in i:
            if j not in total_aiag:
                total_aiag.append(j)
    return sorted(total_aiag)


def juran_1(data):
    #One of one point is outside of +- 3-sigma control limits
    u_1, u_2, u_3, d_1, d_2, d_3 = area(data, type='time')
    no_juran_1 = []
    indexak = 0
    for i in data:
        if i < d_3 or i > u_3:
            no_juran_1.append(indexak)
        indexak += 1
    return no_juran_1


def juran_2(data):
    #Two of three points above 2-sigma control limits
    u_1, u_2, u_3, d_1, d_2, d_3 = area(data, type='time')
    no_juran_2 = []
    poss_range = np.arange(2, len(data), 1)
    # juran_2 should look at a range of 3 >> poss_range
    for i in poss_range:
        rangek = np.arange(i - 2, i + 1, 1)
        tempak = []
        for j in rangek:
            if data[j] > u_2:
                tempak.append('T')

        if tempak.count('T') >= 2 :
            no_juran_2.append(i)

    return no_juran_2


def juran_3(data):
    #Two of three points below -2-sigma control limits
    u_1, u_2, u_3, d_1, d_2, d_3 = area(data, type='time')
    no_juran_3 = []
    poss_range = np.arange(2, len(data), 1)
    # juran_3 should look at a range of 3 >> poss_range
    for i in poss_range:
        rangek = np.arange(i - 2, i + 1, 1)
        tempak = []
        for j in rangek:
            if data[j] < d_2:
                tempak.append('T')

        if tempak.count('T') >= 2:
            no_juran_3.append(i)

    return no_juran_3


def juran_4(data):
    #Four of five points is above 1-sigma control limits
    u_1, u_2, u_3, d_1, d_2, d_3 = area(data, type='time')
    no_juran_4 = []
    poss_range = np.arange(4, len(data), 1)
    # juran_4 should look at a range of 5 >> poss_range
    for i in poss_range:
        rangek = np.arange(i - 4, i + 1, 1)
        tempak = []
        for j in rangek:
            if data[j] > u_1:
                tempak.append('T')

        if tempak.count('T') >= 4 :
            no_juran_4.append(i)

    return no_juran_4


def juran_5(data):
    #Four of five points is above -1-sigma control limits
    u_1, u_2, u_3, d_1, d_2, d_3 = area(data, type='time')
    no_juran_5 = []
    poss_range = np.arange(4, len(data), 1)
    # juran_5 should look at a range of 5 >> poss_range
    for i in poss_range:
        rangek = np.arange(i - 4, i + 1, 1)
        tempak = []
        for j in rangek:
            if data[j] < d_1:
                tempak.append('T')

        if tempak.count('T') >= 4 :
            no_juran_5.append(i)

    return no_juran_5


def juran_6(data):
    #Six points in a row increasing
    no_juran_6 = []
    poss_range = np.arange(5, len(data), 1)
    # juran_6 should look at a range of 6 >> poss_range forces the code
    # to ignore the first 5 points ad start from 6th point
    for i in poss_range:
        rangek = np.arange(i - 5, i + 1, 1)
        tempak = []
        a = 0
        for j in rangek:
            if a != 0:
                if data[j] > data[j - 1]:
                    tempak.append('h')

            a += 1
        if tempak.count('h') == 6:
            no_juran_6.append(i)

    return no_juran_6


def juran_7(data):
    #Six points in a row decreasing
    no_juran_7 = []
    poss_range = np.arange(5, len(data), 1)
    # juran_7 should look at a range of 6 >> poss_range forces the code
    # to ignore the first 5 points ad start from 6th point
    for i in poss_range:
        rangek = np.arange(i - 5, i + 1, 1)
        tempak = []
        a = 0
        for j in rangek:
            if a != 0:
                if data[j] < data[j - 1]:
                    tempak.append('l')

            a += 1
        if tempak.count('l') == 6:
            no_juran_7.append(i)

    return no_juran_7


def juran_8(data):
    # Nine out of the last nine points plot on the same side of the center
    # line, or target value.
    no_juran_8= []
    poss_range = np.arange(8, len(data), 1)
    # juran_8 should look at a range of 8 >> poss_range
    avg = stats(data)[0]
    for i in poss_range:
        rangek = np.arange(i - 8, i + 1, 1)
        tempak = []
        for j in rangek:
            if data[j] > avg:
                tempak.append('u')
            if data[j] < avg:
                tempak.append('d')
        if tempak.count('u') == 9 or tempak.count('d') == 9:
            no_juran_8.append(i)

    return no_juran_8


def juran_9(data):
    # Eight points in a row on both sides of center line, none in zone C
    u_1, u_2, u_3, d_1, d_2, d_3 = area(data, type='time')
    no_juran_9 = []
    poss_range = np.arange(7, len(data), 1)
    # juran_9 should look at a range of 8 >> poss_range
    avg = stats(data)[0]
    for i in poss_range:
        rangek = np.arange(i - 7, i + 1, 1)
        tempak = []
        for j in rangek:
            if data[j] > u_2 or data[j] < d_2:
                tempak.append('T')

        if tempak.count('T') == 8 :
            no_juran_9.append(i)

    return no_juran_9


def juran_rules(data):
    j1 = juran_1(data)
    j2 = juran_2(data)
    j3 = juran_3(data)
    j4 = juran_4(data)
    j5 = juran_5(data)
    j6 = juran_6(data)
    j7 = juran_7(data)
    j8 = juran_8(data)
    j9 = juran_9(data)


    j_list =[j1, j2, j3, j4, j5, j6, j7, j8, j9]
    total_juran = []
    for i in j_list:
        for j in i:
            if j not in total_juran:
                total_juran.append(j)
    return sorted(total_juran)


def hughes_1(data):
    #One of one point is outside of +- 3-sigma control limits
    u_1, u_2, u_3, d_1, d_2, d_3 = area(data, type='time')
    no_hughes_1 = []
    indexak = 0
    for i in data:
        if i < d_3 or i > u_3:
            no_hughes_1.append(indexak)
        indexak += 1
    return no_hughes_1


def hughes_2(data):
    #Two of three points above 2-sigma control limits
    u_1, u_2, u_3, d_1, d_2, d_3 = area(data, type='time')
    no_hughes_2 = []
    poss_range = np.arange(2, len(data), 1)
    # hughes_2 should look at a range of 3 >> poss_range
    for i in poss_range:
        rangek = np.arange(i - 2, i + 1, 1)
        tempak = []
        for j in rangek:
            if data[j] > u_2:
                tempak.append('T')

        if tempak.count('T') >= 2 :
            no_hughes_2.append(i)

    return no_hughes_2


def hughes_3(data):
    #Two of three points below -2-sigma control limits
    u_1, u_2, u_3, d_1, d_2, d_3 = area(data, type='time')
    no_hughes_3 = []
    poss_range = np.arange(2, len(data), 1)
    # hughes_3 should look at a range of 3 >> poss_range
    for i in poss_range:
        rangek = np.arange(i - 2, i + 1, 1)
        tempak = []
        for j in rangek:
            if data[j] < d_2:
                tempak.append('T')

        if tempak.count('T') >= 2:
            no_hughes_3.append(i)

    return no_hughes_3


def hughes_4(data):
    #Three of seven points above 2-sigma control limits
    u_1, u_2, u_3, d_1, d_2, d_3 = area(data, type='time')
    no_hughes_4 = []
    poss_range = np.arange(6, len(data), 1)
    # hughes_4 should look at a range of 7 >> poss_range
    for i in poss_range:
        rangek = np.arange(i - 6, i + 1, 1)
        tempak = []
        for j in rangek:
            if data[j] > u_2:
                tempak.append('T')

        if tempak.count('T') >= 3:
            no_hughes_4.append(i)

    return no_hughes_4


def hughes_5(data):
    #Three of seven points below -2-sigma control limits
    u_1, u_2, u_3, d_1, d_2, d_3 = area(data, type='time')
    no_hughes_5 = []
    poss_range = np.arange(6, len(data), 1)
    # hughes_5 should look at a range of 7 >> poss_range
    for i in poss_range:
        rangek = np.arange(i - 6, i + 1, 1)
        tempak = []
        for j in rangek:
            if data[j] < d_2:
                tempak.append('T')

        if tempak.count('T') >= 3:
            no_hughes_5.append(i)

    return no_hughes_5


def hughes_6(data):
    #Four of ten points above 2-sigma control limits
    u_1, u_2, u_3, d_1, d_2, d_3 = area(data, type='time')
    no_hughes_6 = []
    poss_range = np.arange(9, len(data), 1)
    # hughes_6 should look at a range of 10 >> poss_range
    for i in poss_range:
        rangek = np.arange(i - 9, i + 1, 1)
        tempak = []
        for j in rangek:
            if data[j] > u_2:
                tempak.append('T')

        if tempak.count('T') >= 4:
            no_hughes_6.append(i)

    return no_hughes_6


def hughes_7(data):
    #Four of ten points below -2-sigma control limits
    u_1, u_2, u_3, d_1, d_2, d_3 = area(data, type='time')
    no_hughes_7 = []
    poss_range = np.arange(9, len(data), 1)
    # hughes_7 should look at a range of 10 >> poss_range
    for i in poss_range:
        rangek = np.arange(i - 9, i + 1, 1)
        tempak = []
        for j in rangek:
            if data[j] < d_2:
                tempak.append('T')

        if tempak.count('T') >= 4:
            no_hughes_7.append(i)

    return no_hughes_7


def hughes_8(data):
    #Four of five points is above 1-sigma control limits
    u_1, u_2, u_3, d_1, d_2, d_3 = area(data, type='time')
    no_hughes_8 = []
    poss_range = np.arange(4, len(data), 1)
    # hughes_8 should look at a range of 5 >> poss_range
    for i in poss_range:
        rangek = np.arange(i - 4, i + 1, 1)
        tempak = []
        for j in rangek:
            if data[j] > u_1:
                tempak.append('T')

        if tempak.count('T') >= 4:
            no_hughes_8.append(i)

    return no_hughes_8


def hughes_9(data):
    #Four of five points is below -1-sigma control limits
    u_1, u_2, u_3, d_1, d_2, d_3 = area(data, type='time')
    no_hughes_9 = []
    poss_range = np.arange(4, len(data), 1)
    # hughes_9 should look at a range of 5 >> poss_range
    for i in poss_range:
        rangek = np.arange(i - 4, i + 1, 1)
        tempak = []
        for j in rangek:
            if data[j] < d_1:
                tempak.append('T')

        if tempak.count('T') >= 4:
            no_hughes_9.append(i)

    return no_hughes_9


def hughes_10(data):
    #Seven points in a row increasing
    no_hughes_10 = []
    poss_range = np.arange(6, len(data), 1)
    # hughes_10 should look at a range of 6 >> poss_range forces the code
    # to ignore the first 7 points and start from 6th point
    for i in poss_range:
        rangek = np.arange(i - 6, i + 1, 1)
        tempak = []
        a = 0
        for j in rangek:
            if a != 0:
                if data[j] > data[j - 1]:
                    tempak.append('h')

            a += 1
        if tempak.count('h') == 7:
            no_hughes_10.append(i)

    return no_hughes_10


def hughes_11(data):
    #Seven points in a row decreasing
    no_hughes_11 = []
    poss_range = np.arange(6, len(data), 1)
    # hughes_11 should look at a range of 6 >> poss_range forces the code
    # to ignore the first 7 points and start from 6th point
    for i in poss_range:
        rangek = np.arange(i - 6, i + 1, 1)
        tempak = []
        a = 0
        for j in rangek:
            if a != 0:
                if data[j] < data[j - 1]:
                    tempak.append('l')

            a += 1
        if tempak.count('l') == 7:
            no_hughes_11.append(i)

    return no_hughes_11


def hughes_12(data):
    #Ten of eleven are above center line
    no_hughes_12 = []
    poss_range = np.arange(10, len(data), 1)
    # hughes_12 should look at a range of 8 >> poss_range
    avg = stats(data)[0]
    for i in poss_range:
        rangek = np.arange(i - 10, i + 1, 1)
        tempak = []
        for j in rangek:
            if data[j] > avg:
                tempak.append('T')

        if tempak.count('T') == 10:
            no_hughes_12.append(i)

    return no_hughes_12


def hughes_13(data):
    #Ten of eleven are below center line
    no_hughes_13 = []
    poss_range = np.arange(10, len(data), 1)
    # hughes_13 should look at a range of 8 >> poss_range
    avg = stats(data)[0]
    for i in poss_range:
        rangek = np.arange(i - 10, i + 1, 1)
        tempak = []
        for j in rangek:
            if data[j] < avg:
                tempak.append('T')

        if tempak.count('T') == 10:
            no_hughes_13.append(i)

    return no_hughes_13


def hughes_14(data):
    #Twelve of fourteen are above center line
    no_hughes_14 = []
    poss_range = np.arange(13, len(data), 1)
    # hughes_14 should look at a range of 8 >> poss_range
    avg = stats(data)[0]
    for i in poss_range:
        rangek = np.arange(i - 13, i + 1, 1)
        tempak = []
        for j in rangek:
            if data[j] > avg:
                tempak.append('T')

        if tempak.count('T') == 12:
            no_hughes_14.append(i)

    return no_hughes_14


def hughes_15(data):
    #Ten of eleven are below center line
    no_hughes_15 = []
    poss_range = np.arange(13, len(data), 1)
    # hughes_15 should look at a range of 8 >> poss_range
    avg = stats(data)[0]
    for i in poss_range:
        rangek = np.arange(i - 13, i + 1, 1)
        tempak = []
        for j in rangek:
            if data[j] < avg:
                tempak.append('T')

        if tempak.count('T') == 10:
            no_hughes_15.append(i)

    return no_hughes_15


def hughes_rules(data):
    h1 = hughes_1(data)
    h2 = hughes_2(data)
    h3 = hughes_3(data)
    h4 = hughes_4(data)
    h5 = hughes_5(data)
    h6 = hughes_6(data)
    h7 = hughes_7(data)
    h8 = hughes_8(data)
    h9 = hughes_9(data)
    h10 = hughes_10(data)
    h11 = hughes_11(data)
    h12 = hughes_12(data)
    h13 = hughes_13(data)
    h14 = hughes_14(data)
    h15 = hughes_15(data)

    h_list =[h1, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11, h12, h13, h14, h15]
    total_hughes = []
    for i in h_list:
        for j in i:
            if j not in total_hughes:
                total_hughes.append(j)
    return sorted(total_hughes)


def gitlow_1(data):
    #One of one point is outside of +- 3-sigma control limits
    u_1, u_2, u_3, d_1, d_2, d_3 = area(data, type='time')
    no_gitlow_1 = []
    indexak = 0
    for i in data:
        if i < d_3 or i > u_3:
            no_gitlow_1.append(indexak)
        indexak += 1
    return no_gitlow_1


def gitlow_2(data):
    #Two of three points above 2-sigma control limits
    u_1, u_2, u_3, d_1, d_2, d_3 = area(data, type='time')
    no_gitlow_2 = []
    poss_range = np.arange(2, len(data), 1)
    # gitlow_2 should look at a range of 3 >> poss_range
    for i in poss_range:
        rangek = np.arange(i - 2, i + 1, 1)
        tempak = []
        for j in rangek:
            if data[j] > u_2:
                tempak.append('T')

        if tempak.count('T') >= 2 :
            no_gitlow_2.append(i)

    return no_gitlow_2


def gitlow_3(data):
    #Two of three points below -2-sigma control limits
    u_1, u_2, u_3, d_1, d_2, d_3 = area(data, type='time')
    no_gitlow_3 = []
    poss_range = np.arange(2, len(data), 1)
    # gitlow_3 should look at a range of 3 >> poss_range
    for i in poss_range:
        rangek = np.arange(i - 2, i + 1, 1)
        tempak = []
        for j in rangek:
            if data[j] < d_2:
                tempak.append('T')

        if tempak.count('T') >= 2:
            no_gitlow_3.append(i)

    return no_gitlow_3


def gitlow_4(data):
    #Four of five points is above 1-sigma control limits
    u_1, u_2, u_3, d_1, d_2, d_3 = area(data, type='time')
    no_gitlow_4 = []
    poss_range = np.arange(4, len(data), 1)
    # gitlow_4 should look at a range of 5 >> poss_range
    for i in poss_range:
        rangek = np.arange(i - 4, i + 1, 1)
        tempak = []
        for j in rangek:
            if data[j] > u_1:
                tempak.append('T')

        if tempak.count('T') >= 4:
            no_gitlow_4.append(i)

    return no_gitlow_4


def gitlow_5(data):
    #Four of five points is below -1-sigma control limits
    u_1, u_2, u_3, d_1, d_2, d_3 = area(data, type='time')
    no_gitlow_5 = []
    poss_range = np.arange(4, len(data), 1)
    # gitlow_5 should look at a range of 5 >> poss_range
    for i in poss_range:
        rangek = np.arange(i - 4, i + 1, 1)
        tempak = []
        for j in rangek:
            if data[j] < d_1:
                tempak.append('T')

        if tempak.count('T') >= 4:
            no_gitlow_5.append(i)

    return no_gitlow_5


def gitlow_6(data):
    #Eight points in a row increasing
    no_gitlow_6 = []
    poss_range = np.arange(7, len(data), 1)

    for i in poss_range:
        rangek = np.arange(i - 7, i + 1, 1)
        tempak = []
        a = 0
        for j in rangek:
            if a != 0:
                if data[j] > data[j - 1]:
                    tempak.append('h')

            a += 1
        if tempak.count('h') == 8:
            no_gitlow_6.append(i)

    return no_gitlow_6


def gitlow_7(data):
    #Eight points in a row decreasing
    no_gitlow_7 = []
    poss_range = np.arange(7, len(data), 1)

    for i in poss_range:
        rangek = np.arange(i - 7, i + 1, 1)
        tempak = []
        a = 0
        for j in rangek:
            if a != 0:
                if data[j] < data[j - 1]:
                    tempak.append('l')

            a += 1
        if tempak.count('l') == 8:
            no_gitlow_7_.append(i)

    return no_gitlow_7


def gitlow_8(data):
    #Wight of Eight are above center line
    no_gitlow_8 = []
    poss_range = np.arange(7, len(data), 1)
    # gitlow_8 should look at a range of 8 >> poss_range
    avg = stats(data)[0]
    for i in poss_range:
        rangek = np.arange(i - 7, i + 1, 1)
        tempak = []
        for j in rangek:
            if data[j] > avg:
                tempak.append('T')

        if tempak.count('T') == 8:
            no_gitlow_8.append(i)

    return no_gitlow_8


def gitlow_9(data):
    #Eight of eight are below center line
    no_gitlow_9 = []
    poss_range = np.arange(7, len(data), 1)
    # gitlow_9 should look at a range of 8 >> poss_range
    avg = stats(data)[0]
    for i in poss_range:
        rangek = np.arange(i - 7, i + 1, 1)
        tempak = []
        for j in rangek:
            if data[j] < avg:
                tempak.append('T')

        if tempak.count('T') == 8:
            no_gitlow_9.append(i)

    return no_gitlow_9


def gitlow_rules(data):
    g1 = gitlow_1(data)
    g2 = gitlow_2(data)
    g3 = gitlow_3(data)
    g4 = gitlow_4(data)
    g5 = gitlow_5(data)
    g6 = gitlow_6(data)
    g7 = gitlow_7(data)
    g8 = gitlow_8(data)
    g9 = gitlow_9(data)


    g_list =[g1, g2, g3, g4, g5, g6, g7, g8, g9]
    total_gitlow = []
    for i in g_list:
        for j in i:
            if j not in total_gitlow:
                total_gitlow.append(j)
    return sorted(total_gitlow)


def duncan_1(data):
    # One of one point is outside of +- 3-sigma control limits
    u_1, u_2, u_3, d_1, d_2, d_3 = area(data, type='time')
    no_duncan_1 = []
    indexak = 0
    for i in data:
        if i < d_3 or i > u_3:
            no_duncan_1.append(indexak)
        indexak += 1
    return no_duncan_1


def duncan_2(data):
    #Two of three points above 2-sigma control limits
    u_1, u_2, u_3, d_1, d_2, d_3 = area(data, type='time')
    no_duncan_2 = []
    poss_range = np.arange(2, len(data), 1)
    # duncan_2 should look at a range of 3 >> poss_range
    for i in poss_range:
        rangek = np.arange(i - 2, i + 1, 1)
        tempak = []
        for j in rangek:
            if data[j] > u_2:
                tempak.append('T')

        if tempak.count('T') >= 2 :
            no_duncan_2.append(i)

    return no_duncan_2


def duncan_3(data):
    #Two of three points below -2-sigma control limits
    u_1, u_2, u_3, d_1, d_2, d_3 = area(data, type='time')
    no_duncan_3 = []
    poss_range = np.arange(2, len(data), 1)
    # duncan_3 should look at a range of 3 >> poss_range
    for i in poss_range:
        rangek = np.arange(i - 2, i + 1, 1)
        tempak = []
        for j in rangek:
            if data[j] < d_2:
                tempak.append('T')

        if tempak.count('T') >= 2:
            no_duncan_3.append(i)

    return no_duncan_3


def duncan_4(data):
    #Four of five points is above 1-sigma control limits
    u_1, u_2, u_3, d_1, d_2, d_3 = area(data, type='time')
    no_duncan_4 = []
    poss_range = np.arange(4, len(data), 1)
    # duncan_4 should look at a range of 5 >> poss_range
    for i in poss_range:
        rangek = np.arange(i - 4, i + 1, 1)
        tempak = []
        for j in rangek:
            if data[j] > u_1:
                tempak.append('T')

        if tempak.count('T') >= 4:
            no_duncan_4.append(i)

    return no_duncan_4


def duncan_5(data):
    #Four of five points is below -1-sigma control limits
    u_1, u_2, u_3, d_1, d_2, d_3 = area(data, type='time')
    no_duncan_5 = []
    poss_range = np.arange(4, len(data), 1)
    # duncan_5 should look at a range of 5 >> poss_range
    for i in poss_range:
        rangek = np.arange(i - 4, i + 1, 1)
        tempak = []
        for j in rangek:
            if data[j] < d_1:
                tempak.append('T')

        if tempak.count('T') >= 4:
            no_duncan_5.append(i)

    return no_duncan_5


def duncan_6(data):
    #Seven points in a row increasing
    no_duncan_6 = []
    poss_range = np.arange(6, len(data), 1)

    for i in poss_range:
        rangek = np.arange(i - 6, i + 1, 1)
        tempak = []
        a = 0
        for j in rangek:
            if a != 0:
                if data[j] > data[j - 1]:
                    tempak.append('h')

            a += 1
        if tempak.count('h') == 7:
            no_duncan_6.append(i)

    return no_duncan_6


def duncan_7(data):
    #Seven points in a row decreasing
    no_duncan_7 = []
    poss_range = np.arange(6, len(data), 1)

    for i in poss_range:
        rangek = np.arange(i - 6, i + 1, 1)
        tempak = []
        a = 0
        for j in rangek:
            if a != 0:
                if data[j] < data[j - 1]:
                    tempak.append('l')

            a += 1
        if tempak.count('l') == 7:
            no_duncan_7.append(i)

    return no_duncan_7


def duncan_rules(data):
    d1 = duncan_1(data)
    d2 = duncan_2(data)
    d3 = duncan_3(data)
    d4 = duncan_4(data)
    d5 = duncan_5(data)
    d6 = duncan_6(data)
    d7 = duncan_7(data)



    d_list =[d1, d2, d3, d4, d5, d6, d7]
    total_duncan = []
    for i in d_list:
        for j in i:
            if j not in total_duncan:
                total_duncan.append(j)
    return sorted(total_duncan)


def westgard_1(data):
    #One of one point is outside of +- 3-sigma control limits
    u_1, u_2, u_3, d_1, d_2, d_3 = area(data, type='time')
    no_westgard_1 = []
    indexak = 0
    for i in data:
        if i < d_3 or i > u_3:
            no_westgard_1.append(indexak)
        indexak += 1
    return no_westgard_1


def westgard_2(data):
    #Two of two points outside +-2-sigma control limits
    #change
    u_1, u_2, u_3, d_1, d_2, d_3 = area(data, type='time')
    no_westgard_2 = []
    poss_range = np.arange(1, len(data), 1)
    # westgard_2 should look at a range of 3 >> poss_range
    for i in poss_range:
        rangek = np.arange(i - 1, i + 1, 1)
        tempak = []
        for j in rangek:
            if data[j] > u_2:
                tempak.append('T')
            if data[j] < d_2:
                tempak.append('T')
        if tempak.count('T') >= 2 :
            no_westgard_2.append(i)

    return no_westgard_2


def westgard_3(data):
    #Four of four points outside +-1-sigma control limits
    u_1, u_2, u_3, d_1, d_2, d_3 = area(data, type='time')
    no_westgard_3 = []
    poss_range = np.arange(3, len(data), 1)
    # westgard_3 should look at a range of 5 >> poss_range
    for i in poss_range:
        rangek = np.arange(i - 3, i + 1, 1)
        tempak = []
        for j in rangek:
            if data[j] > u_1:
                tempak.append('T')
            if data[j] < d_1:
                tempak.append('T')

        if tempak.count('T') >= 4 :
            no_westgard_3.append(i)

    return no_westgard_3


def westgard_4(data):
    #Ten of ten points on one side of center line
    no_westgard_4 = []
    poss_range = np.arange(9, len(data), 1)
    # westgard_4 should look at a range of 8 >> poss_range
    avg = stats(data)[0]
    for i in poss_range:
        rangek = np.arange(i - 9, i + 1, 1)
        tempak = []
        for j in rangek:
            if data[j] < avg:
                tempak.append('l')
            if data[j] > avg:
                tempak.append('h')

        if tempak.count('l') == 10 or tempak.count('h') == 10:
            no_westgard_4.append(i)

    return no_westgard_4


def westgard_5(data):
    #Two adjacent points on opposite sides of +-2-sigma
    u_1, u_2, u_3, d_1, d_2, d_3 = area(data, type='time')
    no_westgard_5 = []
    poss_range = np.arange(1, len(data), 1)
    # westgard_5 should look at a range of 2 >> poss_range
    for i in poss_range:
        rangek = np.arange(i - 1, i + 1, 1)
        tempak = []
        for j in rangek:
            if data[j] > u_2:
                tempak.append('h')
            if data[j] < d_2:
                tempak.append('l')
        if tempak.count('h') + tempak.count('l') == 2:
            no_westgard_5.append(i)

    return no_westgard_5


def westgard_6(data):
    #Seven of seven points in a trend increasing or decreasing
    no_westgard_6 = []
    poss_range = np.arange(6, len(data), 1)
    # westgard_6 should look at a range of 7 >> poss_range forces the code
    # to ignore the first 6 points ad start from 6th point
    for i in poss_range:
        rangek = np.arange(i - 6, i + 1, 1)
        tempak = []
        a = 0
        for j in rangek:
            if a != 0:
                if data[j] < data[j - 1]:
                    tempak.append('l')
                else:
                    tempak.append('h')
            a += 1
        if tempak.count('l') == 7 or tempak.count('h') == 7:
            no_westgard_6.append(i)

    return no_westgard_6


def westgard_7(data):
    #One of one point is outside of +- 2-sigma control limits
    u_1, u_2, u_3, d_1, d_2, d_3 = area(data, type='time')
    no_westgrad_7 = []
    for i in range(len(data)):
        if data[i] < d_2 or data[i] > u_2:
            no_westgrad_7.append(i)
    return no_westgrad_7


def westgard_8(data):
    #Two of three points outside +-2-sigma control limits
    u_1, u_2, u_3, d_1, d_2, d_3 = area(data, type='time')
    no_westgard_8 = []
    poss_range = np.arange(2, len(data), 1)
    # westgard_8 should look at a range of 3 >> poss_range
    for i in poss_range:
        rangek = np.arange(i - 2, i + 1, 1)
        tempak = []
        for j in rangek:
            if data[j] > u_2:
                tempak.append('T')
            if data[j] < d_2:
                tempak.append('T')
        if tempak.count('T') >= 2:
            no_westgard_8.append(i)

    return no_westgard_8


def westgard_9(data):
    #Three of three points outside +-1-sigma control limits
    u_1, u_2, u_3, d_1, d_2, d_3 = area(data, type='time')
    no_westgard_9 = []
    poss_range = np.arange(2, len(data), 1)
    # westgard_9 should look at a range of 5 >> poss_range
    for i in poss_range:
        rangek = np.arange(i - 2, i + 1, 1)
        tempak = []
        for j in rangek:
            if data[j] > u_1:
                tempak.append('T')
            if data[j] < d_1:
                tempak.append('T')

        if tempak.count('T') >= 3 :
            no_westgard_9.append(i)

    return no_westgard_9


def westgard_10(data):
    #Six of six points on one side of center line
    no_westgard_10 = []
    poss_range = np.arange(5, len(data), 1)
    # westgard_10 should look at a range of 8 >> poss_range
    avg = stats(data)[0]
    for i in poss_range:
        rangek = np.arange(i - 5, i + 1, 1)
        tempak = []
        for j in rangek:
            if data[j] > avg:
                tempak.append('u')
            if data[j] < avg:
                tempak.append('d')
        if tempak.count('u') == 6 or tempak.count('d') == 6:
            no_westgard_10.append(i)

    return no_westgard_10


def westgard_11(data):
    #Eight of eight points on one side of center line
    no_westgard_11 = []
    poss_range = np.arange(7, len(data), 1)
    # westgard_11 should look at a range of 8 >> poss_range
    avg = stats(data)[0]
    for i in poss_range:
        rangek = np.arange(i - 7, i + 1, 1)
        tempak = []
        for j in rangek:
            if data[j] > avg:
                tempak.append('u')
            if data[j] < avg:
                tempak.append('d')
        if tempak.count('u') == 8 or tempak.count('d') == 8:
            no_westgard_11.append(i)

    return no_westgard_11


def westgard_12(data):
    #Nine of nine points on one side of center line
    no_westgard_12 = []
    poss_range = np.arange(8, len(data), 1)
    # westgard_12 should look at a range of 8 >> poss_range
    avg = stats(data)[0]
    for i in poss_range:
        rangek = np.arange(i - 8, i + 1, 1)
        tempak = []
        for j in rangek:
            if data[j] > avg:
                tempak.append('u')
            if data[j] < avg:
                tempak.append('d')
        if tempak.count('u') == 9 or tempak.count('d') == 9:
            no_westgard_12.append(i)

    return no_westgard_12


def westgard_13(data):
    #Twelve of twelve points on one side of center line
    no_westgard_13 = []
    poss_range = np.arange(11, len(data), 1)
    # westgard_13 should look at a range of 8 >> poss_range
    avg = stats(data)[0]
    for i in poss_range:
        rangek = np.arange(i - 11, i + 1, 1)
        tempak = []
        for j in rangek:
            if data[j] > avg:
                tempak.append('u')
            if data[j] < avg:
                tempak.append('d')
        if tempak.count('u') == 12 or tempak.count('d') == 12:
            no_westgard_13.append(i)

    return no_westgard_13


def westgard_rules(data):
    we1 = westgard_1(data)
    we2 = westgard_2(data)
    we3 = westgard_3(data)
    we4 = westgard_4(data)
    we5 = westgard_5(data)
    we6 = westgard_6(data)
    we7 = westgard_7(data)
    we8 = westgard_8(data)
    we9 = westgard_9(data)
    we10 = westgard_10(data)
    we11 = westgard_11(data)
    we12 = westgard_12(data)
    we13 = westgard_13(data)



    we_list =[we1, we2, we3, we4, we5, we6, we7, we8, we9, we10, we11, we12, we13]
    total_westgard = []
    for i in we_list:
        for j in i:
            if j not in total_westgard:
                total_westgard.append(j)
    return sorted(total_westgard)



def RSA(data, type = 'all'):
    types = ['weco', 'nelson', 'aiag','juran','hughes', 'duncan']
    if type == 'all':
        r1 = weco_rules(data)
        r2 = nelson_rules(data)
        r3 = aiag_rules(data)
        r4 = juran_rules(data)
        r5 = hughes_rules(data)
        r6 = gitlow_rules(data)
        r7 = duncan_rules(data)
        r8 = westgard_rules(data)

        r_list = [r1, r2, r3, r4, r5, r6, r7, r8]
        data_vector = []
        for i in range(len(data)):
            item_vector = []
            for j in r_list:
                if i in j:
                    item_vector.append(1)
                else:
                    item_vector.append(0)
            data_vector.append(item_vector)
        final = []
        for vector in data_vector:
            if np.sum(vector) >= (len(r_list)/2):
                final.append('T')
            else:
                final.append('F')
        final_index = []
        ind = 0
        for m in final:
            if m =='T':
                final_index.append(ind)
            else:
                pass
            ind +=1


    if type == 'weco':
        final_index = weco_rules(data)

    if type == 'nelson':
        final_index = nelson_rules(data)

    if type == 'aiag':
        final_index = aiag_rules(data)

    if type == 'juran':
        final_index = juran_rules(data)

    if type == 'hughes':
        final_index = hughes_rules(data)

    if type == 'gitlow':
        final_index = gitlow_rules(data)

    if type == 'duncan':
        final_index = duncan_rules(data)

    if type == 'westgard':
        final_index = westgard_rules(data)

    return final_index





#TEST DATA >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
df = pd.read_excel('REPORT_LCZ11.xlsx', sheetname='convertido')

raw = df.T30
data = prepare(raw)[0]

outliers = prepare(raw)[3]



g = 0
print('outliers = ', outliers)
print()
print('WECO POINTS =   ', weco_rules(data))
print('NELSON POINTS = ', nelson_rules(data))
print('AIAG POINTS =   ', aiag_rules(data))
print('JURAN POINTS =  ', juran_rules(data))
print('HUGHES POINTS = ', hughes_rules(data))
print('GITLOW POINTS = ', gitlow_rules(data))
print('DUNCAN POINTS = ', duncan_rules(data))
print('WESTGARD POINTS =', westgard_rules(data))
print('RSA =           ', RSA(data))
print()
print('Outlier Limits = ', (round(prepare(raw)[1],3),round(prepare(raw)[2],3)))
print()
print('Run time = ',round(time()-t0,2),'seconds ')




"""u_1, u_2, u_3 , d_1, d_2, d_3 = area(data , type= 'time')

plt.figure(1)
plt.plot(data, marker='o')
plt.hlines(stats(data)[0],xmax = len(data), xmin= 0,colors='k')
plt.hlines(u_1,xmax = len(data), xmin= 0,colors='c')
plt.hlines(d_1,xmax = len(data), xmin= 0,colors='c')
plt.hlines(u_2,xmax = len(data), xmin= 0,colors='b')
plt.hlines(d_2,xmax = len(data), xmin= 0,colors='b')
plt.hlines(u_3,xmax = len(data), xmin= 0,colors='r')
plt.hlines(d_3,xmax = len(data), xmin= 0,colors='r')
plt.axis([0,len(data),0,max(data) * 1.1])
plt.xticks(list(range(0,len(data)+1)))
plt.show()"""
