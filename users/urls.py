from django.urls import path
from .views import *

urlpatterns = [
    path("candidate/signup", candidate_signup, name = "candidate_signup")
]