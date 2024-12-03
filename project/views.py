from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from .models import JobApplication

# Create your views here.

class HomePageView(ListView):
    """View to display a list of job applications."""
    model = JobApplication
    template_name = 'project/homepage.html'
    context_object_name = 'job_applications'

    def get_queryset(self):
        """Return all job applications."""
        return JobApplication.objects.select_related('company')  # Optimize by selecting related companies


class JobDetailView(DetailView):
    """View to display details of a specific job application."""
    model = JobApplication
    template_name = 'project/job_detail.html'
    context_object_name = 'job'

    def get_queryset(self):
        """Include company details for the job."""
        return JobApplication.objects.select_related('company')


