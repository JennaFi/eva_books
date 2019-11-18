from django.urls import path, re_path
from . import views

app_name = 'authors'

urlpatterns = [


    path('<slug>/', views.one_author, name='one_author'),
    path('', views.all_authors, name='author_list'),
]