import numpy as np
import random
import math
# input_data = [[0,0],[0,0],[1,1],[1,1],[1,1]]
rate = 0.5
error_bound = 0.3
node_in = 1
node_hidden = 3
node_out = 1
weight_input = np.zeros((node_in, node_hidden))
weight_hide = np.zeros((node_hidden, node_out))
deltas_input = np.zeros((node_in, node_hidden))
deltas_hide = np.zeros((node_hidden, node_out))
hidden_value = np.zeros((node_hidden, 1))
hidden_error = np.zeros((node_hidden, 1))

def initial():
    #initial weight_input
    for i in range(node_in):
        # print i
        for j in range(node_hidden):
            weight_input[i,j] = random.uniform(-1,1)
    #initial weight_hide    
    for i in range(node_hidden):
        for j in range(node_out):
            weight_hide[i, j] = random.uniform(-1, 1)
    return weight_input,weight_hide

def activate(x):
    return 1.0/(1.0 + math.exp(-x))

def perceptron_train(input_data, rate, correct):
    final_err = 0.0
    for i in range(len(input_data)):
        node_inout = np.zeros((node_hidden, 1))
        node_hiddenout = np.zeros((node_out, 1))
        delta_wi = np.zeros((node_in, node_hidden))
        delta_wh = np.zeros((node_hidden, node_out))
        #======================== calculate input out value ==============
        for j in range(node_hidden):
            for k in range(node_in):
                node_inout[j][0] += input_data[i][k] * weight_input[k,j]
            hidden_value[j,0] = activate(node_inout[j,0])
        #======================== calculate hidden out value ==============
        for j in range(node_out):
            for k in range(node_hidden):
                node_hiddenout[j,0] += hidden_value[k,0] * weight_hide[k,j]
        outvalue = activate(node_hiddenout[0,0])
        #======================== calculate error =========================
        Err = (input_data[i][1] - outvalue) * outvalue * (1 - outvalue)
        tmp = input_data[i][1]-outvalue
        final_err += 0.5*tmp*tmp
        #======================== calculate hide error =====================
        for j in range(node_hidden):
            hidden_error[j,0] = Err * weight_hide[j,0] * hidden_value[j,0] * (1-hidden_value[j,0])
        #======================== back propagation =========================
        for j in range(node_hidden):#update WeightHide
            delta_wh[j,0] += rate * Err * hidden_value[j,0]
            weight_hide[j,0] += delta_wh[j,0] + correct * deltas_hide[j,0]
            deltas_hide[j,0] = delta_wh[j,0]   
        for j in range(node_in):#update weight_input
            for k in range(node_hidden):
                delta_wi[j,k] += rate * hidden_error[k,0] * input_data[i][j]
                weight_input[j,k] += delta_wi[j,k] + correct * deltas_input[j,k]
                deltas_input[j,k] = delta_wi[j,k]
    final_err=final_err/len(input_data)
    return final_err,weight_input,weight_hide

def predict(close,predict_range=10):
    close_cur = close[1:len(close)]
    close_prev = close[0:len(close)-1]
    delta = close_cur - close_prev
    delta[np.where(delta<0)] = (-1)
    delta[np.where(delta>0)] = 1
    delta = delta[len(delta) - predict_range : len(delta)]
    t = np.arange(1,len(delta),1)/10
    input_data = zip(delta, t)
    Weight, HiddenWeight = initial()
    count = 0
    while (count <20000):
        count += 1
        error,final_wi,final_wh = perceptron_train(input_data,rate,error_bound)
        if count==1:
            firstErr = error
        if  error < error_bound:
            break    
    # start to predict       
    next_input = len(delta)+0.1
    node_inout = np.zeros((node_hidden, 1))
    node_hiddenout = np.zeros((node_out, 1))
    for j in range(node_hidden):
            node_inout[j][0] += next_input * weight_input[0,j]
            hidden_value[j,0] = activate(node_inout[j,0])
    for j in range(node_out):
            node_hiddenout[j,0] += hidden_value[0,0] * weight_hide[0,j]
    outvalue = activate(node_hiddenout[0,0])
    if (outvalue>0): 
        return 1
    else:
        return -1

# def predict_longterm(close, ):


