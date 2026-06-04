from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from datetime import timedelta
from django.urls import reverse
from article.models.course import Course
from article.models.question import Quiz, Question, QuizProfile

User = get_user_model()

class QuizIntegrationTest(APITestCase):

    def setUp(self):
        """
        Set up initial data for testing the Quiz API.
        """
        self.teacher = User.objects.create_user(email="teacher@test.com", username="teacher", password="password123")
        self.student = User.objects.create_user(email="student@test.com", username="student", password="password123")

        self.course = Course.objects.create(
            title="Python Basics",
            slug="python-basics",
            author=self.teacher,
            is_active=True,
            time_of_course=timedelta(hours=10)
        )

        self.quiz = Quiz.objects.create(
            title="Midterm Quiz",
            course=self.course,
            publish=True
        )

        self.q1 = Question.objects.create(
            quiz=self.quiz,
            question="What is 2+2?",
            op1="3", op2="4", op3="5", op4="6",
            ans="op2", 
            publish=True
        )
        
        self.q2 = Question.objects.create(
            quiz=self.quiz,
            question="What is the capital of France?",
            op1="London", op2="Berlin", op3="Paris", op4="Rome",
            ans="op3", 
            publish=True
        )

        # Getting JWT Token for the student using the dynamic URL
        login_url = reverse('api_login')
        response = self.client.post(login_url, {
            "email": "student@test.com",
            "password": "password123"
        })
        self.access_token = response.data['access']
        
        # Set the authorization header for all future requests in this test
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_submit_quiz_and_calculate_score(self):
        """
        Test if a student can take a quiz and get correct scores and course enrollment.
        """
        url = reverse('article_api:quiz-take', kwargs={'quiz_id': self.quiz.id})
        
        # 1. Simulate frontend loading the quiz page first (creates QuizProfile)
        self.client.get(url)
        
        # 2. Submit the answers
        payload = {
            "answers": {
                str(self.q1.id): "op2", # Correct
                str(self.q2.id): "op1"  # Wrong
            }
        }

        response = self.client.post(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        results = response.data['results']
        self.assertEqual(results['corrects'], 1)
        self.assertEqual(results['incorrects'], 1)
        self.assertEqual(results['total_score'], 50) 
        self.assertTrue(results['is_done'])

        self.assertTrue(self.student.courses.filter(id=self.course.id).exists())
        print("Success: Quiz scoring and enrollment logic test passed!")

    def test_prevent_double_submission(self):
        """
        Ensure a student cannot take the same quiz twice.
        """
        url = reverse('article_api:quiz-take', kwargs={'quiz_id': self.quiz.id})
        
        # 1. Simulate frontend loading the quiz page first (creates QuizProfile)
        self.client.get(url)
        
        # First submission
        self.client.post(url, {"answers": {}}, format='json')
        
        # Second submission attempt
        response = self.client.post(url, {"answers": {}}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        print("Success: Double submission protection test passed!")