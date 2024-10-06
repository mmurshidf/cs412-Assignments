# File: models.py
# Author: Mohammed Murshid (murshidm@bu.edu), 10/6/2024
# Description: Models file to structure profile info

from django.db import models

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