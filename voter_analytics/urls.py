# File: urls.py
# Author: Mohammed Murshid (murshidm@bu.edu), 11/11/2024
# Description: Urls file for pathing

from django.urls import path
from .views import VoterListView, VoterDetailView, GraphOverviewView

urlpatterns = [
    path('', VoterListView.as_view(), name='voters'),
    path('voter/<int:pk>/', VoterDetailView.as_view(), name='voter'),
    path('graphs/', GraphOverviewView.as_view(), name='graphs'),
]