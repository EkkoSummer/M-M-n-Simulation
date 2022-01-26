import random
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import math
from scipy import stats
import sympy

lam = [0.7,0.8,0.9,0.95]
mu = 1
N = 10000


def mm1(lamda,sd):
    random.seed(sd)

    #initialize
    arrTime = [np.random.exponential(1/lamda,1)]
    waitTime = [0]
    serveTime = [np.random.exponential(1/mu,1)]
    departTime = [arrTime[0] + serveTime[0]]

    arrTime[0] = float(arrTime[0])
    serveTime[0] = float(serveTime[0])
    departTime[0] = float(departTime[0])

    #3 results
    X = [0]
    D = [0]
    B = []
    Ns = []

    #simulation/assignment
    for i in range(1, N):
        #arrTime
        get_arr_time = np.random.exponential(1/lamda,1)
        arrTime.append(arrTime[i-1] + get_arr_time)
        get_ser_time = np.random.exponential(1/mu,1)
        serveTime.append(get_ser_time)
        startTime = max(arrTime[i], departTime[-1])
        departTime.append(startTime + serveTime[i])
        waitTime.append(departTime[i] - arrTime[i])

        arrTime[i] = float(arrTime[i])
        serveTime[i] = float(serveTime[i])
        departTime[i] = float(departTime[i])
        waitTime[i] = float(waitTime[i])

    #Xti
    for i in range(1, N):
        for j in range(i-1, -1, -1):
            if departTime[j] <= arrTime[i]:      #when i-th comes, j-th has already left
                X.append(i-j-1)
                break
            if departTime[0] >= arrTime[i]:      #if the 1st cos doesn't leave when i-th cos comes
                X.append(i)
                break
            else:
                continue


    #Dti
    for i in range(N):
        for j in range(i+1, N):
            if departTime[i] < arrTime[j]:
                D.append(j-i)
                break
            if departTime[i] >= arrTime[N-1]:
                D.append(N-i+1)
                break
            else:
                continue


    #Ns
    for i in range(N-1):
        Ns.append(1)
        if arrTime[i+1] > departTime[i]:    #means there exists the idle time
            Ns.append(0)
        else:
            Ns.append(1)
    Ns.append(1)    #the last cos to be served
    Ns.append(0)    #the last cos left


    #Bi
    for i in range(len(Ns)):
        if Ns[i] == 0:
            flag = i
            break
    B.append(departTime[flag//2] - arrTime[0])     #B[0]
    B[0] = float(B[0])
    flag2 = flag

    for i in range(flag+1,len(Ns)):
        if Ns[i] == 0:      #from busy to idle
            B.append(departTime[i//2] - arrTime[flag2//2 +1])     #this-time's departTime - last-time+1's startTime
            B[-1] = float(B[-1])
            flag2 = i


    return [X,D,B,arrTime,departTime,serveTime,waitTime]


    # D.sort()
    # p = 1. * np.arange(len(D)) / (len(D)-1) # 计算各点的累计概率 F(x)
    # p = [1-i for i in p]                       # 计算概率的补 1-F(x)
    #
    # outX = []
    # for i in range(N):
    #     outX.append(i)
    # y = np.log10(p)                            # log(1-F(x))
    # plt.plot(outX,y)
    # plt.show()

def plotCcdf(data,upper):
    res_freq = stats.relfreq(data,len(data))
    cdf_value = np.cumsum(res_freq.frequency)
    ax = res_freq.lowerlimit + np.linspace(0, res_freq.binsize * res_freq.frequency.size, res_freq.frequency.size)
    #ax = np.linspace(0,upper)
    ay = [1 - i for i in cdf_value]
    ay = np.log(ay)
    plt.plot(ax, ay)


def theoryRes(lamda,paraSet):
    n = len(paraSet)
    theoCcdf = []
    # a = sympy.Symbol("a")
    # b = sympy.solve(sympy.exp(-a) - lamda, a)
    # b = b[0]
    for k in range(n):
        theoCcdf.append(lamda**k)
        #theoCcdf.append(math.e ** (-1 * b) ** k)
    return theoCcdf



# # ##Problem1: for each lam,simulation 10 times
getResult = [[] for i in range(len(lam))]

for i in range(len(lam)):
    for j in range(10):
        getResult[i].append(mm1(lam[i],j))
# for i in range(10):
#     for j in range(4):
#         print(getResult[j][i])

# print(getResult[0][0][0])
# print(getResult[0][0][1])

#Problem2: get 10 plots and then get an average data's plot for arrSee

# #set of separate plots
# plt.figure("MM1_arrSee_sep")
# for i in range(10):
#     for j in range(4):
#         plt.subplot(5, 2, i + 1)
#         plotCcdf(getResult[j][i][0],20)
#     plt.ylim(-4, 0)
# plt.subplots_adjust(wspace =0.1, hspace =0.4)
# plt.show()
#
# #ave
# aveX = []       #4 sets of 100 data of X
# for i in range(4):
#     temp = getResult[i][0][0]
#     for i in range(1, 10):
#         temp = np.array(temp) + np.array(getResult[0][i][0])
#     temp = [n/10 for n in temp]
#     aveX.append(temp)
#
# plt.figure("MM1_arrSee_ave")
# for i in range(4):
#     plotCcdf(aveX[i], 10)
# plt.xlabel('Coms in Sys')
# plt.ylabel('log(CCDF)')
# plt.legend(labels = ["λ=7","λ=8","λ=9","λ=9.5"])
# plt.ylim(-4,0)
# plt.show()

#Problem3: get 10 plots and then get an average data's plot for departSee
#set of separate plots
plt.figure("MM1_depSee_sep")
for i in range(10):
    for j in range(4):
        plt.subplot(5, 2, i + 1)
        plotCcdf(getResult[j][i][1],50)
    plt.ylim(-4, 0)
plt.subplots_adjust(wspace =0.1, hspace =0.4)
plt.show()

#ave
aveX = []       #4 sets of 100 data of X
for i in range(4):
    temp = getResult[i][0][1]
    for i in range(1, 10):
        temp = np.array(temp) + np.array(getResult[0][i][1])
    temp = [n/10 for n in temp]
    aveX.append(temp)

plt.figure("MM1_depSee_ave")
for i in range(4):
    plotCcdf(aveX[i], 50)
plt.xlabel('Coms in Sys')
plt.ylabel('log(CCDF)')
plt.legend(labels = ["λ=7","λ=8","λ=9","λ=9.5"])
plt.xlim(0,15)
plt.ylim(-5,0)
plt.show()


# #Problem4: plot the average CCDF of B
#
# #single time
outB = []
for i in range(4):
    for j in range(10):
        outB = outB + getResult[i][j][2]
plt.figure("busyTime")
for l in lam:
    plotCcdf(mm1(l,0)[2],80)
plt.xlabel('busyTime')
plt.ylabel('log(CCDF)')
plt.legend(labels = ["λ=7","λ=8","λ=9","λ=9.5"])
plt.xlim(0,10)
plt.ylim(-2.5,0)
plt.show()

#Problem5: plot X,D and theory result in the same semi-log plot
# plt.figure("Compare")
# for l in lam:
#     plotCcdf(mm1(l,0)[0],20)
# for l in lam:
#     plotCcdf(mm1(l,0)[0],20)
# for l in lam:
#     b = np.log(l)
#     plt.plot([0,80],[0,80*b])
#
# plt.ylabel('log(CCDF)')
# plt.legend(labels = ["Bλ=7","Bλ=8","Bλ=9","Bλ=9.5","Dλ=7","Dλ=8","Dλ=9","Dλ=9.5","Tλ=7","Tλ=8","Tλ=9","Tλ=9.5"])
# plt.xlim(0,80)
# plt.ylim(-2.5,0)
# plt.show()

###Problem6: For each lam, plot the CCDF of B in the same figure
plt.figure("4busyTime")
for l in lam:
    plotCcdf(mm1(l,0)[2],80)
plt.xlabel('busyTime')
plt.ylabel('log(CCDF)')
plt.legend(labels = ["λ=7","λ=8","λ=9","λ=9.5"])
plt.xlim(0,80)
plt.ylim(-5,0)
plt.show()


