from django.urls import path
from .views import (
    AllJobsView,
    ApplicationSearchView,
    CurrentTeacherProfileView,
    JobPostingSearchView,
    JobSearchView,
    ListAllApplications,
    LoginView,
    LogoutView,
    SchoolListView,
    SignupView,
    TeacherListCreateView,
    TeacherDetailView,
    SchoolDetailView,
    JobPostingListCreateView,
    JobPostingDetailView,
    ApplicationListCreateView,
    ApplicationDetailView,
    SchoolJobApplicationsView,
    CurrentSchoolProfileView,
    DeleteAcountView,
    UnifiedRegistrationView
)

urlpatterns = [

    path('register/', UnifiedRegistrationView.as_view(), name='register'),

    # path('signup/', SignupView.as_view(), name='signup'),
    path('delete_account/', DeleteAcountView.as_view(), name='delete-account'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    path('teachers/', TeacherListCreateView.as_view(), name='teacher-list'),
    path('teachers/<int:pk>/', TeacherDetailView.as_view(), name='teacher-detail'),
    path('teacher-profile/', CurrentTeacherProfileView.as_view()),

    path('schools/', SchoolListView.as_view(), name='school-list'),
    path('schools/<int:pk>/', SchoolDetailView.as_view(), name='school-detail'),
    path('school-profile/', CurrentSchoolProfileView.as_view()),

    path('all_jobs/', AllJobsView.as_view(), name='all_jobs'),
    path('jobs/', JobPostingListCreateView.as_view(), name='job-list-create'),
    path('jobs/<int:pk>/', JobPostingDetailView.as_view(), name='job-detail'),

    path('applications/', ApplicationListCreateView.as_view(), name='application-list-create'),
    path('applications/<int:pk>/', ApplicationDetailView.as_view(), name='application-detail'),
    path('all-applications/', ListAllApplications.as_view(), name='all-applications'),
    path('school-applications/', SchoolJobApplicationsView.as_view(), name='school-applications'),

    path('jobs/search/', JobSearchView.as_view(), name='job-search'),
    path('job-postings/search/', JobPostingSearchView.as_view(), name='job_posting_search'),
    path('applications/search/', ApplicationSearchView.as_view(), name='application_search'),
]
