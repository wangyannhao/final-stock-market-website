from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from  . import data
from  . import data1
from datetime import date
from django.utils import timezone
# Create your views here.
#from .models import Today
from . models import Company
from .models import Nepse
from . import analyzer
import json_, sqlite3
from decimal import Decimal
import retrieve_data_update as rdu
from yahoo_finance import Share
import pandas as pd
import csv,os
#from .stock import neuralNetwork

company =  {28:['GOOG','Google'],
			29:['TWTR','Twitter'],
			30:['AMZN','Amazon'],
			31:['FB','facebook'],
			32:['YHOO','Yahoo'],
			33:['AAPL', 'Apple'],
			34:['GPRO', 'Go Pro'],
			35:['INTC', 'Intel Corporation'],
			36:['NFLX', 'Netflix'],
			37:['TSLA', 'Tesla']
		}
stock_list = ['GOOG','TWTR', 'AMZN','FB','YHOO','AAPL','GPRO', 'INTC', 'NFLX', 'TSLA' ]
stock_name = ['Google','Twitter', 'Amazon','Facebook','Yahoo','Apple','Go Pro', 'Intel Corporation', 'Netflix', 'Tesla']

def search(request):
    stock = request.GET.get('put')
    print stock
    symbol = Share(stock)
    stock_data = symbol.get_historical('2016-01-01',date.today().strftime("%Y-%m-%d"))

    stock_df = pd.DataFrame(stock_data)
    temp = pd.DataFrame({'Close_Price':[],'Low':[],'High':[],'Date':[]})
    temp['Date'] = stock_df['Date']
    temp['High'] = stock_df['High']
    temp['Low'] = stock_df['Low']
    temp['Close_Price'] = stock_df['Adj_Close']
    print temp
    path = os.getcwd()
    filepath = path+os.sep+'static'+os.sep+'js'+os.sep+'search'
    os.chdir(filepath)
    temp.to_csv(filepath+"/result.csv",index_label=False,index=False)
    os.chdir(path)
    # print stock_data

    return render(request,'search2.html')

def searchpage(request):
	return render(request, 'searchpage.html')	 


def sidebar(request,company_id=0):
	if(company_id==0):

		context={

		}
	else:
		c_id = int (company_id)
		p = Company.objects.get(pk=company_id)
		print company[c_id][0]
		pred, last, tomorrow, today = rdu.regression_predict(company[c_id][0]+"_historical",15)
		svm_pred = rdu.svm_predict(company[c_id][0]+'_historical',15)
		ann_pred = rdu.ann_predict(company[c_id][0]+"_historical",15)

		if (pred-last>0): 
			delta = 1
		else: 
			delta = 0
		context = {
			'company_name':company[c_id],
			'individual':p,
			'today': today,
			'pred':pred,
			'last':last,
			'tomorrow':tomorrow,
			'delta': delta,
			'svm_pred':svm_pred,
			'ann_pred':ann_pred
		}
	return render(request, 'prediction.html', context) 

def homeindex(request,company_id=28):
	if(company_id==0):

		context={

		}
	else:
		c_id = int (company_id)
		p = Company.objects.get(pk=company_id) 
		avg, high, low, companies = query(company[c_id][0])
		real_time = rdu.get_realtime_data(stock_list)
		context = {
			'individual':p,
			'avg':avg,
			'high':high,
			'low':low,
			'companies':companies,
			'real_time':real_time,
			'stock_name':stock_name,
			'current_select':company[c_id][1]
		}
	return render(request, 'home.html', context) 


def sidebarhome(request,company_id=0):
	if(company_id==0):

		context={

		}
	else:
		c_id = int (company_id)
		p = Company.objects.get(pk=company_id) 
		avg, high, low, companies = query(company[c_id][0])
		real_time = rdu.get_realtime_data(stock_list)
		context = {
			'individual':p,
			'avg':avg,
			'high':high,
			'low':low,
			'companies':companies,
			'real_time':real_time,
			'stock_name':stock_name,
			'current_select':company[c_id][1]
		}
	print context
	return render(request, 'home.html', context) 

def indicator(request,company_id=0):
	if(company_id==0):

		context={

		}
	else:
		c_id = int (company_id)
		p = Company.objects.get(pk=company_id) 
		context = {
			'individual':p
		}
	return render(request, 'indicator.html', context) 


def query(name):
	tbl = rdu.get_data_db(name+'_historical')
	avg = rdu.getAverage(tbl)
	low = rdu.getLowest(tbl)
	high = rdu.getHighest(tbl)
	companies = rdu.getCompanies(name+'_historical')
	return avg, high, low, companies
