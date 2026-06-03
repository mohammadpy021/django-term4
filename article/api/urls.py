from django.urls import path
from . import views

app_name = 'article_api'

urlpatterns = [
    path('home/', views.HomePageAPIView.as_view(), name='home-page'),
    path('courses/', views.CourseListAPIView.as_view(), name='course-list'),
    path('courses/<slug:slug>/', views.CourseDetailAPIView.as_view(), name='course-detail'),
    path('videos/<int:pk>/', views.VideoRetrieveAPIView.as_view(), name='video-detail'),
    
    path('quiz/<int:quiz_id>/', views.QuizTakeAPIView.as_view(), name='quiz-take'),
    
    path('courses/<int:course_id>/enroll/', views.CourseEnrollAPIView.as_view(), name='course-enroll'),
    path('my-courses/', views.MyCoursesAPIView.as_view(), name='my-courses'),
]