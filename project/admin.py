# File: admin.py
# Author: Mohammed Murshid (murshidm@bu.edu), 12/9/2024
# Description: Registers profile

from django.contrib import admin
from .models import Account, Company, JobApplication, Interview, Job, Review

# Register your models here.

#Registers Account
admin.site.register(Account)

#Registers Company
admin.site.register(Company)

#Registers JobApplication
admin.site.register(JobApplication)

#Registers Interview
admin.site.register(Interview)

#Registers Job
admin.site.register(Job)

#Registers Review
admin.site.register(Review)