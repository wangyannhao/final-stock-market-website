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
from stock.views import homeindex,searchpage, sidebar , indicator, sidebarhome, search
import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', homeindex, name='home'),
    url(r'^home/(?P<company_id>[0-9]+)$', sidebarhome, name ='home'),
    url(r'^prediction/(?P<company_id>[0-9]+)$', sidebar, name ='prediction'),
    url(r'^indicator/(?P<company_id>[0-9]+)$', indicator, name ='indicator'),
    url(r'^indicator/',indicator,name='indicator'),
    url(r'^prediction/', sidebar, name='prediction'),
    url(r'^searchpage/', searchpage, name='searchpage'),
    url(r'^search/$',search, name = 'search'),
]
if settings.DEBUG:
    urlpatterns += (
        url(r'^500/$', TemplateView.as_view(template_name="404.html")),
        url(r'^404/$', TemplateView.as_view(template_name="404.html")),
    )
