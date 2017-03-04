import numpy as np
import math
from statsmodels.stats.stattools import medcouple
#import pandas as pd

data = list(np.arange(1,100, 1))
data.append(300)

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



def weco_1(data):

    no_weco_1 = []
    for i in data:
        if i in stats(data)[5]:
            no_weco_1.append(data.index(i))
    return no_weco_1


#def weco_2(data)
