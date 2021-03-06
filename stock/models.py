from django.db import models
from django.utils import timezone

#Create your models here.
# class Date (models.Model):
# 	date_added = models.DateField(auto_now_add=True, auto_now=False)
# 	def __str__(self):
# 		return str(self.date_added)

class Company(models.Model):
	name = models.CharField(max_length= 50)
	abbr = models.CharField(max_length= 10)
	#date =  models.ForeignKey(Date, on_delete=models.CASCADE)
	date = models.DateField(auto_now_add=True, auto_now=False)
	closing_price = models.IntegerField(default=0)
	predicted_price = models.IntegerField(default=0)
	difference = models.IntegerField(default = 0)
	yesterday_date = models.DateField(auto_now_add = True, auto_now = False)
	previous_closing_price = models.IntegerField(default = 0)
	increased_bool = models.BooleanField(default = False)
	def __str__(self):
		return self.abbr

