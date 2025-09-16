from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .models import *
from .forms import *


# Create your views here.
#homepage view
def home_view(request):
    return render(request, "users/home.html")

#user login view
class UserLoginView(LoginView):
    template_name = "users/login.html"
    authentication_form = CustomLoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user

        if user.role == "C":
            return reverse_lazy("candidate_dashboard")

        elif user.role == "R":
            return reverse_lazy("recruiter_dashboard")

        return reverse_lazy("home")

#user logout view
def user_logout_view(request):
    logout(request)
    return redirect("home")

#user signup view
def user_signup(request):
    if request.method == "POST":
        form = UserSignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            if user.role == "J":
                return redirect("candidate_profile_create")
            elif user.role == "R":
                return redirect("recruiter_profile_create")

    else:
        form = UserSignUpForm()
    return render(request, "users/signup.html", {'form': form} )

#job seeker profile creation view
@login_required
def candidate_profile_create(request):
    if request.method == "POST":
        form = CandidateSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit= False)
            profile.user = request.user
            profile.save()
            return redirect('dashboard')
    else:
        form = CandidateSignUpForm()

    return render(request, 'users/candidateprofileform.html', {'form': form})

#recruiter profile creation view
@login_required
def recruiter_profile_create(request):
    if request.method == "POST":
        form = RecruiterSignUpForm(request.POST)
        if form.is_valid():
            profile = form.save(commit= False)
            profile.user = request.user
            profile.save()
            return redirect('dashboard')
    else:
        form = RecruiterSignUpForm()
    return render(request, 'users/recruiterprofileform.html', {'form': form}) 