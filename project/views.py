# File: views.py
# Author: Mohammed Murshid (murshidm@bu.edu), 12/9/2024
# Description: Creates views for the site

from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View, DeleteView
from .models import JobApplication, Account, Job, Company
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UpdateProfileForm, JobCreationForm, CreateAccountForm, InterviewForm, CompanyForm, ReviewForm, Review
from django.utils import timezone
from django.contrib import messages
from django.db.models import Q

# Create your views here.

# HomePageView - A view that displays all available job listings.
class HomePageView(ListView):
    """View to display a list of job applications."""
    model = Job  # Model representing job listings
    template_name = 'project/homepage.html'  # Template for displaying job listings
    context_object_name = 'jobs'  # Name of the context object passed to the template

    def get_queryset(self):
        """Return all jobs with flexible search options (by position, industry, or company)."""
        queryset = Job.objects.all()  # Fetch all jobs

        search_query = self.request.GET.get('search', '')  # Get the search query from the URL
        if search_query:
            # Apply filters based on search query (position, industry, or company name)
            queryset = queryset.filter(
                Q(position_title__icontains=search_query) |  # Search by job position
                Q(company__industry__icontains=search_query) |  # Search by company industry
                Q(company__name__icontains=search_query)  # Search by company name
            )

        return queryset  # Return the filtered queryset
    
# JobDetailView - A view that displays detailed information about a specific job.
class JobDetailView(DetailView):
    """View to display details of a specific job application."""
    model = Job  # Model for fetching a specific job
    template_name = 'project/job_detail.html'  # Template for displaying job details
    context_object_name = 'job'  # Name of the context object passed to the template

    def get_context_data(self, **kwargs):
        """Return context data for the job detail page, including application status."""
        context = super().get_context_data(**kwargs)
        job = self.get_object()  # Get the current job
        
        # Check if the user has already applied for this job
        if self.request.user.is_authenticated:
            user_account = get_object_or_404(Account, user=self.request.user)
            context['has_applied'] = JobApplication.objects.filter(
                user=user_account, job=job
            ).exists()  # Add information about whether the user has applied

        return context

# CreateAccountView - A view to create a new user account.
class CreateAccountView(CreateView):
    template_name = 'project/create_account.html'  # Template for the account creation page
    form_class = CreateAccountForm  # Form class for creating the user
    success_url = reverse_lazy('login')  # Redirect to the login page after successful account creation

    def form_valid(self, form):
        """Handle the form submission when it is valid."""
        # Save the user using the form data
        user = form.save()

        # Check if the email already exists in the Account model
        email = form.cleaned_data.get('email')
        if Account.objects.filter(email=email).exists():
            messages.error(self.request, "This email is already registered. Please use a different one.")
            return render(self.request, self.template_name, {'form': form})  # Return with error message

        # Create the Account model instance for the user
        account = Account.objects.create(user=user, username=user.username, email=email)
        account.save()  # Save the new account

        messages.success(self.request, "Account created successfully! You can now log in.")
        return redirect(self.success_url)  # Redirect to the login page

# UserProfileView - A view to display the profile page for the logged-in user.
class UserProfileView(LoginRequiredMixin, DetailView):
    """View to display the profile page with jobs applied to and created by the user."""
    model = Account  # Model for fetching the user's account
    template_name = 'project/user_profile.html'  # Template for the profile page
    context_object_name = 'account'  # Context variable name for the account

    def get_object(self):
        """Get the account object for the logged-in user."""
        return get_object_or_404(Account, user=self.request.user)  # Fetch the account based on logged-in user

    def get_context_data(self, **kwargs):
        """Add job applications and jobs created by the user to the context."""
        context = super().get_context_data(**kwargs)
        user_account = self.get_object()  # Get the user's account object

        # Jobs applied to
        context['applied_jobs'] = JobApplication.objects.filter(user=user_account)

        # Jobs created by the user
        context['created_jobs'] = Job.objects.filter(created_by=self.request.user)

        # Provide the email and resume update form to the template
        context['email_form'] = UpdateProfileForm(instance=user_account)
        
        return context

# UpdateProfileView - A view to update the user's profile (email, resume).
class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = Account  # Model for the user's account
    form_class = UpdateProfileForm  # Form for updating the user's email and resume
    template_name = 'project/update_profile.html'  # Template for the profile update page
    
    def get_object(self):
        """Get the Account object for the logged-in user."""
        return get_object_or_404(Account, user=self.request.user)

    def get_success_url(self):
        """Redirect to the user's profile page after updating."""
        return reverse_lazy('user_profile')

# ApplyToJobView - A view for handling the job application process.
class ApplyToJobView(LoginRequiredMixin, View):
    """Handle the job application process."""
    
    def post(self, request, job_id):
        """Handle the application process for a specific job."""
        # Get the job instance
        job = get_object_or_404(Job, pk=job_id)
        
        # Create a new job application for the logged-in user
        user_account = get_object_or_404(Account, user=request.user)
        
        # Check if the user has already applied for this job (optional)
        if JobApplication.objects.filter(user=user_account, job=job).exists():
            return redirect('job_detail', pk=job_id)  # Redirect to job detail if already applied
        
        # Create and save the new job application
        job_application = JobApplication(
            user=user_account,
            job=job,
            application_date=timezone.now(),
            status='applied',
        )
        job_application.save()
        
        return redirect('user_profile')  # Redirect to user profile after application

# CreateJobView - A view to create a new job posting.
class CreateJobView(LoginRequiredMixin, CreateView):
    model = Job  # Model for creating a new job
    form_class = JobCreationForm  # Form for creating the job
    template_name = 'project/create_job.html'  # Template for creating a job
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user  # Associate the job with the logged-in user
        return super().form_valid(form)
    
    def get_success_url(self):
        """Redirect to the user's profile page after job creation."""
        return reverse_lazy('user_profile')

# JobApplicationsForJobView - A view to display all applications for a specific job.
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
            return redirect('homepage')  # Redirect if the user is not the job creator
        return context

# ScheduleInterviewView - A view to schedule an interview for a job applicant.
class ScheduleInterviewView(View):
    def get(self, request, job_application_id):
        """Display the interview scheduling form."""
        job_application = get_object_or_404(JobApplication, pk=job_application_id)

        # Only allow the job creator to schedule an interview
        if job_application.job.created_by == request.user:
            form = InterviewForm()
            return render(request, 'project/schedule_interview.html', {'form': form, 'job_application': job_application})

        return redirect('homepage')

    def post(self, request, job_application_id):
        """Handle interview form submission."""
        job_application = get_object_or_404(JobApplication, pk=job_application_id)

        if job_application.job.created_by == request.user:
            form = InterviewForm(request.POST)
            if form.is_valid():
                interview = form.save(commit=False)
                interview.job_application = job_application
                interview.save()

                # Update job application status to "interview"
                job_application.status = 'interview'
                job_application.save()

                return redirect('job_detail', pk=job_application.job.pk)

        return redirect('homepage')  # Redirect if user is not authorized to schedule an interview

# WithdrawApplicationView - A view to allow users to withdraw their job application.
class WithdrawApplicationView(View):
    def post(self, request, pk):
        """Withdraw the user's job application."""
        application = get_object_or_404(JobApplication, pk=pk)
        application.delete()  # Delete the job application

        return redirect('user_profile')  # Redirect to the user's profile after withdrawal

# CompanyListView - A view to display all companies.
class CompanyListView(ListView):
    model = Company  # Model for listing companies
    template_name = 'project/company_list.html'  # Template for listing companies
    context_object_name = 'companies'  # Context variable name for the list of companies

# CreateCompanyView - A view to create a new company.
class CreateCompanyView(LoginRequiredMixin, CreateView):
    model = Company  # Model for creating a company
    form_class = CompanyForm  # Form class for creating a company
    template_name = 'project/create_company.html'  # Template for creating a company
    success_url = reverse_lazy('company_list')  # Redirect to the company list after successful creation

    def form_valid(self, form):
        """Handle form submission when it's valid."""
        return super().form_valid(form)

# OfferOrRejectApplicationView - A view to allow job creators to offer or reject applicants.
class OfferOrRejectApplicationView(LoginRequiredMixin, View):
    """View to allow job creator to offer or reject an applicant.""" 
    
    def post(self, request, application_id, action):
        application = get_object_or_404(JobApplication, pk=application_id)
        
        # Ensure the user is the job creator
        if application.job.created_by != request.user:
            return redirect('homepage')

        if action == 'offer':
            application.status = 'offer'  # Set application status to 'offer'
        elif action == 'reject':
            application.status = 'rejected'  # Set application status to 'rejected'
        
        application.save()  # Save the updated application status
        return redirect('job_applications_for_job', pk=application.job.pk)  # Redirect to job applications page

# DeleteJobView - A view to delete a job posting.
class DeleteJobView(LoginRequiredMixin, DeleteView):
    model = Job  # Model for deleting a job
    template_name = 'project/job_confirm_delete.html'  # Template for confirming job deletion
    context_object_name = 'job'  # Context variable for the job to be deleted
    success_url = reverse_lazy('user_profile')  # Redirect to user's profile after deletion

    def get_object(self):
        """Override to ensure that only the job created by the current user can be deleted."""
        job = get_object_or_404(Job, pk=self.kwargs['pk'])
        return job

# CompanyDetailView - A view to display detailed information about a company.
class CompanyDetailView(DetailView):
    model = Company  # Model for fetching a specific company
    template_name = 'project/company_detail.html'  # Template for displaying company details
    context_object_name = 'company'  # Context variable for the company

    def get_context_data(self, **kwargs):
        """Return context data for the company detail page, including reviews."""
        context = super().get_context_data(**kwargs)
        
        # Get reviews for the company
        context['reviews'] = Review.objects.filter(company=self.object)
        
        # If the user is logged in, add the review form to the context
        if self.request.user.is_authenticated:
            context['review_form'] = ReviewForm()

        return context

    def post(self, request, *args, **kwargs):
        """Handle review form submission for a company."""
        company = self.get_object()  # Get the company being viewed
        form = ReviewForm(request.POST)

        if form.is_valid():
            # Create a review for the company
            review = form.save(commit=False)
            review.user = request.user  # Set the logged-in user as the review author
            review.company = company  # Link the review to the company
            review.save()

            # Redirect to the same page to refresh and show the new review
            return redirect('company_detail', pk=company.pk)

        # If the form is not valid, render the page again with the form errors
        return self.render_to_response({'form': form})