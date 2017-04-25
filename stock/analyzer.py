import sqlite3, time
from datetime import datetime
from time import mktime

from . neuralNetwork import NeuralNetwork

## ================================================================

class InitialCalculation:
    min_max = []
    def __init__(self):
        pass
    #calculate maximum and minimum values    
    def minmax(self, values):
        transaction=[]
        traded_share = []
        high = []
        low = []
        close = []
        global min_max
        for i in range(len(values)):
            transaction.append(values[i][0])
            traded_share.append(values[i][1])
            high.append(values[i][2])
            low.append(values[i][3])
            close.append(values[i][4]) 
        min_max = [[min(transaction),max(transaction)],[min(traded_share),max(traded_share)],[min(high),max(high)],[min(low),max(low)],[min(close),max(close)]]
        return min_max

    def Average(self, values):
        avg_high=0
        avg_low=0
        avg_closed=0
        avg_transaction = 0
        avg_tradedshare = 0
        list1=[]
        for i in range (0,5):
            avg_transaction  = (avg_transaction +(values[i][0]*(10**(i/2))))
            avg_tradedshare = (avg_tradedshare +(values[i][1]*(10**(i/2))))
            avg_high = (avg_high+(values[i][2]*(10**(i/2))))
            avg_low = (avg_low+(values[i][3]*(10**(i/2))))
            avg_closed = (avg_closed +(values[i][4]*(10**(i/2))))
        a = (10**0 + 10**0.5 + 10**1 + 10**1.5 + 10**2)
        avg_transaction = avg_transaction/a
        avg_tradedshare = avg_tradedshare/a
        avg_high=avg_high/a
        avg_low=avg_low/a
        avg_closed=avg_closed/a
        list1=[avg_transaction,avg_tradedshare,avg_high,avg_low,avg_closed]
        return list1

    def minmaxNepse(self, values):
        banking=[]
        dev_bank = []
        finance = []
        hotel = []
        hydro_power = []
        insurance = []
        nepse = []
        others = []
        global min_max
        for i in range(len(values)):
            banking.append(values[i][0])
            dev_bank.append(values[i][1])
            finance.append(values[i][2])
            hotel.append(values[i][3])
            hydro_power.append(values[i][4])
            insurance.append(values[i][5])
            nepse.append(values[i][6])
            others.append(values[i][7]) 
        min_max = [[min(banking),max(banking)],[min(dev_bank),max(dev_bank)],[min(finance),max(finance)],[min(hotel),max(hotel)],[min(hydro_power),max(hydro_power)],[min(insurance),max(insurance)],[min(nepse),max(nepse)],[min(others),max(others)]]
        #print("min-max = ", min_max)
        return min_max

    def AverageNepse(self, values):
        #return a list that contain 3 elements aka average values of high, low and close 
        avg_banking=0
        avg_devbank=0
        avg_finance=0
        avg_hotel = 0
        avg_hydropower = 0
        avg_insurance = 0
        avg_others = 0
        avg_nepse = 0
        list1=[]
        

        for i in range (0,5):
            avg_banking  = (avg_banking +(values[i][0]*(10**(i/2))))
            avg_devbank = (avg_devbank +(values[i][1]*(10**(i/2))))
            avg_finance = (avg_finance+(values[i][2]*(10**(i/2))))
            avg_hotel = (avg_hotel+(values[i][3]*(10**(i/2))))
            avg_hydropower = (avg_hydropower +(values[i][4]*(10**(i/2))))
            avg_insurance = (avg_insurance+(values[i][5]*(10**(i/2))))
            avg_nepse = (avg_nepse+(values[i][6]*(10**(i/2))))
            avg_others = (avg_others+(values[i][7]*(10**(i/2))))
        a = (10**0 + 10**0.5 + 10**1 + 10**1.5 + 10**2)
        # print('a = ', a)
        avg_banking = avg_banking/a
        avg_devbank = avg_devbank/a
        avg_finance=avg_finance/a
        avg_hotel=avg_hotel/a
        avg_hydropower=avg_hydropower/a
        avg_insurance=avg_insurance/a
        avg_nepse=avg_nepse/a
        avg_others=avg_others/a        
        list1=[avg_banking,avg_devbank,avg_finance,avg_hotel,avg_hydropower,avg_insurance,avg_nepse,avg_others]
        #print("average =", list1)
        return list1

    def denormalizePriceNepse(self, price):
        dnorm = price*(min_max[6][1]-min_max[6][0])+ min_max[6][0]
        return dnorm
    def denormalizePrice(self, price):
        dnorm = price*(min_max[4][1]-min_max[4][0])+ min_max[4][0]
        return dnorm
    def normalizePriceNepse(self,price):
        norm =[]
        for i in range(len(price)):
            if(i <8):
                norm.append((price[i] - min_max[i][0]) / (min_max[i][1] - min_max[i][0]))
            else:
                norm.append((price[i] - min_max[6][0]) / (min_max[6][1] - min_max[6][0]))

        return norm

    def normalizePrice(self,price):
        norm =[]
        for i in range(len(price)):
            if(i <5):
                norm.append((price[i] - min_max[i][0]) / (min_max[i][1] - min_max[i][0]))
            else:
                norm.append((price[i] - min_max[4][0]) / (min_max[4][1] - min_max[4][0]))

        return norm

    

## ================================================================


def getTimeSeriesValues(values, i=-1):
    initial = InitialCalculation()
    averages =[]
    minmax = []
    if (i>=0):
        # i is greater than 0 for the trainingData and testData
        averages =initial.Average(values[i:5+i])
        averages.append(values[i+5][4])
        minmax = initial.minmax(values)

    else:
        # i is less than 0 for predicionData
        # i did this because for Prediction data, target value i.e the '6th' value is not required
        # whereas it is needed to calculate error for training and test process
        averages = initial.Average(values[0:5])
        minmax = initial.minmax(values)

    
    #print('avg =',averages)
    returnData = []

    # build items of the form [[average, minimum, maximum], normalized price]
    returnData = initial.normalizePrice(averages)
    
    #returnData contains normalized value : [norm_high, norm_low, norm_close, target]
    #'target' is present only when this funciton is called by getTrainingData and getTestData
    #print('normal = ', returnData)
    return returnData
##------------------------------------------------------------------------
def getTimeSeriesValuesNepse(values, i=-1):
    initial = InitialCalculation()
    averages =[]
    minmax = []
    
    if (i>=0):
        # i is greater than 0 for the trainingData and testData
        averages =initial.AverageNepse(values[i:8+i])
        #print(averages)
        averages.append(values[i+5][6])
        #print(averages) # initializing average[3] with the target value
        minmax = initial.minmaxNepse(values)
    else:
        averages = initial.AverageNepse(values[0:8])
        minmax = initial.minmaxNepse(values)
    returnData = []
    returnData = initial.normalizePriceNepse(averages)
    return returnData
## ================================================================

def getHistoricalData(c_id):
    if(c_id == 0):
        conn = sqlite3.connect('nepsedata.sqlite3')
    elif (c_id ==1):
        conn = sqlite3.connect('nabildata.sqlite3')
    elif (c_id ==2):
        conn = sqlite3.connect('sanimadata.sqlite3')
    
    elif (c_id ==4):
        conn = sqlite3.connect('adbldata.sqlite3')
    elif (c_id ==5):
        conn = sqlite3.connect('sbidata.sqlite3')
    elif (c_id ==6):
        conn = sqlite3.connect('plicdata.sqlite3')
    # elif (c_id ==7):
    #     conn = sqlite3.connect('shpcdata.sqlite3')
    elif (c_id ==8):
        conn = sqlite3.connect('alicldata.sqlite3')
    
    elif (c_id ==10):
        conn = sqlite3.connect('ahpcdata.sqlite3')
    else:
        conn = sqlite3.connect('ntcdata.sqlite3')
    #else:
        #conn = sqlite3.connect('nepse.sqlite3')
    c = conn.cursor()
    
    def read_form_db():
        c.execute('SELECT * FROM alldata')    
        data=c.fetchall()
        return (data)

    list_data = read_form_db()
    historicalPrices = list_data

    #print(historicalPrices)
    return historicalPrices


## ================================================================

def getTrainingData(c_id, i):
    historicalData = getHistoricalData(c_id)
    if (c_id>0):
        # take the first 100 day's data for training 
        historicalData =  historicalData[105:405]
        historicalData.reverse()
        # get five 5-day averages, 5-day lows, and 5-day highs
        trainingData = getTimeSeriesValues(historicalData, i)

    else:
        historicalData.reverse()
        historicalData =  historicalData[20:120]
        historicalData.reverse()
        #historicalData.reverse()
        # get five 5-day averages, 5-day lows, and 5-day highs
        trainingData = getTimeSeriesValuesNepse(historicalData, i)


    return trainingData

def getTestData(c_id, i):
    historicalData = getHistoricalData(c_id)
    if (c_id>0):
        
        historicalData =  historicalData[5:105]
        historicalData.reverse()
        # get five 5-day averages, 5-day lows, and 5-day highs
        testData = getTimeSeriesValues(historicalData, i)
    else:
        historicalData.reverse()
        historicalData =  historicalData[5:20]
        historicalData.reverse()
        testData = getTimeSeriesValuesNepse(historicalData, i)

    return testData

def getPredictionData(c_id):
    historicalData = getHistoricalData(c_id)
    
    if (c_id>0): 
        del historicalData[5:]
        historicalData.reverse()
        predictionData = getTimeSeriesValues(historicalData)
    else:
        historicalData.reverse()
        del historicalData[5:]
        historicalData.reverse()
        predictionData = getTimeSeriesValuesNepse(historicalData)

    # reverse it so we're using the most recent data first, then ensure we only have 5 data points
    
    
    #historicalData.reverse() #reversed because we dont want the most recent data as the first element of the list
    #when calculating arithematic weighted average
    #print(historicalData)
    # get five 5-day averages, 5-day lows, and 5-day highs
    
    #print("predictionData = ", predictionData)
    #print("historicalData = ",historicalData )
    return predictionData

## ================================================================

def analyzeId(c_id):
    startTime = time.time()
    count2 =0
    itr = 0
    if (c_id>0):
        network = NeuralNetwork(inputNodes = 5, hiddenNodes = 18, outputNodes = 1) #company id >0 for individual prediciton
        averageError = 1      
        while (averageError>0.001 and itr<5000):
        #for i in range(1000):
            count1 =0
            resultBackProp =[]
            while (count1<295):
                trainingData = getTrainingData(c_id,count1)
                resultBackProp.append(network.train(trainingData))
                count1 = count1 +1  
            averageError = sum(resultBackProp)/len(resultBackProp)
        print ("avgError = ", averageError)

        #==================================================================    
        # get data for testing
        
        testError =[]
        while (count2<95):
            testData = getTestData(c_id,count2)
            testError.append(network.accuracyTest(testData))
            count2 = count2 + 1
        
        testErrorAverage = sum(testError)/len(testError)
        
        #====================================================================

        # get data for tomorrow's prediction
        predictionData = getPredictionData(c_id)

        # get prediction result
        returnPrice = network.test(predictionData)

        # de-normalize and return predicted stock price
        final = InitialCalculation()
        predictedStockPrice = final.denormalizePrice(returnPrice)

        # create return object, including the accuracy of the testing
        returnData =[]
        returnData = [predictedStockPrice, testErrorAverage, time.time() - startTime]
        
        print(returnData)
        return (returnData)

    else:
        nep_network = NeuralNetwork(inputNodes = 8, hiddenNodes = 20, outputNodes = 1) #company id =0 for nepse prediciton
        averageError = 1      
        #while (averageError>0.0008):
        while (averageError>0.03):
        #for i in range(1000):
            count1 =0
            resultBackProp =[]
            #print(getTrainingData(c_id,count1))
            while (count1<95):
                trainingData = getTrainingData(c_id,count1)
                resultBackProp.append(nep_network.trainNepse(trainingData))
                count1 = count1 +1  
            averageError = sum(resultBackProp)/len(resultBackProp)
        print ("avgError = ", averageError)

        #==================================================================    
        # get data for testing
        # considering 50 test data, we nedd 45 loops 
        testError =[]
        while (count2<10):
            testData = getTestData(c_id,count2)
            testError.append(nep_network.accuracyTestNepse(testData))
            count2 = count2 + 1
        testErrorAverage = sum(testError)/len(testError)
        #print ("test error =", testError)
        #print("te average = ", testErrorAverage)
        #accuracy = (1- testErrorAverage)*100
        #====================================================================

        # get data for tomorrow's prediction
        predictionData = getPredictionData(c_id)

        # get prediction result
        returnPrice = nep_network.test(predictionData)

        # de-normalize and return predicted stock price
        final = InitialCalculation()
        predictedStockPrice = final.denormalizePriceNepse(returnPrice)

        # create return object, including the accuracy of the testing
        returnData =[]
        returnData = [predictedStockPrice, testErrorAverage, time.time() - startTime]
        
        print(returnData)
        return (returnData)
    
    

## ================================================================

# if __name__ == "__main__":
#     analyzeId(2)
