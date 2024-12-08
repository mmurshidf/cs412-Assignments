from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.forms import UserCreationForm
from .models import JobApplication, Account, Job
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms

# Create your views here.

class HomePageView(ListView):
    """View to display a list of job applications."""
    model = Job  # Use the Job model to display job listings
    template_name = 'project/homepage.html'
    context_object_name = 'jobs'  # Context name is now 'jobs'

    def get_queryset(self):
        """Return all jobs available to apply to."""
        return Job.objects.all()  # Fetch all jobs available for users


class JobDetailView(DetailView):
    """View to display details of a specific job application."""
    model = JobApplication
    template_name = 'project/job_detail.html'
    context_object_name = 'job'

    def get_queryset(self):
        """Include company details for the job."""
        return JobApplication.objects.select_related('company')

class CreateAccountView(CreateView):
    template_name = 'project/create_account.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        account = Account.objects.create(user=user, username=user.username, email=user.email)
        account.save()

        return redirect(self.success_url)

class UserProfileView(LoginRequiredMixin, ListView):
    """Display profile with the job applications of the logged-in user."""
    model = JobApplication
    template_name = 'project/user_profile.html'
    context_object_name = 'job_applications'

    def get_queryset(self):
        """Return all job applications for the logged-in user."""
        user_account = get_object_or_404(Account, user=self.request.user)
        return JobApplication.objects.filter(user=user_account)

    def get_login_url(self):
        return reverse_lazy('login')

class UpdateProfileForm(forms.ModelForm):
    """Form to update the user's email."""
    class Meta:
        model = Account
        fields = ['email']


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = Account
    form_class = UpdateProfileForm
    template_name = 'project/update_profile.html'
    
    def get_object(self):
        """Get the Account object for the logged-in user."""
        return get_object_or_404(Account, user=self.request.user)

    def get_success_url(self):
        """Redirect to the user's profile page after updating."""
        return reverse_lazy('user_profile')

