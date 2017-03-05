import numpy as np
import math
from statsmodels.stats.stattools import medcouple
import matplotlib.pyplot as plt
import pandas as pd



def prepare(data):
    #convert Series to list
    data = data.tolist()
    #Remove possible zeros
    data = list(filter(lambda a: a != float(0), data))

    qq1 = np.percentile(data, 25)
    qq3 = np.percentile(data, 75)
    IQR = qq3 - qq1

    medad = float(medcouple(data))
    if medad > 0:
        loa = qq1 - (1.5 * ((math.e ** (-4 * medad)) * IQR))
        uoa = qq3 + (1.5 * ((math.e ** (3 * medad)) * IQR))
    if medad <= 0:
        loa = qq1 - (1.5 * ((math.e ** (-3 * medad)) * IQR))
        uoa = qq3 + (1.5 * ((math.e ** (4 * medad)) * IQR))
    if medad == 0:
        loa = qq1 - (1.5 * IQR)
        uoa = qq3 + (1.5 * IQR)
    out = []
    for i in data:
        if i < loa or i > uoa:
            out.append(i)
            data.remove(i)
    if len(out) > 0:
        outlier = out
        outlier = [round(s, 2) for s in outlier]
        outlier = sorted(outlier)
    else:
        outlier = []
    return data, loa, uoa, outlier


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


def internal_checker(data, outrange, inrange, limit):
    #to be used inside weco and similar rules

    for_return = []
    poss_range = np.arange(outrange-1, len(data), 1)

    for i in poss_range:
        rangek = np.arange(i - outrange-1, i, 1)
        tempak = []
        for j in rangek:
            if data[j] > limit:
                tempak.append('u')
            if data[j] < limit:
                tempak.append('d')
        if tempak.count('u') >= inrange or tempak.count('d') >= inrange:
            for_return.append(i)

    return no_weco_2


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
        rangek = np.arange(i-2, i, 1)
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
        rangek = np.arange(i - 4, i, 1)
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
    u_1, u_2, u_3, d_1, d_2, d_3 = area(data, type='time')
    no_weco_4 = []
    poss_range = np.arange(7, len(data), 1)
    # weco_4 should look at a range of 8 >> poss_range
    avg = stats(data)[0]
    for i in poss_range:
        rangek = np.arange(i - 7, i, 1)
        tempak = []
        for j in rangek:
            if data[j] > avg:
                tempak.append('u')
            if data[j] < avg:
                tempak.append('d')
        if tempak.count('u') == 8 or tempak.count('d') == 8:
            no_weco_4.append(i)

    return no_weco_4

#TEST DATA >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
df = pd.read_excel('REPORT_LCZ11.xlsx', sheetname='convertido')

data = prepare(df.T30)
data = clean_data(data)






print('weco_1 ='  ,weco_1(data))
print('weco_2 = '  ,weco_2(data))
print('weco_3 = '  ,weco_3(data))
print('weco_4 = '  ,weco_4(data))
print('outliers = ', stats(data)[5])

print('Outlier Limits = ', (round(outlier_limits(data)[0],3),round(outlier_limits(data)[1],3)))

u_1, u_2, u_3 , d_1, d_2, d_3 = area(data , type= 'time')

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
plt.show()
