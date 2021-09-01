from django.urls import path
from . import views


urlpatterns = [
    path('review_and_rate/',views.review_and_rate, name='review_and_rate' ),


    
    
]