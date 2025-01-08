from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView,
    ListAPIView, RetrieveUpdateAPIView, RetrieveAPIView,
    DestroyAPIView
)
from .models import (
    JobPosting, SchoolProfile,
    TeacherProfile, Application,
    CustomUser
)
from .serializers import (
    JobPostingSerializer,
    RegistrationSerializer, 
    SchoolProfileSerializer, 
    TeacherProfileSerializer, 
    ApplicationSerializer
)
from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework import status
from rest_framework.views import APIView

from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.contrib.auth import authenticate, login, logout

from .models import (
    JobPosting, SchoolProfile,
    TeacherProfile, Application,
    CustomUser
)
from .serializers import (
    JobPostingSerializer, 
    SchoolProfileSerializer, 
    TeacherProfileSerializer, 
    ApplicationSerializer
)
from .serializers import UserSerializer
from .permissions import IsSchool, IsTeacher
from django.db.models import Q
from rest_framework.filters import SearchFilter

CustomUser = get_user_model()

class UnifiedRegistrationView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "Registration successful.", "user_id": user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






class SignupView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # Create the user
            user = serializer.save()

            # Create the appropriate profile based on user_type
            if user.user_type == 'teacher':
                TeacherProfile.objects.create(user=user)
            elif user.user_type == 'school':
                SchoolProfile.objects.create(user=user)

            return Response({"message": "User and profile created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteAcountView(DestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return CustomUser.objects.get(username=self.request.user.username)
        except CustomUser.DoesNotExist:
            raise NotFound("School profile not found for the current user.")

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if user is not None:
            # Log the user in and start a session
            login(request, user)
            return Response({"message": "Login successful."}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Delete the user's token to log them out
        logout(request=request)
        return Response({"message": "Logout successful."}, status=status.HTTP_200_OK)


# Teacher views----------------------------------------------------

class CurrentTeacherProfileView(RetrieveAPIView):
    serializer_class = TeacherProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return TeacherProfile.objects.get(user=self.request.user)
        except TeacherProfile.DoesNotExist:
            raise NotFound("Teacher profile not found for the current user.")

class TeacherListCreateView(ListAPIView):
    queryset = TeacherProfile.objects.all()
    serializer_class = TeacherProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class TeacherDetailView(RetrieveAPIView):
    """Retrieve a specific TeacherProfile,
    Identified by its ID
    """
    serializer_class = TeacherProfileSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        return TeacherProfile.objects.all()


# School Veiws----------------------------------------------

# List All Schools profile
class SchoolListView(ListAPIView):
    queryset = SchoolProfile.objects.all()
    serializer_class = SchoolProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class CurrentSchoolProfileView(RetrieveAPIView):
    serializer_class = SchoolProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return SchoolProfile.objects.get(user=self.request.user)
        except SchoolProfile.DoesNotExist:
            raise NotFound("School profile not found for the current user.")

class SchoolDetailView(RetrieveUpdateAPIView):
    """get or update the given school profile"""
    serializer_class = SchoolProfileSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'
    def get_queryset(self):
        return SchoolProfile.objects.all()


# Job Postings Views--------------------------------------------

#   Retrieve, update or destroy the given JobPosting
class JobPostingDetailView(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or destroy the given JobPosting
    """
    queryset = JobPosting.objects.all()
    serializer_class = JobPostingSerializer
    permission_classes = [IsAuthenticated, IsSchool]
    lookup_field = 'pk'

    def get_queryset(self):
        if self.request.user.user_type == 'school':
            school = SchoolProfile.objects.filter(user=self.request.user).first()
            return JobPosting.objects.filter(school=school)
        return JobPosting.objects.none()

class AllJobsView(ListAPIView):
    """List all job postings of all schools"""
    queryset = JobPosting.objects.all()
    serializer_class = JobPostingSerializer
    permission_classes = [IsAuthenticated]

class JobPostingListCreateView(ListCreateAPIView):
    """
    List Job Postings of the current school, or create Job postings for this
    school
    """
    queryset = JobPosting.objects.all()
    serializer_class = JobPostingSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        # Schools can only view their own job postings
        if self.request.user.user_type == 'school':
            school = SchoolProfile.objects.filter(user=self.request.user).first()
            return JobPosting.objects.filter(school=school)
        return JobPosting.objects.none()

    def perform_create(self, serializer):
        # Ensure only schools can create job postings
        if self.request.user.user_type == 'school':
            school = SchoolProfile.objects.filter(user=self.request.user).first()
            serializer.save(school=school)
        else:
            raise PermissionDenied("Only schools can create job postings.")



# Applications Views------------------------------------------

class ApplicationListCreateView(ListCreateAPIView):
    """
    List all application of the current teacher
    or Apply for a job for this teacher
    """
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    def get_queryset(self):
        if self.request.user.user_type == 'teacher':
            teacher = TeacherProfile.objects.filter(user=self.request.user).first()
            return Application.objects.filter(teacher=teacher)
        return Application.objects.none()

    def perform_create(self, serializer):
        
        if self.request.user.user_type == 'teacher':
            teacher = TeacherProfile.objects.filter(user=self.request.user).first()
            serializer.save(teacher=teacher)
        else:
            raise PermissionDenied("Only teachers can apply for jobs.")

class ListAllApplications(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ApplicationSerializer
    queryset = Application.objects.all()

class ApplicationDetailView(RetrieveUpdateDestroyAPIView):
    """Retrieve a specific applicatin details of the
    current teacher, the application is identified by
    it's ID.
    """

    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated, IsTeacher]
    lookup_field = 'pk'

    def get_queryset(self):
        if self.request.user.user_type == 'teacher':
            teacher = TeacherProfile.objects.filter(user=self.request.user).first()
            return Application.objects.filter(teacher=teacher)

class SchoolJobApplicationsView(ListAPIView):

    """List all Applications to the current School
    """
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated, IsSchool]

    def get_queryset(self):
        if self.request.user.user_type == 'school':
            school = SchoolProfile.objects.filter(user=self.request.user).first()
            job = JobPosting.objects.filter(school=school)
            if not job.exists():
                return Application.objects.none()
            return Application.objects.filter(job__in=job)
        else:
            PermissionDenied("only schools can perfrom this action")
        return Application.objects.none()

class JobSearchView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        keyword = request.query_params.get('q', '')

        query = Q()

        if keyword:
            query &= Q(subject__icontains=keyword)
        
        jobs = JobPosting.objects.filter(query)
        serializer = JobPostingSerializer(jobs, many=True)
        return Response(serializer.data)

class JobPostingSearchView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = JobPosting.objects.all()
    serializer_class = JobPostingSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title', 'description', 'subject', 'location']

class ApplicationSearchView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    filter_backends = [SearchFilter]
    search_fields = ['teacher__user__username', 'job__title', 'status']