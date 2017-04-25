import numpy as np
from sklearn.svm import SVC


# predict_range = 50


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
    data = np.arange(1,len(delta),1)/10.0
    x = zip(data, delta_prev)
    clf = SVC()
    clf.fit(x, t)
    return clf.predict([data[len(data)-1]+0.1, 1])