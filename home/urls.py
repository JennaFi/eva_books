from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [

    path('', views.index, name='index'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('search/', views.search, name='search'),

]