from django.urls import path
from .views import *

urlpatterns = [
    path("", home_view, name="home"),
    path("signup/", user_signup, name = "user_signup"),
    path("login/", UserLoginView.as_view(), name= "user_login" ),
    path("logout/", user_logout_view, name="user_logout"),
    path("candidate-profile", candidate_profile_create, name= "candidate_profile_create"),
    path("recruiter-profile", recruiter_profile_create, name= "recruiter_profile_create"),
]