"""minor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin
from django.views.generic.base import TemplateView
from stock.views import home, analysis, sidebar,previous_prediction, previous_nepse_prediction, about#, details2, details3, details4o
import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', home, name='home1'),
    url(r'^analysis/', analysis, name='khatra'),
    url(r'^prediction/(?P<company_id>[0-9]+)$', sidebar, name ='prediction'),
    url(r'^previous_prediction/(?P<company_id>[0-9]+)$', previous_prediction, name ='previous_prediction'),
    url(r'^previous_nepse_prediction/', previous_nepse_prediction, name ='previous_nepse_prediction'),
    # url(r'^adb/', details2, name='adblana'),
    # url(r'^plic/', details3, name='plicanalysis'),
    # url(r'^nlic/', details4, name='nlicanalysis'),
    url(r'^prediction/', sidebar, name='prediction'),
    url(r'^about/', about, name='about'),
]
if settings.DEBUG:
    urlpatterns += (
        url(r'^500/$', TemplateView.as_view(template_name="404.html")),
        url(r'^404/$', TemplateView.as_view(template_name="404.html")),
    )
