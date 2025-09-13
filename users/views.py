from django.shortcuts import render, redirect
from .models import *

# Create your views here.
def candidate_signup(request):
    if request.method == "POST":
        # User Fields
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        #Candidate Fields
        full_name = request.POST['full_name']
        phone_number = request.POST['phone_number']
        resume = request.FILES.get('resume')
        skills = request.POST['skills']
        experience = request.POST['experience']

        #user creation
        user = User.objects.create_user(
            username = username,
            email = email,
            password = password,
            role = 'J'
        )

        #candidate creation
        CandidateProfile.objects.create(
            user = user,
            full_name = full_name,
            phone_number = phone_number,
            resume = resume,
            skills = skills,
            experience = experience
        )

        return redirect("login")
    return render(request, "users/candidate_signup.html")