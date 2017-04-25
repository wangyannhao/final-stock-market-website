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

#from .stock import neuralNetwork

def home(request):
	conn = sqlite3.connect('nepse_only.sqlite3')
	c = conn.cursor()  
	def read_form_db():
		c.execute('SELECT * FROM alldata')    
		data=c.fetchall()
		return (data)
	list_data = read_form_db()
	list_data.reverse()
	data1.neps_data.reverse()
	#make_nepse_prediction(list_data)
	c = Nepse.objects.all()
	#c.difference = c.index - c.predicted_index

	object_recent = Nepse.objects.order_by('-date')[0]
	#print (object_recent)
	#object_old = Nepse.objects.order_by('-date')[1:3]
	context={
	#'q2':object_old,
	'q1': object_recent,
	'neps_data':data1.neps_data
	}
	
	return render(request, 'home1.html', context) 

def make_nepse_prediction(list_data):
	nepse_prediction = []
	nepse_prediction = analyzer.analyzeId(0)
	nep_price = Nepse( predicted_index= nepse_prediction[0], previous_index = list_data[0][0], difference= index- predicted_index)	
	
	if ((nep_price.predicted_index - nep_price.previous_index)>0):
		nep_price.increased_bool = True 
	nep_price.save()

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
		
		#c.difference = c.closing_price - c.predicted_price
		#make_company_prediction(c_id)	
		p = Company.objects.get(pk=company_id) 
		#c = Company.objects.all().order_by('-date').filter(abbr__exact = p.abbr)
		context = {
			'individual':p
		}
	return render(request, 'prediction.html', context) 

def make_company_prediction(c_id):
	close_prediction = []
	close_prediction = analyzer.analyzeId(c_id)
	cls_price = Company.objects.get(pk = c_id)
	cls_price.predicted_price= int(close_prediction[0])
	
	if ((cls_price.predicted_price - cls_price.previous_closing_price)>0):
		cls_price.increased_bool = True 
	cls_price.save()

def previous_prediction(request,company_id):
	p = Company.objects.get(pk=company_id)
	pre = Company.objects.all().order_by('-date').filter(abbr__exact = p.abbr)
	context = {
		'query':pre,
		'given':p
	}
	return render(request, 'previous_prediction.html', context) 

def previous_nepse_prediction(request):
	pre = Nepse.objects.all().order_by('-date')
	context = {
		'query':pre
	}
	return render(request, 'previous_nepse_prediction.html', context) 

def about(request):
	context = {
		
	}
	return render(request, 'about.html', context) 
