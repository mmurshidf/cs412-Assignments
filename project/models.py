# File: models.py
# Author: Mohammed Murshid (murshidm@bu.edu), 11/21/2024
# Description: Models file to for final project/job application app

from django.db import models

# Create your models here.

# User model that represents a user by giving them a username, email, and profile
class User(models.Model):

    #Fields
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    profile = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username

#Company model that represents the company by its name, industry, and location
class Company(models.Model):

    #Fields
    name = models.CharField(max_length=100)
    industry = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name

#Job application status model
class JobApplication(models.Model):

    #Status choices
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('interview', 'Interview'),
        ('offer', 'Offer'),
        ('rejected', 'Rejected'),
    ]

    #Fields and applicant status
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    position_title = models.CharField(max_length=100)
    application_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.position_title} at {self.company.name}"


#Interview Model to track interviews
class Interview(models.Model):

    #Fields
    job_application = models.ForeignKey(JobApplication, on_delete=models.CASCADE)
    interview_date = models.DateField()
    interviewer_name = models.CharField(max_length=100)
    feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Interview for {self.job_application.position_title} on {self.interview_date}"