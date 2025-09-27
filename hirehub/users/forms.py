from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *

#User Sign Up form
class UserSignUpForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
            "placeholder": "Enter password"
        })
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
            "placeholder": "Confirm password"
        })
    )
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "role"]

        widgets = {
            "username" : forms.TextInput(attrs= {
                "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
                "placeholder": "username"
            }),
            "email": forms.EmailInput(attrs= {
                "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
                "placeholder": "enter your email.."
            }),
             
        }

#custom login form
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500",
            "placeholder": "Enter username"
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500",
            "placeholder": "Enter password"
        })
    )

# Candidate Signup Form 
class CandidateSignUpForm(forms.ModelForm):
    class Meta:
        model = CandidateProfile
        fields= ["full_name", "phone_number", "skills", "experience", "resume"]

        widgets= {
            "full_name": forms.TextInput(attrs={
                "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
                "placeholder": "Full Name"
            }),
            "phone_number": forms.TextInput(attrs= {
                "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
                "placeholder": "Enter your phone number..."
            }),
            "skills": forms.Textarea(attrs={
                "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
                "placeholder": "Full Name"
            }),
            "experience": forms.TextInput(attrs={
                "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
                "placeholder": "Experience"
            }),
            "resume":forms.ClearableFileInput(attrs={
                "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            })
        }

#Recruiter Sign up form
class RecruiterSignUpForm(forms.ModelForm):
    class Meta:
        model = RecruiterProfile
        fields = ["company_name", "phone_number","address"]

        widgets = {
            "company_name": forms.TextInput(attrs={
                "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
                "placeholder": "Company Name"
            }),
            "phone_number": forms.TextInput(attrs={
                "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
                "placeholder": "Phone Number"
            }),
            "address": forms.TextInput(attrs={
                "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
                "placeholder": "Company Address"
            }),
        }

#job apply form
class JobApplyForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ["cover_letter"]
        widgets = {
            "cover_letter": forms.Textarea(attrs={
                "class": "w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500",
                "placeholder": "Write your cover letter (optional)...",
                "rows": 4
            })
        }


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'location', 'salary']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input w-full', 'placeholder': 'Job Title'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea w-full', 'placeholder': 'Job Description'}),
            'location': forms.TextInput(attrs={'class': 'form-input w-full', 'placeholder': 'Location'}),
            'salary': forms.TextInput(attrs={'class': 'form-input w-full', 'placeholder': 'Salary'}),
        }