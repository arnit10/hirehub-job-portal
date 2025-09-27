from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.db.models import Q
from django.core.paginator import Paginator

from .models import *
from .forms import *


# Create your views here.
#homepage view
def home_view(request):
    jobs = Job.objects.all()
     # Search
    query = request.GET.get("q")
    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(location__icontains=query)
        )

    # Location filter
    location = request.GET.get("location")
    if location:
        jobs = jobs.filter(location__icontains=location)

    # #Salary filters
    # min_salary = request.GET.get("min_salary")
    # if min_salary:
    #     jobs = jobs.filter(salary__gte=min_salary)

    # max_salary = request.GET.get("max_salary")
    # if max_salary:
    #     jobs = jobs.filter(salary__lte=max_salary)

    # Pagination
    paginator = Paginator(jobs.order_by("-created_at"), 5)  # 10 per page
    page = request.GET.get("page")
    jobs = paginator.get_page(page)
    role = None
    if request.user.is_authenticated:
        role = request.user.role
    return render(request, "users/home.html", {"role": role, "jobs":jobs})

#user signup view
def user_signup(request):
    if request.method == "POST":
        form = UserSignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            if user.role == "J":
                return redirect("candidate_profile")
            elif user.role == "R":
                return redirect("recruiter_profile")

    else:
        form = UserSignUpForm()
    return render(request, "users/signup.html", {'form': form} )

#user login view
class UserLoginView(LoginView):
    template_name = "users/login.html"
    authentication_form = CustomLoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user

        if user.role == "J":
            return reverse_lazy("home")

        elif user.role == "R":
            return reverse_lazy("home")

        return reverse_lazy("home")

#user logout view
def user_logout_view(request):
    logout(request)
    return redirect("home")


#*****************DASHBOARDS***********************
#candidate dashboard
@login_required
def candidate_dashboard(request):
    profile = CandidateProfile.objects.filter(user=request.user).first()  
    applications = JobApplication.objects.filter(candidate=request.user).select_related("job").order_by("-applied_at")
    return render(request, "users/candidate_dashboard.html", {"profile": profile, "applications":applications})

#recruiter dashboard
@login_required
def recruiter_dashboard(request):
    profile = RecruiterProfile.objects.filter(user=request.user).first()
    if not profile:
        messages.error(request, "Please complete your recruiter profile first.")
        return redirect("recruiter_profile")
    
    jobs = Job.objects.filter(recruiter=request.user).order_by("-created_at")

    return render(request, "users/recruiter_dashboard.html", {
        "profile": profile,
        "jobs": jobs 
    })


#candidate profile
@login_required
def candidate_profile(request):
    try:
        profile = CandidateProfile.objects.get(user=request.user)
    except CandidateProfile.DoesNotExist:
        profile = None

    if request.method == "POST":
        form = CandidateSignUpForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            candidate_profile = form.save(commit=False)
            candidate_profile.user = request.user
            candidate_profile.save()
            return redirect("candidate_dashboard") 
    else:
        form = CandidateSignUpForm(instance=profile)

    return render(request, "users/candidateprofileform.html", {"form": form})

#recruiter profile
@login_required
def recruiter_profile(request):
    try:
        profile = RecruiterProfile.objects.get(user=request.user)
    except RecruiterProfile.DoesNotExist:
        profile = None

    if request.method == "POST":
        form = RecruiterSignUpForm(request.POST, instance=profile)
        if form.is_valid():
            recruiter_profile = form.save(commit=False)
            recruiter_profile.user = request.user
            recruiter_profile.save()
            messages.success(request, "Profile saved successfully ✅")
            return redirect("recruiter_dashboard")
    else:
        form = RecruiterSignUpForm(instance=profile)

    return render(request, "users/recruiterprofileform.html", {"form": form})

#job_create
@login_required
def job_create(request):
    if request.user.role != "R":
        return HttpResponseForbidden("You are not authorized to create jobs.")

    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.recruiter = request.user 
            job.save()
            messages.success(request, "Job posted successfully!")
            return redirect("recruiter_dashboard")
    else:
        form = JobForm()

    return render(request, "users/job_form.html", {"form": form})

# recruiter jobs
@login_required
def recruiter_jobs(request):
    # only recruiters allowed
    if request.user.role != "R":
        return HttpResponseForbidden("You are not authorized to access this page.")

    jobs = Job.objects.filter(posted_by=request.user)
    return render(request, "users/recruiter_jobs.html", {"jobs": jobs})

#job details view
def job_details(request, job_id):
    job = get_object_or_404(Job, id= job_id)
    application = None
    if request.user.is_authenticated and request.user.role == "J":
        application = JobApplication.objects.filter(job=job, candidate=request.user).first()

    return render(request, 'users/job_details.html', 
                  {'job': job,
                   'application': application
                   })

#job apply
@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    # only job seekers can apply
    if request.user.role != "J":
        messages.error(request, "Only Job Seekers can apply for jobs.")
        return redirect("job_details", job_id=job.id)

    if JobApplication.objects.filter(job=job, candidate=request.user).exists():
        messages.warning(request, "You have already applied for this job.")
        return redirect("job_details", job_id=job.id)

    if request.method == "POST":
        form = JobApplyForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.candidate = request.user
            application.save()
            messages.success(request, "Your application has been submitted!")
            return redirect("job_details", job_id=job.id)
    else:
        form = JobApplyForm()

    return render(request, "users/apply_job.html", {"form": form, "job": job})

#job applicants
@login_required
def job_applicants(request, job_id):
    job = get_object_or_404(Job, id=job_id, recruiter=request.user)
    applications = JobApplication.objects.filter(job=job).select_related("candidate", "candidate__candidateprofile")
    return render(request, "users/job_applicants.html", {"job": job, "applications": applications})


#job edit view
@login_required
def job_edit(request, job_id):
    job = get_object_or_404(Job, id=job_id, recruiter=request.user)

    if request.method == "POST":
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, "Job updated successfully!")
            return redirect("recruiter_dashboard")
    else:
        form = JobForm(instance=job)

    return render(request, "users/job_form.html", {"form": form})

#job delete view
@login_required
def job_delete(request, job_id):
    job = get_object_or_404(Job, id=job_id, recruiter=request.user)

    if request.method == "POST":
        job.delete()
        messages.success(request, "Job deleted successfully!")
        return redirect("recruiter_dashboard")

    return render(request, "users/job_confirm_delete.html", {"job": job})

def job_list(request):
    jobs = Job.objects.all()

    # Search
    query = request.GET.get("q")
    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(location__icontains=query)
        )

    # Location filter
    location = request.GET.get("location")
    if location:
        jobs = jobs.filter(location__icontains=location)

    # Salary filters
    min_salary = request.GET.get("min_salary")
    if min_salary:
        jobs = jobs.filter(salary__gte=min_salary)

    max_salary = request.GET.get("max_salary")
    if max_salary:
        jobs = jobs.filter(salary__lte=max_salary)

    # Pagination
    paginator = Paginator(jobs.order_by("-created_at"), 10)  # 10 per page
    page = request.GET.get("page")
    jobs = paginator.get_page(page)

    return render(request, "users/job_list.html", {"jobs": jobs})

#save a job
@login_required
def save_job(request, job_id):
    if request.user.role != "J":
        return HttpResponseForbidden("Only Job Seekers can save jobs.")
    
    job = get_object_or_404(Job, id=job_id)
    saved, created = SavedJob.objects.get_or_create(candidate=request.user, job=job)

    if created:
        messages.success(request, "Job saved to wishlist!")
    else:
        messages.info(request, "You already saved this job.")

    return redirect("job_details", job_id=job.id)

#saved jobs
@login_required
def saved_jobs(request):
    if request.user.role != "J":
        return HttpResponseForbidden("Only Job Seekers can view saved jobs.")
    
    saved_jobs = SavedJob.objects.filter(candidate=request.user).select_related("job").order_by("-saved_at")
    return render(request, "users/saved_jobs.html", {"saved_jobs": saved_jobs})

#unsave job
@login_required
def unsave_job(request, job_id):
    if request.user.role != "J":
        return HttpResponseForbidden("Only Job Seekers can unsave jobs.")
    
    job = get_object_or_404(Job, id=job_id)
    SavedJob.objects.filter(candidate=request.user, job=job).delete()
    messages.success(request, "Job removed from your saved list.")
    return redirect("saved_jobs")

#update job status
@login_required
def update_application_status(request, application_id):
    application = get_object_or_404(JobApplication, id=application_id, job__recruiter=request.user)
    
    if request.method == "POST":
        new_status = request.POST.get("status")
        if new_status in dict(JobApplication.STATUS_CHOICES).keys():
            application.status = new_status
            application.save()
            messages.success(request, f"Status updated to {new_status}")
    
    return redirect("job_applicants", job_id=application.job.id)





