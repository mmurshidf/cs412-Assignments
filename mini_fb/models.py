# File: models.py
# Author: Mohammed Murshid (murshidm@bu.edu), 10/6/2024
# Description: Models file to structure profile info

from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.

class Profile(models.Model):
    """Class for profile"""
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    profile_image_url = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    def get_status_messages(self):
        return StatusMessage.objects.filter(profile=self).order_by('-timestamp')
    
    def get_absolute_url(self):
        return reverse('show_profile', kwargs={'pk': self.pk})

class StatusMessage(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Status by {self.profile.first_name} on {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
