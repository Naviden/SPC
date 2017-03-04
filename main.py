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
    return data



def outlier_limits(data):

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

    return loa,uoa


def clean_data(data):
    #cleans data from outliers

    loa, uoa = outlier_limits(data)

    for i in data:
        if i < loa or i > uoa:
            data.remove(i)
    return data


def stats(data):

    avg = np.mean(data)
    qq1 = np.percentile(data, 25)
    med = np.median(data)
    qq3 = np.percentile(data, 75)
    std = np.std(data)
    loa, uoa = outlier_limits(data)
    out = []
    for j in data:
        if j < loa or j > uoa:
            out.append(j)
    if len(out) > 0:
        outlier = out
        outlier = [round(s, 2) for s in outlier]
        outlier = sorted(outlier)
    else:
        outlier = []

    return avg, qq1, med, qq3, std, outlier


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
    no_weco_1 = []
    indexak = 0
    for i in data:
        if i in stats(data)[5]:
            no_weco_1.append(indexak)
        indexak+=1
    return no_weco_1


def weco_2(data):
    no_weco_2 = []
    poss_range = np.arange(2,len(data),1)
    #weco_2 should look at a range of 3 >> poss_range
    for i in poss_range:
        rangek = np.arange(i-2, i, 1)
        stat_check = []
        for j in rangek:
            stat_check.append(find_area(data, data[j], ddtype ='time'))
        if stat_check.count('u2') + stat_check.count('u3') >= 2 or \
                                stat_check.count('d2') + stat_check.count('d3') >= 2:
            no_weco_2.append(i)
    return no_weco_2



#TEST DATA >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
df = pd.read_excel('REPORT_LCZ11.xlsx', sheetname='convertido')

"""plt.figure(1)
plt.plot(df.T1)
plt.show()"""


data = prepare(df.T1)



print(weco_1(data))
print('outliers = ', stats(data)[5])

print('Outlier Limits = ', outlier_limits(data))
a = 0
for g in data:
    print (a,'-',g)
    a  =a + 1
