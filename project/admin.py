from django.contrib import admin
from .models import Account, Company, JobApplication, Interview

# Register your models here.

admin.site.register(Account)

admin.site.register(Company)

admin.site.register(JobApplication)

admin.site.register(Interview)