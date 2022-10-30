from django.urls import path

from .views import  logoutPage, register, loginPage, account

urlpatterns = [
    path('my-accont/', account, name='account'),
    path('login/', loginPage, name='login'),
    path('register/', register, name='register'),
    path('logout/', logoutPage, name='logout'),
]
