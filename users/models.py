from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
#User model
class User(AbstractUser):
    ROLE_CHOICES = (
        ('J', "Job Seeker"),
        ('E', "Employer")
    )

    role = models.CharField(max_length=20, choices= ROLE_CHOICES)

    