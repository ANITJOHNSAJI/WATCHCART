from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.userlogin,name='userlogin'),
    path('signup',views.usersignup,name='usersignup'),
    path('index',views.index,name='index'),
    path('forgotpassword',views.getusername,name='forgotpassword'),
    path('verifyotp',views.verifyotp,name='verifyotp'),
    path('passwordreset',views.passwordreset,name='passwordreset'),
    path('logout',views.logoutuser,name="logout"),
    
]