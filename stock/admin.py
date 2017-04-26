from django.contrib import admin
from .models import Company
from django.apps import AppConfig


class CompanyAdmin(admin.ModelAdmin):
	list_display= ["__str__", "date", "closing_price","predicted_price", "difference", "previous_closing_price"]
	

# class DateAdmin(admin.ModelAdmin):
# 	list_display= ["date_added"]
	
admin.site.register(Company)
# admin.site.register(Date, DateAdmin)
