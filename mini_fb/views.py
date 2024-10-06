# File: views.py
# Author: Mohammed Murshid (murshidm@bu.edu), 10/6/2024
# Description: Creates views for site

from django.shortcuts import render
from django.views.generic import ListView
from .models import Profile

# Create your views here.

class ShowAllProfilesView(ListView):
    """View for show_all_profiles"""
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'
