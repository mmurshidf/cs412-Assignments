# File: models.py
# Author: Mohammed Murshid (murshidm@bu.edu), 10/6/2024
# Description: Models file to structure profile info

from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    """Class for profile"""
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    profile_image_url = models.URLField(max_length=200, blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profiles", default=1)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    def get_status_messages(self):
        return StatusMessage.objects.filter(profile=self).order_by('-timestamp')
    
    def get_absolute_url(self):
        return reverse('show_profile', kwargs={'pk': self.pk})
    
    def get_friends(self):
        friends_1 = Friend.objects.filter(profile1=self).values_list('profile2', flat=True)
        friends_2 = Friend.objects.filter(profile2=self).values_list('profile1', flat=True)
        friends_ids = list(friends_1) + list(friends_2)
        return Profile.objects.filter(id__in=friends_ids)
    
    def add_friend(self, other):
        """Add a Friend relation between this profile and another, avoiding duplicates and self-friending."""
        if self == other:
            return

        friendship_exists = Friend.objects.filter(
            Q(profile1=self, profile2=other) | Q(profile1=other, profile2=self)
        ).exists()

        if not friendship_exists:
            Friend.objects.create(profile1=self, profile2=other)
    
    def get_friend_suggestions(self):
        existing_friends = self.get_friends()
        suggestions = Profile.objects.exclude(
            Q(id=self.id) | Q(id__in=[friend.id for friend in existing_friends])
        )
        
        return suggestions

    def get_news_feed(self):
        friends = self.get_friends()
        status_messages = StatusMessage.objects.filter(
            Q(profile=self) | Q(profile__in=friends)
        ).order_by('-timestamp')

        return status_messages

class StatusMessage(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Status by {self.profile.first_name} on {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
    
    def get_images(self):
        return Image.objects.filter(status_message=self)

class Image(models.Model):
    image_file = models.ImageField(upload_to='images/')
    status_message = models.ForeignKey(StatusMessage, on_delete=models.CASCADE, related_name='images')
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Image uploaded on {self.timestamp}"
    
class Friend(models.Model):
    profile1 = models.ForeignKey(Profile, related_name='friendships_initiated', on_delete=models.CASCADE)
    profile2 = models.ForeignKey(Profile, related_name='friendships_received', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.profile1.first_name} {self.profile1.last_name} & {self.profile2.first_name} {self.profile2.last_name}"
