from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('post_create/', views.post_create, name='post_create'),
    path('check/', views.check, name='check'),
    path('post_check/', views.post_check, name='post_check'),
    path('accept/', views.accept,name='accept'),
    path('decline/', views.decline,name='decline'),
    path('cart/', views.cart,name='cart'),
    path('cart_check/', views.cart_check,name='cart_check'),
]