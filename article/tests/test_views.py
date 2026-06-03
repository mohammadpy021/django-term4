from django.test import TestCase
from django.urls import reverse
from article.models import Course
from django.contrib.auth import get_user_model
from django.test.client import Client
from django.core.files.uploadedfile import SimpleUploadedFile

from django.contrib import auth
import tempfile



class TestHomeView(TestCase):
    
    def setUp(self):
        self.user = get_user_model().objects.create_superuser(username='testuser',email='testuser@gmail.com', password='12345')
        c = Client()
        self.logged_in_user = c.login(email='testuser@gmail.com', password='12345')
        # self.client.force_login(get_user_model().objects.get_or_create(username='testuser')[0])
        # self.client.login(username='Adam', password='password')
        
    def test_home_user_authenticated(self):
        course = Course(title="My Title",
                        publish_status="completed",
                      is_active=True,
                      author= self.user,
                      image= tempfile.NamedTemporaryFile(suffix=".jpg").name ,
                      slug="test-unique",
                      time_of_course="11:11:11")
        self.assertEqual(course.title, "My Title")
    
    def test_home_user_anonymous(self):
        pass