# File: models.py
# Author: Mohammed Murshid (murshidm@bu.edu), 11/21/2024
# Description: Models file to for final project/job application app

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# User model that represents a user by giving them a username, email, and profile, first name, and last name
class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="accounts", default=1)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    profile = models.TextField(blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)

    def __str__(self):
        return self.username
    
#Company model that represents the company by its name, industry, and location
class Company(models.Model):
    name = models.CharField(max_length=100)
    industry = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Jobs model to represent job listings posted by companies
class Job(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    position_title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    industry = models.CharField(max_length=100)
    posted_date = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_jobs", default=1)

    def __str__(self):
        return f"{self.position_title} at {self.company.name}"

    def get_job_details_url(self):
        """Get the URL to view the job details."""
        return f"/project/job/{self.pk}/"


#Job application status model
class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('interview', 'Interview'),
        ('offer', 'Offer'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, default=1)
    application_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.user.username} applied for {self.job.position_title}"



#Interview Model to track interviews
class Interview(models.Model):

    #Fields
    job_application = models.ForeignKey(JobApplication, on_delete=models.CASCADE)
    interview_date = models.DateField()
    interviewer_name = models.CharField(max_length=100)
    feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Interview for {self.job_application.position_title} on {self.interview_date}"