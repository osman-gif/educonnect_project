from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import SchoolProfile, JobPosting, Application, TeacherProfile, CustomUser

admin.site.register(SchoolProfile)

admin.site.register(JobPosting)
admin.site.register(Application)
admin.site.register(TeacherProfile)
admin.site.register(CustomUser)