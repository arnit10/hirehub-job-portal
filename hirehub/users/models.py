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
    
    def is_candidate(self):
        return self.role == "J"

    def is_recruiter(self):
        return self.role == "R"
    

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

#job model
class Job(models.Model):
    recruiter = models.ForeignKey(User, on_delete= models.CASCADE, limit_choices_to= {"Role": 'R'})
    title = models.CharField(max_length=300)
    description = models.TextField()
    location = models.CharField(max_length= 150)
    salary = models.CharField(max_length= 100)
    created_at = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return self.title
    
#Job Application
class JobApplication(models.Model):
    STATUS_CHOICES = [
        ("Applied", "Applied"),
        ("Seen", "Seen"),
        ("Shortlisted", "Shortlisted"),
        ("Rejected", "Rejected"),
        ("Selected", "Selected"),
    ]
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    candidate = models.ForeignKey(User, on_delete= models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)
    cover_letter = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="applied")
    
    class Meta:
        unique_together = ("job", "candidate")

    def __str__(self):
        return f"{self.candidate.username} applied to {self.job.title}"

#saved jobs   
class SavedJob(models.Model):
    candidate = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={"role": "J"})
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("candidate", "job")

    def __str__(self):
        return f"{self.candidate.username} saved {self.job.title}"
    


