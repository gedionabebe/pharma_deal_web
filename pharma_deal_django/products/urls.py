from django.urls import path
from . import views

urlpatterns = [
    path('browse/',views.browse, name='browse' ),
    path('create/',views.create, name='create' ),
    path('update/<int:product_id>/',views.update, name='update' ),
    path('delete/<int:product_id>/',views.delete, name='delete' ),
    path('inventory/',views.inventory, name='inventory' ),
    path('search/',views.search, name='search' ),
    path('filters/', views.filters, name='filters'),
    path('single_product/<int:product_id>/', views.single_product, name='single_product'),


    
    
]