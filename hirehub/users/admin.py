from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(CandidateProfile)
admin.site.register(RecruiterProfile)
admin.site.register(JobApplication)
admin.site.register(Job)