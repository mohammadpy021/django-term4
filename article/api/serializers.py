from rest_framework import serializers
from article.models.course import Course, Category
from article.models.video import Videos
from article.models.question import Quiz
from article.models.question import Question, QuizProfile
from article.models.home_page import HomePage

# Serializers for nested objects 

# class VideoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Videos
#         fields = ('id', 'title', 'position', 'duration', 'is_free', 'videofile', 'video_thumbnail')

class VideoListSerializer(serializers.ModelSerializer):
    """ This will be used inside CourseDetail to show the list of videos WITHOUT the file link """
    class Meta:
        model = Videos
        #  'videofile' Removed from here to protect it by unathenticated users
        fields = ('id', 'title', 'position', 'duration', 'is_free', 'video_thumbnail')

class VideoDetailSerializer(serializers.ModelSerializer):
    """ This will be used when a user explicitly requests to watch a specific video """
    class Meta:
        model = Videos
        # 'videofile' is included here because this serializer will be protected by our Permission
        fields = ('id', 'title', 'position', 'duration', 'is_free', 'videofile', 'video_description')
        
class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ('id', 'title', 'position', 'type')

# Serializer for the Course List (Grid View) 

class CourseListSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    
    class Meta:
        model = Course
        fields = ('id', 'title', 'slug', 'image', 'price', 'is_free', 'author_name', 'time_of_course')

# Serializer for Course Detail (Single Course View) 

class CourseDetailSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    
    # related_name of the model
    videos = VideoListSerializer(many=True, read_only=True)
    quizes = QuizSerializer(many=True, read_only=True)
    
    class Meta:
        model = Course
        fields = (
            'id', 'title', 'slug', 'description', 'image', 'price', 'is_free', 
            'author_name', 'time_of_course', 'prerequisite', 'created_at',
            'videos', 'quizes' 
        )
        
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        # we diidn't bring "ans" field here that user doesn't see the answer via the network of browser
        fields = ('id', 'question', 'op1', 'op2', 'op3', 'op4', 'position')

class QuizResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizProfile
        fields = ('corrects', 'incorrects', 'total_score', 'is_done', 'choices')
        
class QuizSubmitSerializer(serializers.Serializer):
    """ sc"""
    answers = serializers.JSONField(
        default={"1": "op1", "2": "op2"},
        help_text="""Enter your answers here. Example: {'1': 'op4', '2': 'op3'}
        this means the exam with id 1 option 4 and exam with id 2 is op3
        """
    )
    
    
class HomePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomePage
        fields = '__all__' # Return all fields (title, banner, etc.)