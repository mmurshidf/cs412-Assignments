# File: forms.py
# Author: Mohammed Murshid (murshidm@bu.edu), 12/9/2024
# Description: Creates forms for site

from django import forms
from .models import Job, Company, Account, Interview, Review
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Form to update the user's email and resume
class UpdateProfileForm(forms.ModelForm):
    """Form to update the user's email and resume."""
    class Meta:
        model = Account
        fields = ['email', 'resume']

    email = forms.EmailField(required=True)  # Field for the user's email address
    resume = forms.FileField(required=False)  # Field for the user's resume (optional)

# Form to create a new job listing
class JobCreationForm(forms.ModelForm):
    """Form to create a new job listing."""
    class Meta:
        model = Job
        fields = ['company', 'position_title', 'description', 'location']  # Fields for job creation

    def __init__(self, *args, **kwargs):
        """Modify the company field queryset to show all companies."""
        super(JobCreationForm, self).__init__(*args, **kwargs)
        self.fields['company'].queryset = Company.objects.all()  # Limit companies to the existing ones

# Form to create a new user account
class CreateAccountForm(UserCreationForm):
    """Form to create a new user account."""
    email = forms.EmailField(required=True, label="Email Address")  # Field for email address

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')  # Fields for creating a user account

# Form for scheduling an interview
class InterviewForm(forms.ModelForm):
    """Form to schedule an interview with the applicant."""
    class Meta:
        model = Interview
        fields = ['interview_date', 'interviewer_name', 'feedback']  # Fields for interview scheduling

# Form to create a new company
class CompanyForm(forms.ModelForm):
    """Form to create a new company."""
    class Meta:
        model = Company
        fields = ['name', 'industry', 'location']  # Fields for creating a company

# Form to leave a review for a company
class ReviewForm(forms.ModelForm):
    """Form to leave a review for a company."""
    class Meta:
        model = Review
        fields = ['rating', 'review_text']  # Fields for the review
        # Customize the 'review_text' field to be a multi-line text area with a placeholder
        widgets = {
            'review_text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your review here...'}),  # Textarea widget for reviews
        }
