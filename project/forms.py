from django import forms
from .models import Job, Company, Account, Interview
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UpdateProfileForm(forms.ModelForm):
    """Form to update the user's email and resume."""
    class Meta:
        model = Account
        fields = ['email', 'resume']  # Include both email and resume fields for update

    email = forms.EmailField(required=True)
    resume = forms.FileField(required=False)

class JobCreationForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['company', 'position_title', 'description', 'location', 'industry']

    def __init__(self, *args, **kwargs):
        super(JobCreationForm, self).__init__(*args, **kwargs)
        self.fields['company'].queryset = Company.objects.all()  # Allow user to select a company from existing companies

class CreateAccountForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email Address")

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = ['interview_date', 'interviewer_name', 'feedback']

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'industry', 'location']