## restaurant/urls.py
## description: URL patterns for the restaurant app

from django.urls import path
from django.conf import settings
from . import views

# all of the URLs that are part of this app
urlpatterns = [
    path('main/', views.main, name='main'),
    path('order/', views.order, name='order'),
    path('confirmation/', views.confirmation, name='confirmation'),
]