from django.contrib import admin
from .models import User, Company, JobApplication, Interview

# Register your models here.

admin.site.register(User)

admin.site.register(Company)

admin.site.register(JobApplication)

admin.site.register(Interview)