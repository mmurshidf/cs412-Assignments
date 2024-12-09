from django.shortcuts import get_object_or_404, redirect,render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View, DeleteView
from .models import JobApplication, Account, Job, Company
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from.forms import UpdateProfileForm, JobCreationForm, CreateAccountForm, InterviewForm, CompanyForm, ReviewForm, Review
from django.utils import timezone
from django.contrib import messages


# Create your views here.

class HomePageView(ListView):
    """View to display a list of job applications."""
    model = Job
    template_name = 'project/homepage.html'
    context_object_name = 'jobs'

    def get_queryset(self):
        search_query = self.request.GET.get('search', '')  # Get the search query from the request
        if search_query:
            # Filter jobs by position title that contains the search term
            return Job.objects.filter(position_title__icontains=search_query)
        return Job.objects.all()
    
class JobDetailView(DetailView):
    """View to display details of a specific job application."""
    model = Job
    template_name = 'project/job_detail.html'
    context_object_name = 'job'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job = self.get_object()  # Get the current job
        
        # Check if the user has already applied for this job
        if self.request.user.is_authenticated:
            user_account = get_object_or_404(Account, user=self.request.user)
            context['has_applied'] = JobApplication.objects.filter(
                user=user_account, job=job
            ).exists()

        return context

class CreateAccountView(CreateView):
    template_name = 'project/create_account.html'
    form_class = CreateAccountForm
    success_url = reverse_lazy('login')  # Redirect to login page after successful account creation

    def form_valid(self, form):
        # Save the user using the form data
        user = form.save()

        # Check if the email already exists in the Account model
        email = form.cleaned_data.get('email')
        if Account.objects.filter(email=email).exists():
            messages.error(self.request, "This email is already registered. Please use a different one.")
            return render(self.request, self.template_name, {'form': form})

        # Create the Account model instance for the user
        account = Account.objects.create(user=user, username=user.username, email=email)
        account.save()

        messages.success(self.request, "Account created successfully! You can now log in.")
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
            return redirect('homepage')
        return context

class ScheduleInterviewView(View):
    def get(self, request, job_application_id):
        # Get the job application the interview is for
        job_application = get_object_or_404(JobApplication, pk=job_application_id)

        # Only allow the creator of the job to schedule an interview
        if job_application.job.created_by == request.user:
            form = InterviewForm()
            return render(request, 'project/schedule_interview.html', {'form': form, 'job_application': job_application})

        # If the user is not the creator, return error or redirect
        return redirect('homepage')

    def post(self, request, job_application_id):
        job_application = get_object_or_404(JobApplication, pk=job_application_id)

        if job_application.job.created_by == request.user:
            form = InterviewForm(request.POST)
            if form.is_valid():
                # Save the interview form with the job_application set
                interview = form.save(commit=False)
                interview.job_application = job_application  # Associate with the job application
                interview.save()

                # Update the status of the job application to "interview"
                job_application.status = 'interview'
                job_application.save()

                # Redirect to the job detail or interview page
                return redirect('job_detail', pk=job_application.job.pk)

        return redirect('homepage')


class WithdrawApplicationView(View):
    def post(self, request, pk):
        # Get the JobApplication using the pk
        application = get_object_or_404(JobApplication, pk=pk)
        
        # Delete the application
        application.delete()

        # Redirect to the user's profile page after deletion
        return redirect('user_profile')

class CompanyListView(ListView):
    model = Company
    template_name = 'project/company_list.html'  # Template for listing companies
    context_object_name = 'companies'

class CreateCompanyView(LoginRequiredMixin, CreateView):
    model = Company
    form_class = CompanyForm
    template_name = 'project/create_company.html'
    success_url = reverse_lazy('company_list')

    def form_valid(self, form):
        return super().form_valid(form)

class OfferOrRejectApplicationView(LoginRequiredMixin, View):
    """View to allow job creator to offer or reject an applicant."""
    
    def post(self, request, application_id, action):

        application = get_object_or_404(JobApplication, pk=application_id)
        

        if application.job.created_by != request.user:
            return redirect('homepage')  
        

        if action == 'offer':
            application.status = 'offer'
        elif action == 'reject':
            application.status = 'rejected'
        
        application.save()
        return redirect('job_applications_for_job', job_id=application.job.id)

class DeleteJobView(LoginRequiredMixin, DeleteView):
    model = Job
    template_name = 'project/job_confirm_delete.html'  # A confirmation page before deletion
    context_object_name = 'job'
    success_url = reverse_lazy('user_profile')  # Redirect to the user's profile page after deletion

    def get_object(self):
        """Override to ensure that only the job created by the current user can be deleted."""
        job = get_object_or_404(Job, pk=self.kwargs['pk'])
        return job

class CompanyDetailView(DetailView):
    model = Company
    template_name = 'project/company_detail.html'
    context_object_name = 'company'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get reviews for the company
        context['reviews'] = Review.objects.filter(company=self.object)
        
        # If the user is logged in, add the review form to the context
        if self.request.user.is_authenticated:
            context['review_form'] = ReviewForm()

        return context

    def post(self, request, *args, **kwargs):
        company = self.get_object()  # Get the company being viewed
        form = ReviewForm(request.POST)

        if form.is_valid():
            # Create a review for the company
            review = form.save(commit=False)
            review.user = request.user  # Set the logged-in user as the review author
            review.company = company  # Link the review to the company
            review.save()

            # Redirect to the same page (refresh the page to show the new review)
            return redirect('company_detail', pk=company.pk)

        # If the form is not valid, render the page again with the form errors
        return self.render_to_response({'form': form})