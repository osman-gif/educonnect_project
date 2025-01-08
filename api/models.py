import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    """
    CustomUser Model class
    """
    USER_TYPE_CHOICES = (
        ('teacher', 'Teacher'),
        ('school', 'School'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, null=False, blank=False, default='teacher')
    
    def __str__(self):
        return self.username

class TeacherProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='teacher_profile')
    resume = models.FileField(upload_to='resumes/')
    qualifications = models.TextField()
    subject_expertise = models.CharField(max_length=255)

    def __str__(self):
        return self.user.get_full_name()


class SchoolProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='school_profile')
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=20)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.school_name

class JobPosting(models.Model):
    """JobPosting Model class"""

    school = models.ForeignKey(SchoolProfile, on_delete=models.CASCADE, related_name='job_postings')
    title = models.CharField(max_length=255)
    description = models.TextField()
    subject = models.CharField(max_length=100)
    salary_range = models.CharField(max_length=50)
    location = models.CharField(max_length=255)
    requirements = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} at {self.school.name}"

class Application(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='applications')
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.teacher.user.get_full_name()} applied for {self.job.title}"
