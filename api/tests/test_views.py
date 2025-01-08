from unittest.mock import patch
from django.test import RequestFactory
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from api.models import TeacherProfile, SchoolProfile
from api.serializers import UserSerializer
from api.views import DeleteAcountView, SignupView, LoginView
from rest_framework.test import force_authenticate


CustomUser = get_user_model()

class DeleteAccountViewTest(APITestCase):

    def setUp(self):
        # Create a test user
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.factory = RequestFactory()  # Create a factory for making requests
        self.view = DeleteAcountView.as_view()  # Get the view instance

    @patch('api.models.CustomUser.delete')  # Patch the delete method in the models
    def test_delete_account_authenticated_user(self, mock_delete):
        # Create a DELETE request for the delete account endpoint
        request = self.factory.delete('/api/delete_account/')
        request.user = self.user  # Simulate an authenticated user
        force_authenticate(request, user=self.user)
        response = self.view(request)


        # Assert that delete was called exactly once
        mock_delete.assert_called_once()

        # Assert the response status code is 204 No Content
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)



class RegisterUserViewTest(APITestCase):
    def setUp(self) -> None:
        self.data = {
            "username": "testuser",
            "password": "testpassword",
            "user_type": "teacher",
            "subject": "Math",
        }
        # self.user = User.objects.create(self.data)
        self.factory = RequestFactory()
        self.view = SignupView.as_view()

    @patch('api.serializers.UserSerializer.save')
    def test_signup_view(self, mock_post):
        request = self.factory.post(path='api/singup', data=self.data)
        response = self.view(request)

        mock_post.assert_called_once()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class LoginViewTest(APITestCase):
    def setUp(self) -> None:
        self.data = {
            "username": "testuser",
            "password": "testpassword",
            "user_type": "teacher",
            "subject": "Math",
        }
        # self.user = User.objects.create(self.data)
        self.factory = RequestFactory()
        self.view = LoginView.as_view()

    def test_login(self):
        user = CustomUser.objects.create_user(self.data)
        request = self.factory.post('api/login', self.data)
        response = self.view(request)
        print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)