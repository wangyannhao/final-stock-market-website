import sys
sys.path.append('c:/programdata/anaconda2/lib/site-packages')
from yahoo_finance import Share
import csv
import MySQLdb
import pandas as pd
from datetime import date,datetime
import time
import urllib
import numpy as np
import matplotlib.pyplot as plt
import linear_regression as lr
from ann import predict as predict_ann
from linear_regression import predict as predict_regression
from svm_manual import predict as predict_svm
from django.utils import timezone

date.today().strftime("%Y-%m-%d")

def store_realtime_in_database(mydb, table,data):
    # data = [Realtime, Price, Volume]
    cursor = mydb.cursor()
    insert_stmt = (
            "INSERT INTO "+table +"(Realtime, Price, Volume)"
            "VALUES (%s, %s, %s)"
    )
    cursor.execute(insert_stmt,
            data)
    mydb.commit()
    cursor.close()

def store_realtime_in_csv(files,data):
    # data = [Realtime, Price, Volume]
    stock_data = [{'Date_time': str(data[0]), 'Price':str(data[1]), 'Volume': str(data[2])}]
    stock_pandas = pd.DataFrame(stock_data)
    with open(files,'a') as f:
         stock_pandas.to_csv(f,header=False)

def store_historical_in_database(mydb, csv_data, table): 
    cursor = mydb.cursor() 
    with open(csv_data) as f:
        reader = csv.reader(f)
        for row in reader:
            #adj = double(row[1])
            insert_stmt = (
                    "INSERT INTO " + table +"(Adj_Close, Close_price, Date_time, High_price, Low_price, Open_price, Stock_name, Volume)"
                    "VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                    )
            cursor.execute(insert_stmt, row[1:9])
            print row[1:9]
            mydb.commit()
    cursor.close()

def create_historical_table(mydb,table):
    cursor = mydb.cursor()
    cursor.execute('create table ' + table +"("
    'Date_time varchar(40),'
    'Adj_Close varchar(20),'
    'Close_price varchar(20),'
    'High_price varchar(20),'
    'Low_price varchar(20),'
    'Open_price varchar(20),'
    'Stock_name varchar(20),'
    'Volume varchar(20),'
    'primary key (Date_time)'
    ');')
    mydb.commit()
    cursor.close()
    
def create_realtime_table(mydb, table):
    cursor = mydb.cursor()
    cursor.execute('create table ' + table +'('
            'Realtime varChar(40),'
            'Price varChar(20),'
            'Volume varChar(20),'
            'primary key (Realtime)'
            ')'
            )
    mydb.commit()
    cursor.close()
    
def get_historical(stock):
    symbol = Share(stock)
    stock_data = symbol.get_historical('2016-01-01',date.today().strftime("%Y-%m-%d"))
    stock_df = pd.DataFrame(stock_data)
    dataFileName = stock + '_historical.csv'
    stock_df.to_csv(dataFileName)
    temp = pd.DataFrame({'Close_Price':[],'Low':[],'High':[],'Date':[]})
    temp['Date'] = stock_df['Date']
    temp['High'] = stock_df['High']
    temp['Low'] = stock_df['Low']
    temp['Close_Price'] = stock_df['Adj_Close']
    dataFileName = stock +'.csv'
    temp.to_csv('../static/js/csv/'+dataFileName,index_label=False,index=False)

# def get_realtime_data(stock,mydb,table):
    # symbol = Share(stock)
    # symbol.refresh()
    # price  = symbol.get_price()
    # volume = symbol.get_volume()
    # date_time = str(datetime.now())[:19]
    # data=[date_time, price, volume]
    # print stock, data
    # store_realtime_in_database(mydb,table, data) 
    # files = stock+'_realtime_1.csv'
    # store_realtime_in_csv(files, data)

def get_realtime_from_url(stock,table):
    urllib.urlretrieve ("http://finance.yahoo.com/d/quotes.csv?s=" +stock + "&f=sl1d1t1c1ohgv&e=.csv","static/js/csv/real_time/"+stock+"_realtime_url.csv")
    csv_data = "static/js/csv/real_time/"+stock+"_realtime_url.csv"
    cursor = mydb.cursor() 
    with open(csv_data) as f:
        reader = csv.reader(f)
    for row in reader:
        insert_stmt = (
                    "INSERT INTO " + table +"(Realtime, Price, Volume)"
                    "VALUES (%s,%s,%s)"
                    )
        time = str(datetime.now())
        price = str(row[1])
        volume = str(row[8])
        data = [time,price, volume]
        print stock, data
        cursor.execute(insert_stmt, data)
        mydb.commit()
        cursor.close()

def get_realtime_data(stock_list):
    data_list = []
    for stock in stock_list:
        urllib.urlretrieve ("http://finance.yahoo.com/d/quotes.csv?s=" +stock + "&f=sl1d1t1c1ohgv&e=.csv","static/js/csv/real_time/"+stock+"_realtime_url.csv")
        csv_data = "static/js/csv/real_time/"+stock+"_realtime_url.csv"
        with open(csv_data) as f:
            reader = csv.reader(f)
            for row in reader:
                time = str(datetime.now())
                price = str(row[1])
                volume = str(row[8])
                data = [time, price, volume]
                data_list.append(data)
    return data_list

def timer(times,stock,table):
    now = datetime.now()
    close_time = now.replace(hour=16, minute=00, second = 0, microsecond = 0) # set stop time
    while(True):
        now = datetime.now()
        for each in stock:
            get_realtime_from_url(each,table[each])
        now = datetime.now()
        if now > close_time: # market closes at 16:00
            print "market closed"
            break
        time.sleep(times)

def collect_data():
    # change retrieve type here
    historical = 1  
    mydb = MySQLdb.connect(host = 'localhost',
           user='root',
           passwd='123456',
           db='test')
   
    stock = ['AAPL', 'AMZN', 'FB', 'GOOG', 'GPRO', 'INTC', 'NFLX', 'TSLA', 'TWTR', 'YHOO']
    table_realtime = {'AAPL':'AAPL_realtime',
                  'AMZN':'AMZN_realtime',
                  'FB':'FB_realtime',
                  'GOOG':'GOOG_realtime',
                  'GPRO':'GPRO_realtime',
                  'INTC':'INTC_realtime',
                  'NFLX':'NFLX_realtime',
                  'TSLA':'TSLA_realtime',
                  'TWTR':'TWTR_realtime',
                  'YHOO':'YHOO_realtime'}
    table_historical = {'AAPL':'AAPL_historical',
                  'AMZN':'AMZN_historical',
                  'FB':'FB_historical',
                  'GOOG':'GOOG_historical',
                  'GPRO':'GPRO_historical',
                  'INTC':'INTC_historical',
                  'NFLX':'NFLX_historical',
                  'TSLA':'TSLA_historical',
                  'TWTR':'TWTR_historical',
                  'YHOO':'YHOO_historical'}
    
    for i in range(len(stock)):
        if historical:
            cursor = mydb.cursor()
            cursor.execute('DROP TABLE IF EXISTS '+table_historical[stock[i]] )
            mydb.commit()
            cursor.close()
            create_historical_table(mydb, table_historical[stock[i]])
        else:
            cursor = mydb.cursor()
            cursor.execute('DROP TABLE IF EXISTS '+table_realtime[stock[i]] )
            mydb.commit()
            cursor.close()
            create_realtime_table(mydb,table_realtime[stock[i]])
            
    if historical: 
        for each in stock:
            get_historical(each)
            filename = each + '_historical.csv'
            store_historical_in_database(mydb, filename, table_historical[each])
        
    else:
        timer(30,stock,table_realtime)

def get_data_db(table):
    mydb = MySQLdb.connect(host = 'localhost',
       user='root',
       passwd='123456',
       db='test')
    cursor = mydb.cursor()
    cursor.execute("SELECT * from "+table)
    tbl = cursor.fetchall()
    return tbl
    
def getAverage(data):
    sum = 0.0
    for i in range(len(data)-1):
        # print i  
        try:
            sum = sum + float(data[i][2])
        except ValueError,e:
            print "error",e,"on line",i
    return sum/len(data)

def getLowest(data):
    low = float(data[0][2])
    for i in range(len(data)-1):
        try:
            if low > float(data[i][2]):
                low = float(data[i][2])
        except ValueError,e:
            print "error",e,"on line",i
    return low

def getHighest(data):
    high = float(data[0][2])
    for i in range(len(data)-11,len(data)-1):
        try:
            if high < float(data[i][2]):
                high = float(data[i][2])
        except ValueError,e:
            print "error",e,"on line",i
    return high

# companies: average stock price lesser than the lowest of any of the Selected Company
def getCompanies(tbl):
    data = get_data_db(tbl)
    low = getLowest(data)
    table_historical = {'GOOG','YHOO','FB','AMZN','TWTR','GPRO','INTC','NFLX','TSLA'}
    companies = []
    for c in table_historical:
        tmp = getAverage(get_data_db(c+'_historical'))
        if tmp < low:
            companies.append(c)
    # print companies
    print "hahah"
    print companies
    return companies
    
def bollingerBands(tbl, dur = 20):
    whole = get_data_db(tbl)
    close = zip(*whole)[2]
    close = np.asarray(map(float,close[0:len(close)-1]))
    Date = zip(*whole[0:len(whole)-1])[0]
    data = {'price': close}
    df = pd.DataFrame(data)
    df['MA'] = df.rolling(window=20).mean()
    std = pd.rolling_std(df['price'],window=20)
    df['upper'] = df['MA'] + std
    df['lower'] = df['MA'] - std
    df['b'] = (df['price']-df['lower']) / (df['upper']-df['lower'])*1.00
    df['BW'] = (df['upper']-df['lower']) / df['MA']*1.00
    df['date'] = Date

    #csv
    temp = pd.DataFrame({'Date':df['date'],'Price':df['price'],'MA':df['MA'],'upper':df['upper'],
        'lower':df['lower']})
    stockabbr = tbl.split('_')[0]
    csvfileName1 = stockabbr+'_bollinger1.csv'
    temp.to_csv(csvfileName1,index_label=False,index=False)

    temp1 = pd.DataFrame({'Date':df['date'],'b':df['b'],'BW':df['BW']})
    csvfileName2 = stockabbr+'_bollinger2.csv'
    temp1.to_csv("../static/js/indicator/"+csvfileName2,index_label=False,index=False)
    # plt.plot(df['price'])
    # plt.plot(df['MA'])
    # plt.plot(df['upper'])
    # plt.plot(df['lower'])
    # plt.plot(df['b'])
    # plt.plot(df['BW'])
    # plt.show()
    return df

def cal_rsi(tbl,dur=14): #calculate Relative Strength Index from database table
    table = get_data_db(tbl)
    close = zip(*table)[1]
    date2 = zip(*table)[0]
    date2 = date2[1:len(date2)-1]
    date = date2[dur-1:len(date2)]
    print len(date)
    close = close[0:len(close)-1]
    close = map(float, close)
    close_tmp = np.asarray(close)
    rsi = []
    for i in range(0,len(close_tmp)-dur):
        prev = close_tmp[i:i+dur]
        cur = close_tmp[i+1:i+dur+1]
        tmp = cur-prev
        U = np.where(tmp>0)
        D = np.where(tmp<0)
        U = np.abs(tmp[U[0]])
        D = np.abs(tmp[D[0]])
        U_avg = np.average(U)
        D_avg = np.average(D)
        rsi.append(100-100/(1+U_avg/D_avg))
    # print len(rsi)
    # plt.plot(rsi)
    # plt.show()
    # csv
    temp = pd.DataFrame({'date':date,'rsi':rsi})
    csvfilename = tbl.split('_')[0]+'_rsi.csv'
    temp.to_csv("../static/js/indicator/"+csvfilename,index_label=False,index=False)
    return rsi, date

def cal_dmi(tbl,dur=14):
    table = get_data_db(tbl)
    date = zip(*table)[0]
    date = date[1:len(date)-1]
    close = zip(*table)[1]
    close = np.asarray(map(float,close[0:len(close)-1]))
    high = zip(*table)[3]
    high = np.asarray(map(float,high[0:len(high)-1]))
    low = zip(*table)[4]
    low = np.asarray(map(float,low[0:len(low)-1]))

    TR1 = high[1:len(high)] - low[1:len(high)]
    TR2 = np.abs(high[1:len(high)] - close[0:len(high)-1])
    TR3 = np.abs(low[1:len(high)] - close[0:len(high)-1])
    TR = np.maximum(TR1,TR2)
    TR = np.maximum(TR,TR3)

    prev_high = high[0:len(high)-1] 
    cur_high = high[1:len(high)]
    prev_low = low[0:len(low)-1]
    cur_low = low[1:len(low)]
    upmove = cur_high - prev_high
    downmove = prev_low - cur_low
    upmove[np.where(upmove<0)[0]] = 0 
    downmove[np.where(downmove<0)[0]] = 0
    delta = upmove - downmove

    downmove[np.where(delta>0)[0]] = 0
    upmove[np.where(delta<0)[0]] = 0

    downmove = 100 * downmove / TR
    upmove = 100 * upmove / TR
    DI_plus = pd.ewma(upmove,None,14)
    DI_minus = pd.ewma(downmove, None, 14)
    ADX = np.abs((DI_plus - DI_minus) / (DI_plus + DI_minus))
    ADX = 100*pd.ewma(ADX,None,14)
    ADX = ADX[14:len(ADX)]
    DI_plus = DI_plus[14:len(DI_plus)]
    DI_minus = DI_minus[14:len(DI_minus)]

    # csv
    date = date[14:len(date)]
    temp = pd.DataFrame({'date':date,'ADX':ADX,'DI_plus':DI_plus,'DI_minus':DI_minus})
    csvfilename = tbl.split('_')[0]+'_dmi.csv'
    temp.to_csv("../static/js/indicator/"+csvfilename,index_label=False,index=False)

    return ADX, DI_plus, DI_minus, date

def ann_predict(tbl, predict_range=30):
    table = get_data_db(tbl)
    close = zip(*table)[1]
    close = np.asarray(map(float,close[0:len(close)-1]))
    result  = predict_ann(close, predict_range )
    return result

def svm_predict(tbl, predict_range):
    table = get_data_db(tbl)
    date = zip(*table)[0]
    date = date[0:len(date)-1]
    close = zip(*table)[1]
    close = np.asarray(map(float,close[0:len(close)-1]))
    result = predict_svm(close, predict_range)
    return result

def regression_predict(tbl, predict_range):
    table = get_data_db(tbl)
    date = zip(*table)[0]
    date = date[1:len(date)-1]
    close = zip(*table)[1]
    close = np.asarray(map(float,close[0:len(close)-1]))
    result = predict_regression(close,predict_range)
    return result,close[len(close)-1], date[len(date)-1],date[len(date)-2]

# if __name__ == '__main__':
#     # stock = ['AAPL_historical', 'AMZN_historical', 'FB_historical', 'GOOG_historical', 'GPRO_historical', 'INTC_historical', 'NFLX_historical', 'TSLA_historical', 'TWTR_historical', 'YHOO_historical']
#     # for i in stock:
#     #     bollingerBands(i, 20)
#     #     cal_rsi(i,14)
#     #     cal_dmi(i, 14)
#     # print ann_predict("AMZN_historical", 10)
#     # print svm_predict("AMZN_historical", 10)
#     # print regression_predict("AMZN_historical",100)
#     collect_data()











