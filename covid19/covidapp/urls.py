from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls import url


urlpatterns = [
    path('dev/',views.dev,name='dev'),
    path('',views.api,name='api'),
    path('api/global/',views.globalview,name='globalview'),
    path('api/statewise/',views.statewise,name='statewise'),
    path('api/statewise/state/<sname>/',views.stateview,name='stateview'),
    path('api/countrywise/country/<code>/',views.countryview,name='countryview'),
    path('api/statewise/search/',views.statesearch,name='statesearch'),
    path('api/helpline/',views.Helpline,name='Helpline'),
    path('api/about', views.about, name='about')
    
]
