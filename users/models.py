from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
#User model
class User(AbstractUser):
    ROLE_CHOICES = (
        ('J', "Job Seeker"),
        ('R', "Recruiter")
    )

    role = models.CharField(max_length=20, choices= ROLE_CHOICES)

    def __str__(self):
        return self.username

#Candidate 
class CandidateProfile(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)

    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)
    resume = models.FileField(upload_to='resumes/')
    skills = models.TextField(max_length=400)
    experience = models.PositiveIntegerField(default= 0)

    def __str__(self):
        return self.full_name
    
# Recruiter
class RecruiterProfile(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)

    company_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)
    address = models.CharField(max_length=250)
    