import numpy as np
from sklearn.neural_network import MLPClassifier


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
    date = np.arange(1,len(delta),1)/len(delta)
    x = zip(date, delta_prev)
    clf = clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
    clf.fit(x, t)
    print "ANN short term acuracy",clf.score(x, t, sample_weight=None)
    return clf.predict([1+1/len(delta), t[len(t)-1]])[0]

def predictLong(close, predict_range): # input close price and predict range 
    sum = 0
    ma = []
    # date = []
    for i in range(0,len(close)):
        sum = sum + close[i]
        if ( (i+1) % 7 == 0 ):
            ma.append(sum/7.0)
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
    x = zip(date, t_prev)
    clf = clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
    clf.fit(x, t)
    print "ANN long term acuracy",clf.score(x, t, sample_weight=None)
    return clf.predict([1+60/len(delta), t[len(t)-1]])[0]
