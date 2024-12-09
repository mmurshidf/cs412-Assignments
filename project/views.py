from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from django.contrib.auth.forms import UserCreationForm
from .models import JobApplication, Account, Job
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from.forms import UpdateProfileForm, JobCreationForm
from django.utils import timezone

# Create your views here.

class HomePageView(ListView):
    """View to display a list of job applications."""
    model = Job
    template_name = 'project/homepage.html'
    context_object_name = 'jobs'

    def get_queryset(self):
        """Return all jobs created by users."""
        return Job.objects.all()

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
    """Handle the job application process."""
    
    def post(self, request, job_id):
        # Get the job instance
        job = get_object_or_404(Job, pk=job_id)
        
        # Create a new job application for the logged-in user
        user_account = get_object_or_404(Account, user=request.user)
        
        # Check if the user has already applied for this job (optional)
        if JobApplication.objects.filter(user=user_account, job=job).exists():
            return redirect('job_detail', pk=job_id)  # Or render a message saying "Already Applied"
        
        job_application = JobApplication(
            user=user_account,
            job=job,
            application_date=timezone.now(),
            status='applied',
        )
        job_application.save()
        
        return redirect('user_profile')

class CreateJobView(LoginRequiredMixin, CreateView):
    model = Job
    form_class = JobCreationForm
    template_name = 'project/create_job.html'
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user  # Associate the job with the logged-in user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('user_profile')
    
class JobApplicationsForJobView(DetailView):
    """View to display all applications for a specific job."""
    model = Job
    template_name = 'project/job_applications_for_job.html'
    context_object_name = 'job'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job = self.get_object()

        # Check if the user is the job creator
        if self.request.user == job.created_by:
            job_applications = JobApplication.objects.filter(job=job)
            context['job_applications'] = job_applications
        else:
            # Redirect or show a message if the user is not the job creator
            return redirect('homepage')  # Or you can show a "not authorized" message
        return context

