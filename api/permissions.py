
from rest_framework.permissions import BasePermission

class IsTeacher(BasePermission):
    """Ensure the user is authenticated and is a teacher"""

    def has_permission(self, request, view):
        # return request.user.is_authenticated and request.user.role == 'teacher'
        return request.user.is_authenticated and request.user.user_type == 'teacher'

class IsSchool(BasePermission):
    """Enusre the user is authenticated and is school"""
    def has_permission(self, request, view):
        # return request.user.is_authenticated and request.user.role == 'school'
        return request.user.is_authenticated and request.user.user_type == 'school'
