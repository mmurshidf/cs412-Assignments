# File: models.py
# Author: Mohammed Murshid (murshidm@bu.edu), 11/21/2024
# Description: Models file for final project/job application app

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Account model that represents a user by giving them a username, email, profile, first name, and last name
class Account(models.Model):
    """User model that stores the user's account details."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="accounts", default=1)  # Link to the built-in User model
    username = models.CharField(max_length=50, unique=True)  # Unique username for the user
    email = models.EmailField(unique=True)  # Unique email address for the user
    profile = models.TextField(blank=True, null=True)  # Optional profile information about the user
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)  # Optional field for uploading a resume

    def __str__(self):
        return self.username  # Display the username when this model is referenced

# Company model that represents the company by its name, industry, and location
class Company(models.Model):
    """Represents a company in the system."""
    name = models.CharField(max_length=100)  # Name of the company
    industry = models.CharField(max_length=100)  # Industry in which the company operates
    location = models.CharField(max_length=100)  # Location of the company

    def __str__(self):
        return self.name  # Display the company's name when this model is referenced


# Job model to represent job listings posted by companies
class Job(models.Model):
    """Represents a job listing created by a company."""
    company = models.ForeignKey(Company, on_delete=models.CASCADE)  # Link to the Company model
    position_title = models.CharField(max_length=100)  # Job position title
    description = models.TextField()  # Detailed description of the job
    location = models.CharField(max_length=100)  # Location where the job is based
    posted_date = models.DateField(auto_now_add=True)  # Date when the job was posted
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_jobs", default=1)  # Link to the user who created the job

    def __str__(self):
        return f"{self.position_title} at {self.company.name}"  # Display the position title and company name

    def get_job_details_url(self):
        """Get the URL to view the job details."""
        return f"/project/job/{self.pk}/"  # URL pattern for the job details page


# Job application status model
class JobApplication(models.Model):
    """Represents an application for a specific job."""
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('interview', 'Interview'),
        ('offer', 'Offer'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(Account, on_delete=models.CASCADE)  # Link to the Account model (user applying for the job)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, default=1)  # Link to the Job model (the job being applied for)
    application_date = models.DateField()  # Date the application was submitted
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)  # Current status of the application
    interview = models.OneToOneField('Interview', on_delete=models.CASCADE, blank=True, null=True)  # One-to-one relationship with the Interview model (if applicable)

    def __str__(self):
        return f"{self.user.username} applied for {self.job.position_title}"  # Display the user's name and job position

# Interview model to track interviews
class Interview(models.Model):
    """Represents an interview scheduled for a job application."""
    job_application = models.ForeignKey(JobApplication, on_delete=models.CASCADE, related_name='interviews')  # Link to the JobApplication model
    interview_date = models.DateField()  # Date of the interview
    interviewer_name = models.CharField(max_length=100)  # Name of the interviewer
    feedback = models.TextField(blank=True, null=True)  # Optional feedback after the interview

    def __str__(self):
        return f"Interview for {self.job_application.position_title} on {self.interview_date}"  # Display job position title and interview date


# Review model to allow users to leave reviews for companies
class Review(models.Model):
    """Represents a review given by a user for a company."""
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='reviews')  # Link to the Company being reviewed
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the user who wrote the review
    rating = models.IntegerField(choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')])  # Rating (1 to 5 stars)
    review_text = models.TextField()  # Text content of the review
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the review was created

    def __str__(self):
        return f"Review by {self.user.username} for {self.company.name} - {self.rating} stars"  # Display user and company name with rating

    class Meta:
        ordering = ['-created_at']  # Order reviews by creation time, with the most recent first
