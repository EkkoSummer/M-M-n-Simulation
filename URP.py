import random
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import math
from scipy import stats
import sympy

lamda = [7,8,9,9.5]
N = 50000
m = 10
mu = 1
indexList = [i for i in range(m)]




def joinShortQ(lamda, sd):
    random.seed(sd)

    X = [[] for i in range(10)]
    S = [[] for i in range(10)]
    enter = [[] for i in range(10)]
    depart = [[0] for i in range(10)]

    t = []
    d = []

    get_arr_time = np.random.exponential(1/lamda,1)
    get_arr_time = float(get_arr_time)
    t.append(get_arr_time)
    enter[0].append(get_arr_time)
    get_ser_time = np.random.exponential(1/mu,1)
    get_ser_time = float(get_ser_time)
    d.append(get_arr_time + get_ser_time)
    S[0].append(get_ser_time)
    depart[0].append(get_arr_time + get_ser_time)




    for j in range(1, N):
        get_arr_time = np.random.exponential(1/lamda, 1)
        get_arr_time = float(get_arr_time)
        t.append(t[j-1] + get_arr_time)



        seletion = random.randint(indexList[0],indexList[-1])

        for i in range(m):
            if i == seletion:
                # record the arrive time
                enter[i].append(t[j])

                #get and update the sertime
                get_ser_time = np.random.exponential(1/mu,1)
                get_ser_time = float(get_ser_time)
                S[i].append(get_ser_time)

                #departTime
                d.append(max(depart[i][-1], t[j]) + get_ser_time)
                d[j] = float(d[j])
                depart[i].append(d[j])

    result = [t,d,enter,S,depart]
    return result

def culWaitTime(t,d):
    w = []
    for i in range(N):
        w.append(d[i] - t[i])
    return w

def averageWait(lamda):
    resAveWait = joinShortQ(lamda, 0)       #PS: it's 0, not 1!
    arriveTime = resAveWait[0]
    departTime = resAveWait[1]
    waitTime = culWaitTime(arriveTime, departTime)

    for i in range(1,m):
        resAveWait = joinShortQ(lamda, i)
        arriveTime = resAveWait[0]
        departTime = resAveWait[1]
        waitTime += culWaitTime(arriveTime, departTime)

    aveWaitTime = [waitTime[i]/10 for i in range(len(waitTime))]
    return aveWaitTime

def culCcdf(dataset):
    res_freq = stats.relfreq(dataset, len(dataset))
    cdf_value = np.cumsum(res_freq.frequency)
    ax = res_freq.lowerlimit + np.linspace(0, res_freq.binsize * res_freq.frequency.size, res_freq.frequency.size)
    #ax = [i for i in range(len(dataset))]
    ay = [1 - i for i in cdf_value]
    ay = np.log(ay)
    plt.ylim(-9, 0)
    plt.plot(ax, ay)


# # #Problem3.1: for each λ, cul the average of waitTime
# lamda = [7,8,9,9.5]
# #
# print("average Lists:\n")
# for l in lamda:
#     print(averageWait(l))
#
# print("average total time:\n")
# for l in lamda:
#     print(sum(averageWait(l)))
#
# #Problem3.2: for each λ, plot the semi-log CCDF in the same figure.
# for l in lamda:
#     culCcdf(averageWait(l))
#
# plt.xlabel('Number of Coms')
# plt.ylabel('log(CCDF)')
# plt.legend(labels = ["λ=7","λ=8","λ=9","λ=9.5"])
# plt.ylim(-13,0)
# plt.show()
# #
# #
#







