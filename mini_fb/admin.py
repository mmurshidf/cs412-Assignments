# File: admin.py
# Author: Mohammed Murshid (murshidm@bu.edu), 10/6/2024
# Description: Registers profile

from django.contrib import admin
from .models import Profile, StatusMessage, Image, Friend

# Register your models here.

admin.site.register(Profile)

admin.site.register(StatusMessage)

admin.site.register(Image)

admin.site.register(Friend)