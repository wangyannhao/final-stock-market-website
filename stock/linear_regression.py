from numpy import *
import numpy
import math

# M = 7

# Mp = M + 1
alpha = 0.005
beta = 11.1

fileName = {1: 'Square.csv',
            2: 'Twitter.csv',
            3: 'Facebook.csv',
            4: 'Amazon.csv',
            5: 'Alphabet.csv',
            6: 'Netflix.csv',
            7: 'Tesla.csv',
            8: 'Alibaba.csv',
            9: 'GoPro.csv',
            10: 'Fitbit.csv'}

def readfile(filename,len):
    file = open(filename)
    X = []
    i = 0
    for line in file.readlines():
        if i<len:
            item = line.split(',')
            X.append(float(item[4]))
            i += 1
    return X

def chooseFile():
    print 'Choose the number of train data to read: '
    num = []
    for j in fileName:
        print str(j) + ':' + fileName[j]
        num.append(str(j))
    file = raw_input()
    while file not in num:
        print 'input is invalid, please input the number of train data: '
        file = raw_input()
    print 'The train data file is: ' + fileName[int(file)]

    print 'Choose the length of train data (100-240): '
    length = input()
    while length<100 or length>240:
        print 'input is invalid, please input a length between 100 and 240: '
        length = input()
    print 'The length of train data is: ' + str(length)

    Datas = readfile(fileName[int(file)], length)
    x = length+1
    Dlength = length
    N = numpy.arange(1,x,1)

    return Datas,x,Dlength,N


def getPhiX(x,Mp):
    PhiX = []
    i = 0
    while i < Mp:
        PhiX.append(math.pow(x, i))
        i += 1
    PhiXX = numpy.array(PhiX)
    return PhiXX


def getInvS(N,Mp):
    I = numpy.ones((Mp, Mp))
    tmp = numpy.zeros((Mp, Mp))
    for n in range(0, len(N)):

        PhiX = getPhiX(N[n],Mp)
        PhiX.shape = (Mp, 1)
        PhiXT = numpy.transpose(PhiX)
        tmp += numpy.dot(PhiX, PhiXT)

    betaPhi = beta * numpy.matrix(tmp)
    alphaI = alpha * numpy.matrix(I)
    InverseS = alphaI + betaPhi
    return InverseS


def getm(x,data,N,Mp):
    tmp = numpy.zeros((Mp, 1))
    PhiX = getPhiX(x,Mp)
    PhiX.shape = (Mp, 1)
    InverseS = getInvS(N,Mp)
    S = numpy.linalg.inv(InverseS)
    PhiXT = numpy.transpose(PhiX)
    tmp1 = numpy.dot(PhiXT, S)
    mult = beta * numpy.matrix(tmp1)
    n = 0
    while n < len(N):
        phiXn = getPhiX(N[n],Mp)
        phiXn.shape = (Mp, 1)
        z = numpy.dot(phiXn, data[n])
        tmp = numpy.add(tmp, z)
        n += 1
    result = numpy.dot(mult, tmp)
    return result[0,0]


def gets2(x):
    PhiX = getPhiX(x)
    PhiX.shape = (Mp, 1)
    InverseS = getInvS()
    PhiXT = numpy.transpose(PhiX)
    S = numpy.linalg.inv(InverseS)
    tmp = numpy.dot(PhiXT, S)
    s2 = numpy.dot(tmp, PhiX)
    s2 += (1 / beta)
    return s2[0,0]

# def error():
#     meanErr = 0
#     relativeErr = 0
#     predict = getm(x)
#     i = 0
#     while i<Dlength:
#         meanErr += Datas[i] - predict
#         relativeErr += (Datas[i] - predict)/Datas[i]
#         i += 1
#     meanErr /= Dlength
#     relativeErr /= Dlength
#     print 'Absolute Mean Error is: '+ str(meanErr)
#     print 'Average Relative Error is: '+ str(relativeErr)
def predict(table, range):
    M=10
    Datas = table[len(table)-range:len(table)]
    x = len(Datas)+1
    Dlength = len(Datas)
    N = numpy.arange(1,x,1)
    # print len(N),"hahahahha"
    mean = getm(x,Datas,N,M+1)
    return mean
def predictLong(table, rrange):
    M = 1
    Datas = table[len(table)-rrange:len(table)]
    sum = 0
    ma = []
    for i in range(0,len(Datas)):
        sum = sum + Datas[i]
        if ( (i+1) % 7 == 0 ):
            ma.append(sum/7.0)
            sum = 0
    x = len(ma)+1
    Dlength = len(ma)
    N = numpy.arange(1,x,1)
    # print len(N),"hahahahha"
    mean = getm(x+8,ma,N,M+1)
    return mean

# def predictLong(table, rrange):
#     # long term t

#     start = len(table) % rrange
#     distance = (len(table)-start) / rrange
#     # print distance,"distance ", len(table),'table'
#     # x = len(Datas)+1
#     # N_s = numpy.arange(1,x,1)
#     N = []
#     Datas = []
#     count = 0
#     for i in range(start, len(table)):
#         count = count + 1
#         if count % distance == 0:
#             Datas.append(table[i])
#             N.append(i)
#     # Datas = table[len(table)-rrange:len(table)]
#     x = len(Datas)+1
#     # print x,"xxxxxxxxxxxx"
#     Dlength = len(Datas)
#     # N = numpy.arange(1,x,1)
#     mean = getm(x+distance,Datas,N)
#     # print len(N),"xixiixixi"
#     return mean
