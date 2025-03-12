from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from eapp import views

urlpatterns = [
    path('', views.userlogin,name='userlogin'),
    path('signup',views.usersignup,name='usersignup'),
    path('index',views.index,name='index'),
    path('forgotpassword',views.getusername,name='forgotpassword'),
    path('verifyotp',views.verifyotp,name='verifyotp'),
    path('passwordreset',views.passwordreset,name='passwordreset'),
    path('logout/', views.logoutuser, name="logout"),
    path('category',views.category,name="category"),
    path('bookings',views.bookings,name="bookings"),
    path('edit/<int:id>/', views.edit_g, name='edit_g'),
    path('add/', views.add_product, name='add'),
    path('firstpage/', views.first_page, name='firstpage'),
    path('product/<int:id>/', views.product, name='product'),

    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)