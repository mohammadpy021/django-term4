from rest_framework import generics, filters, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
# from rest_framework import serializers
from drf_spectacular.utils import extend_schema
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from article.models.question import Quiz, QuizProfile
from article.models.course import Course
from article.models.video import Videos
from article.models.home_page import HomePage
from .serializers import HomePageSerializer
from .serializers import QuestionSerializer, QuizResultSerializer
from .serializers import CourseListSerializer, CourseDetailSerializer, VideoDetailSerializer, QuizSubmitSerializer
from .permissions import HasVideoAccess

class HomePageAPIView(generics.RetrieveAPIView):
    serializer_class = HomePageSerializer
    permission_classes = (AllowAny,)

    def get_object(self):
        # Always return the first HomePage object created in the database
        homepage = HomePage.objects.first()
        return homepage
    
class CourseEnrollAPIView(APIView):
    # add course to the cousrse list  of user
    permission_classes = [IsAuthenticated]
    # serializer_class = serializers.Serializer
    @extend_schema(responses={200: dict, 400: dict})
    def post(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        
        # Check if the user is already enrolled in this course
        if request.user.courses.filter(id=course_id).exists():
            return Response({
                "error": "You are already enrolled in this course.",
                "course_title": course.title
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # If not enrolled, add the course to the user's M2M field
        request.user.courses.add(course)
        return Response({
            "message": "Successfully enrolled in the course.",
            "course_title": course.title
        }, status=status.HTTP_200_OK)
class MyCoursesAPIView(generics.ListAPIView):
    """
    Return a list of courses that the logged-in user has enrolled in.
    """
    serializer_class = CourseListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.courses.all()
    
class CourseListAPIView(generics.ListAPIView):
    queryset = Course.objects.active()
    serializer_class = CourseListSerializer
    # permission_classes = (AllowAny,)
    

    filter_backends = [filters.SearchFilter]    
    search_fields = ['title', 'description']
    # Cache the output of this view for 15 minutes (60 seconds * 15)
    @method_decorator(cache_page(60 * 15))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
class CourseDetailAPIView(generics.RetrieveAPIView):
    queryset = Course.objects.active()
    serializer_class = CourseDetailSerializer
    # permission_classes = (AllowAny,)
    lookup_field = 'slug'
    
class VideoRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Videos.objects.filter(
        publish=True, 
        course__is_active=True,
    )
    serializer_class = VideoDetailSerializer

    permission_classes = (HasVideoAccess,)
    

class QuizTakeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    # serializer_class = serializers.Serializer
    def get(self, request, quiz_id):
        """
        get list of questions for a quiz, or return the result if the user has already taken it.
        """
        quiz = get_object_or_404(Quiz, id=quiz_id, publish=True)
        quiz_profile, created = QuizProfile.objects.get_or_create(quiz=quiz, user=request.user)

        if quiz_profile.is_done:
            # If the user has already completed the quiz, return their results
            serializer = QuizResultSerializer(quiz_profile)
            return Response({
                "message": "You have already completed this quiz.",
                "results": serializer.data
            })
        else:
            # If not completed, send the list of questions (without answers to prevent cheating)
            questions = quiz.question.filter(publish=True).order_by('position')
            serializer = QuestionSerializer(questions, many=True)
            return Response({
                "quiz_title": quiz.title,
                "questions": serializer.data
            })
    @extend_schema(request=QuizSubmitSerializer, responses=QuizResultSerializer)
    def post(self, request, quiz_id):
        """
        Submit user answers, calculate the score, and save the profile.
        """
        quiz = get_object_or_404(Quiz, id=quiz_id, publish=True)
        quiz_profile = get_object_or_404(QuizProfile, quiz=quiz, user=request.user)

        if quiz_profile.is_done:
            return Response(
                {"error": "This quiz is already completed."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # We expect the payload format from frontend: {"answers": {"1": "op1", "2": "op3"}}
        user_answers = request.data.get('answers', {})

        correct = 0
        wrong = 0
        total = 0
        user_choices = {}

        questions = quiz.question.filter(publish=True)

        for q in questions:
            total += 1
            # Get the user's answer for this specific question ID
            user_ans = user_answers.get(str(q.id))

            # Store the user's choice and the correct answer
            user_choices[str(q.id)] = {"user": user_ans, "answer": q.ans}

            # Check if the answer is correct
            if user_ans == q.ans:
                correct += 1
            else:
                wrong += 1

        # Calculate the percentage
        percent = (correct / total) * 100 if total > 0 else 0

        # Update and save the quiz profile
        quiz_profile.choices = user_choices
        quiz_profile.corrects = correct
        quiz_profile.incorrects = wrong
        quiz_profile.total_score = int(percent)
        quiz_profile.is_done = True
        quiz_profile.save()

        # Add the course to the user's enrolled courses if not already there
        if quiz.course and quiz.course not in request.user.courses.all():
            request.user.courses.add(quiz.course)

        return Response({
            "message": "Quiz submitted successfully!",
            "results": QuizResultSerializer(quiz_profile).data
        }, status=status.HTTP_200_OK)