from django.urls import path
from . import views

urlpatterns = [
    path('', views.calc, name='calc'),
    path('newcalc/', views.new_calc, name='new_calc'),
]
