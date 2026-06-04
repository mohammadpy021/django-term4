from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class RegistrationAPITest(APITestCase):
    
    def setUp(self):
        """
        Setup variables for registration tests.
        Using reverse with the exact namespace from accounts/api/urls.py
        """
        self.register_url = reverse('accounts_api:register')
        
        self.valid_payload = {
            "email": "teststudent@gmail.com",
            "username": "teststudent",
            "password": "StrongPassword123!",
            "password_confirm": "StrongPassword123!"
        }
        
        self.invalid_payload = {
            "email": "hacker@gmail.com",
            "username": "hacker",
            "password": "StrongPassword123!",
            "password_confirm": "WrongPassword!"
        }

    def test_register_new_user_successfully(self):
        """
        Test if a user can successfully register with correct credentials.
        """
        response = self.client.post(self.register_url, self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        user_exists = User.objects.filter(email=self.valid_payload['email']).exists()
        self.assertTrue(user_exists)
        print("Success: Valid user registration test passed!")

    def test_register_user_with_mismatched_passwords(self):
        """
        Test if the API blocks registration when passwords do not match.
        """
        response = self.client.post(self.register_url, self.invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        user_exists = User.objects.filter(email=self.invalid_payload['email']).exists()
        self.assertFalse(user_exists)
        print("Success: Mismatched password security test passed!")


class LoginAPITest(APITestCase):
    
    def setUp(self):
        """
        Setup a real user in the test database to test the login process.
        Using reverse with the exact name from core/urls.py
        """
        self.login_url = reverse('api_login') 
        self.user_password = "StrongPassword123!"
        self.user_email = "teststudent2@gmail.com" # Changed email to avoid conflict
        
        # Create a user in the test database
        self.user = User.objects.create_user(
            email=self.user_email,
            username="teststudent2",
            password=self.user_password
        )

    def test_login_user_and_get_jwt_token(self):
        """
        Test if a valid user can log in and receive JWT access/refresh tokens.
        """
        payload = {
            "email": self.user_email,
            "password": self.user_password
        }
        
        response = self.client.post(self.login_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        print("Success: User login and JWT token generation test passed!")

    def test_login_user_with_wrong_password(self):
        """
        Test if the API blocks login attempts with incorrect passwords.
        """
        payload = {
            "email": self.user_email,
            "password": "WrongPassword!"
        }
        
        response = self.client.post(self.login_url, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('access', response.data)
        print("Success: Security test for wrong password passed!")