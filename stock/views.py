from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from  . import data
from  . import data1
from datetime import datetime
from django.utils import timezone
# Create your views here.
#from .models import Today
from . models import Company
from .models import Nepse
from . import analyzer
import json_, sqlite3
from decimal import Decimal
import retrieve_data_update as rdu
#from .stock import neuralNetwork

company =  {28:['GOOG','Google'],
			29:['TWTR','Twitte'],
			30:['AMZN','Amazon'],
			31:['FB','facebook'],
			32:['YHOO','Yahoo'],
			33:['AAPL', 'Apple'],
			34:['GPRO', 'Go Pro'],
			35:['INTC', 'Intc'],
			36:['NFLX', 'Netflix'],
			37:['TSLA', 'Tesla']
		}

def analysis(request):
	data.bank_data.reverse()
	data.devbank_data.reverse()
	data.finance_data.reverse()
	data.hotel_data.reverse()
	data.hydropower_data.reverse()
	data.insurance_data.reverse()
	data.nepse_data.reverse()
	data.others_data.reverse()
	context={
	'bank_data':data.bank_data,
	'devbank_data':data.devbank_data,
	'finance_data':data.finance_data,
	'hotel_data':data.hotel_data,
	'hydropower_data':data.hydropower_data,
	'insurance_data':data.insurance_data,
	'nepse_data':data.nepse_data,
	'others_data':data.others_data
	}
	return render(request, 'khatra.html', context)	 


def sidebar(request,company_id=0):
	if(company_id==0):

		context={

		}
	else:
		c_id = int (company_id)
		p = Company.objects.get(pk=company_id)
		print company[c_id][0]
		pred, last, tomorrow, today = rdu.regression_predict(company[c_id][0]+"_historical",15)
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
			'delta': delta
		}
	return render(request, 'prediction.html', context) 

def homeindex(request,company_id=28):
	if(company_id==0):

		context={

		}
	else:
		c_id = int (company_id)
		p = Company.objects.get(pk=company_id) 
		context = {
			'individual':p,
		}
	return render(request, 'home.html', context) 


def sidebarhome(request,company_id=0):
	if(company_id==0):

		context={

		}
	else:
		c_id = int (company_id)
		p = Company.objects.get(pk=company_id) 
		query(company[c_id][0]) 
		context = {
			'individual':p,

		}
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

def make_company_prediction(c_id):
	close_prediction = []
	close_prediction = analyzer.analyzeId(c_id)
	cls_price = Company.objects.get(pk = c_id)
	cls_price.predicted_price= int(close_prediction[0])
	
	if ((cls_price.predicted_price - cls_price.previous_closing_price)>0):
		cls_price.increased_bool = True 
	cls_price.save()

def query(name):
	tbl = rdu.get_data_db(name+'_historical')
	avg = rdu.getAverage(tbl)
	low = rdu.getLowest(tbl)
	high = rdu.getHighest(tbl)
	companies = rdu.getCompanies(name+'_historical')
	print avg, high, low, companies
