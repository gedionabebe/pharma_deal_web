"""pharma_deal_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include, path
from authentication import views
from authentication.views import *
from django.views.static import serve
from django.conf.urls import url

urlpatterns = [
    path('', views.login, name='login'),
    path('authentication/', include('authentication.urls')),
    path('products/', include('products.urls')),
    path('admin/', admin.site.urls),
    path('profile/', include('profile.urls')),
    path('transaction/', include('transaction.urls')),
    path('review_and_rate/', include('review_and_rate.urls')),
    url(r'^media/(?P<path>.*)$', serve,{'document_root':       settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
]
