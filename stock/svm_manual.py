import numpy as np
from sklearn.svm import SVC


  # // written by: Yanhao Wang
  # // assisted by:  Xin Zhang
  # // debugged by:
  # // etc.
def predict(close, predict_range): # input close price and predict range 
# table = get_data_db("AMZN_historical")
# close = zip(*table)[1]
# close = np.asarray(map(float,close[0:len(close)-1]))

    close_cur = close[1:len(close)]
    close_prev = close[0:len(close)-1]
    delta = close_cur - close_prev
    delta[np.where(delta<0)] = (-1)
    delta[np.where(delta>0)] = 1
    t = delta[len(delta) - predict_range : len(delta)]
    delta_prev = delta[len(delta) - predict_range-1 : len(delta)-1]
    date = np.arange(1,len(delta),1)
    date = date/float(len(date))
    x = zip(date, delta_prev)
    clf = SVC()
    clf.fit(x, t)
    print "short term svm acuracy",clf.score(x,t)
    return clf.predict([date[len(date)-1]+1/len(date)/7, t[len(t)-1]])[0]

def predictLong(close, predict_range): # input close price and predict range 

    sum = 0
    ma = []
    # date = []
    for i in range(0,len(close)):
        sum = sum + close[i]
        if ( (i+1) % 7 == 0 ):
            if (sum>0):
                ma.append(1)
            elif(sum<0):
                ma.append(-1)
            else:
                ma.append(0)
            # date.append((i+1))
            sum = 0
    close_cur = close[1:len(ma)]
    close_prev = close[0:len(ma)-1]
    delta = close_cur - close_prev
    delta[np.where(delta<0)] = (-1)
    delta[np.where(delta>0)] = 1

    t = delta[1:len(delta)]
    t_prev = delta[0:len(delta)-1]
    date = np.arange(1,len(t)+1,1)
    date = date/float(len(date))
    x = zip(date, t_prev)
    clf = SVC()
    clf.fit(x, t)
    # print "long term svm acuracy",clf.score(x,t)
    # print date, len(date)
    print date[len(date)-1]+8/float(len(date)), date[len(date)-1]
    return clf.predict([date[len(date)-1]+8/float(len(date)), t[len(t)-1]])[0]