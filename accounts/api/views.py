from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from accounts.tasks import send_welcome_email_task

from .serializers import RegisterSerializer


class RegisterAPIView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = RegisterSerializer
    
    def perform_create(self, serializer):
        # Save the user to the database
        user = serializer.save()
        
        print(f"Triggering background email task for {user.email}")
        send_welcome_email_task.delay(user.email)
        
        