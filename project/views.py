from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
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
    model = Job
    template_name = 'project/job_detail.html'
    context_object_name = 'job'

    def get_queryset(self):
        """Return the specific job based on its ID (pk)."""
        return Job.objects.select_related('company')

class CreateAccountView(CreateView):
    template_name = 'project/create_account.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        account = Account.objects.create(user=user, username=user.username, email=user.email)
        account.save()

        return redirect(self.success_url)

class UserProfileView(LoginRequiredMixin, DetailView):
    """View to display the profile page with jobs applied to and created by the user."""
    model = Account
    template_name = 'project/user_profile.html'
    context_object_name = 'account'

    def get_object(self):
        """Get the account object for the logged-in user."""
        return get_object_or_404(Account, user=self.request.user)

    def get_context_data(self, **kwargs):
        """Add job applications and jobs created by the user to the context."""
        context = super().get_context_data(**kwargs)
        user_account = self.get_object()

        # Jobs applied to
        context['applied_jobs'] = JobApplication.objects.filter(user=user_account)

        # Jobs created by the user
        context['created_jobs'] = Job.objects.filter(created_by=self.request.user)

        # Provide the email and resume update form to the template
        context['email_form'] = UpdateProfileForm(instance=user_account)
        
        return context

class UpdateProfileForm(forms.ModelForm):
    """Form to update the user's email and resume."""
    class Meta:
        model = Account
        fields = ['email', 'resume']

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

class ApplyToJobView(LoginRequiredMixin, View):
    """View to handle job applications."""
    
    def post(self, request, job_id):
        # Get the job object
        job = get_object_or_404(Job, pk=job_id)
        
        # Create a job application for the logged-in user
        job_application = JobApplication.objects.create(
            user=request.user.account,
            job=job,
            status='applied',
            application_date=request.POST.get('application_date')
        )
        
        return redirect('user_profile')

