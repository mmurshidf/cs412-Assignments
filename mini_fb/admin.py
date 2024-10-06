# File: admin.py
# Author: Mohammed Murshid (murshidm@bu.edu), 10/6/2024
# Description: Registers profile

from django.contrib import admin
from .models import Profile

# Register your models here.

admin.site.register(Profile)