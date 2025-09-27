from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", home_view, name="home"),
    path("signup/", user_signup, name = "user_signup"),
    path("login/", UserLoginView.as_view(), name= "user_login" ),
    path("logout/", user_logout_view, name="user_logout"),
    path("candidate-profile/", candidate_profile, name= "candidate_profile"),
    path("recruiter-profile/", recruiter_profile, name= "recruiter_profile"),
    path("candidate-dashboard/", candidate_dashboard, name = "candidate_dashboard"),
    path("recruiter-dashboard/", recruiter_dashboard, name= "recruiter_dashboard"),
    path("job/<int:job_id>/", job_details, name="job_details"),
    path("job/<int:job_id>/apply/", apply_job, name="apply_job"),
    path('job/create/', job_create, name='job_create'),
    path('recruiter/jobs/<int:job_id>/applicants/', job_applicants, name='job_applicants'),
    path('recruiter/jobs/<int:job_id>/edit/', job_edit, name='job_edit'),
    path('recruiter/jobs/<int:job_id>/delete/', job_delete, name='job_delete'),
    path('jobs/', job_list, name= "job_list"),
    path("job/<int:job_id>/save/", save_job, name="save_job"),
    path("saved-jobs/", saved_jobs, name="saved_jobs"),
    path("job/<int:job_id>/unsave/", unsave_job, name= "unsave_job"),
    path("applications/<int:application_id>/update-status/", update_application_status, name="update_application_status"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
