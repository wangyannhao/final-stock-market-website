from django.contrib import admin
from .models import Company
from django.apps import AppConfig
from .models import Nepse

class CompanyAdmin(admin.ModelAdmin):
	list_display= ["__str__", "date", "closing_price","predicted_price", "difference", "previous_closing_price"]
	
class NepseAdmin(admin.ModelAdmin):
	list_display= ["date", "index","predicted_index", "difference", "previous_index"]

# class DateAdmin(admin.ModelAdmin):
# 	list_display= ["date_added"]
	
admin.site.register(Company, CompanyAdmin)
# admin.site.register(Date, DateAdmin)
admin.site.register(Nepse, NepseAdmin)
#admin.site.register(Nepse)
