# File: urls.py
# Author: Mohammed Murshid (murshidm@bu.edu), 10/6/2024
# Description: Urls file for pathing

from django.urls import path
from django.conf import settings
from .views import ShowAllProfilesView, ShowProfilePageView

#Url pathing

urlpatterns = [
    path('', ShowAllProfilesView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>/', ShowProfilePageView.as_view(), name='show_profile'),
]