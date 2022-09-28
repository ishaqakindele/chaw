from os import name
from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name='index'),
    path('password_reset', password_reset_request, name= 'password_reset'),
    path('contact', contact, name='contact'),
    path('all_food', all_food, name='all_food'),
    path('categories', categories, name='categories'),
    path('detail/<str:id>', detail, name='detail'),
    path('category/<str:id>', single_category, name='category'),
    path('signout', signout, name='signout'),
    path('signin', signin, name='signin'),
    path('signup', signup, name='signup'),
    path('dashboard', dashboard, name='dashboard'),
    path('profileupdate', profileupdate, name='profileupdate'),
    path('passwordupdate', passwordupdate, name='passwordupdate'),
    path('ordermeal', ordermeal, name='ordermeal'),
    path('mycart', mycart, name='mycart'),
    path('deletemeal', deletemeal, name='deletemeal'),
    path('deleteallmeal', deleteallmeal, name='deleteallmeal'),
    path('checkout', checkout, name='checkout'),
    path('payment', payment, name='payment'),
    path('decrease', decrease, name='decrease'),
    path('increase', increase, name='increase'),
    path('completed', completed, name='completed'),

]