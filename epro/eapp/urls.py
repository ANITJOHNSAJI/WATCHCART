from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from eapp import views

urlpatterns = [
    path('userlogin', views.userlogin,name='userlogin'),
    path('signup',views.usersignup,name='usersignup'),
    path('',views.index,name='index'),
    path('forgotpassword',views.getusername,name='forgotpassword'),
    path('verifyotp',views.verifyotp,name='verifyotp'),
    path('passwordreset',views.passwordreset,name='passwordreset'),
    path('logout/', views.logoutuser, name="logout"),
    path('category',views.category,name="category"),
    path('bookings',views.bookings,name="bookings"),
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:id>/', views.edit_g, name='edit_g'),
    path('delete/<int:id>/', views.delete_g, name='delete_g'),
    path('firstpage/', views.first_page, name='firstpage'),
    path('product/<int:id>/', views.product, name='product'),
    path('add_to_cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart_view'),
    path('increment_cart/<int:id>/', views.increment_cart, name='increment_cart'),
    path('decrement_cart/<int:id>/', views.decrement_cart, name='decrement_cart'),
    path('delete_cart_item/<int:id>/', views.delete_cart_item, name='delete_cart_item'),
    path('checkout/', views.checkout, name='checkout'),

    
]

