from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'books'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('<slug>/', views.one_book, name='one_book'),
    path('', views.all_books, name='all_books'),

]