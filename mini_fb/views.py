# File: views.py
# Author: Mohammed Murshid (murshidm@bu.edu), 10/6/2024
# Description: Creates views for site

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Profile, StatusMessage
from django.urls import reverse_lazy, reverse
from .forms import CreateProfileForm, CreateStatusMessageForm

# Create your views here.

class ShowAllProfilesView(ListView):
    """View for show_all_profiles"""
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'

class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'

class CreateProfileView(CreateView):
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'
    success_url = reverse_lazy('show_all_profiles')

class CreateStatusMessageView(CreateView):
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        context['profile'] = profile
        return context

    def form_valid(self, form):
        profile = Profile.objects.get(pk=self.kwargs['pk'])  # Look up the Profile object by pk
        status_message = form.save(commit=False)
        status_message.profile = profile  # Attach the Profile object to the StatusMessage
        status_message.save()
        return super().form_valid(form)  # Save the StatusMessage and return
    
    def get_success_url(self):
        profile = Profile.objects.get(pk=self.kwargs['pk'])  # Get the profile by pk
        return reverse('show_profile', kwargs={'pk': profile.pk})  # Redirect to profile page
